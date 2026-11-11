"""Same cuSOLVER SVD, independent head groups on three CUDA streams.

This changes execution scheduling only. The exact torch default driver,
float32 precision, ranks and returned factor strides are preserved. Its caller
must compare actual full-model logits bit for bit before enabling the schedule.
There are three worker threads plus the main thread, and one process/GPU lock.
"""
from sampling import MODELS  # datasets and native thread caps precede torch.
from concurrent.futures import ThreadPoolExecutor
import math
import torch

_POOL = None
_STREAMS = {}
WORKERS = 3

@torch.inference_mode()
def _factor(part,stream,driver):
    with torch.cuda.device(part.device), torch.cuda.stream(stream):
        return torch.linalg.svd(part,full_matrices=False,driver=driver)

def parallel_svd(weights,driver=None):
    global _POOL
    if weights.device.type != "cuda" or weights.dtype != torch.float32:
        raise ValueError("Parallel P0 scheduling is only for unchanged float32 CUDA SVD")
    m,n=weights.shape[-2:];batch_shape=weights.shape[:-2]
    total=math.prod(batch_shape)
    if total<WORKERS or min(m,n)<64:
        return torch.linalg.svd(weights,full_matrices=False,driver=driver)
    if _POOL is None:
        _POOL=ThreadPoolExecutor(max_workers=WORKERS,thread_name_prefix="p0_svd")
    device=str(weights.device)
    if device not in _STREAMS:
        _STREAMS[device]=[torch.cuda.Stream(device=weights.device) for _ in range(WORKERS)]
    streams=_STREAMS[device]
    main=torch.cuda.current_stream(weights.device)
    flat=weights.reshape(total,m,n)
    size=math.ceil(total/WORKERS)
    jobs=[]
    for start,stream in zip(range(0,total,size),streams):
        stop=min(start+size,total)
        part=flat[start:stop]
        # Inputs were produced on the model stream. Each factorization waits
        # for that event, without a device-to-host synchronization.
        stream.wait_stream(main)
        part.record_stream(stream)
        jobs.append((start,stop,stream,_POOL.submit(_factor,part,stream,driver)))
    pieces=[]
    for start,stop,stream,future in jobs:
        u,s,vh=future.result()  # exceptions propagate, never silently fallback.
        main.wait_stream(stream)
        for tensor in (u,s,vh):tensor.record_stream(main)
        pieces.append((start,stop,u,s,vh))
    # Preserve torch.linalg.svd's column/row-major factor layouts. A plain cat
    # would change strides and could change subsequent float32 GEMM rounding.
    first=pieces[0];rank=first[3].shape[-1]
    u0,s0,vh0=first[2:]
    u=torch.empty_strided((total,m,rank),(u0.stride(0),*u0.stride()[-2:]),device=weights.device,dtype=u0.dtype)
    s=torch.empty_strided((total,rank),(s0.stride(0),s0.stride(-1)),device=weights.device,dtype=s0.dtype)
    vh=torch.empty_strided((total,rank,n),(vh0.stride(0),*vh0.stride()[-2:]),device=weights.device,dtype=vh0.dtype)
    for start,stop,pu,ps,pvh in pieces:
        u[start:stop].copy_(pu);s[start:stop].copy_(ps);vh[start:stop].copy_(pvh)
    return (u.reshape(*batch_shape,m,rank),s.reshape(*batch_shape,rank),vh.reshape(*batch_shape,rank,n))
