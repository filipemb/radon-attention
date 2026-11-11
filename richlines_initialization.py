"""Deterministic multiscale line initialization for the gradient experiment.

Convolving a digital sinogram along offsets proposes broad continuous lines.
The actual continuous atoms are rendered and refitted by NNLS. This is an
initialization only, with at most 32 greedy proposals; every final atom has
the same five stored parameters and is subsequently optimized by gradient.
"""
import numpy as np
from scipy.fft import irfft,rfft,next_fast_len
from richlines_core import NNLSActive


class MultiscaleInitializer:
    def __init__(self,dictionary):
        self.d=dictionary
        n=dictionary.n
        self.widths=np.array([0.5,1,2,4,8,16,32],dtype=float)
        self.widths=self.widths[self.widths<=n/4]
        self.low=int(dictionary.offset.min())
        self.high=int(dictionary.offset.max())
        self.length=self.high-self.low+1
        half=int(np.ceil(6*self.widths.max()))
        offsets=np.arange(-half,half+1)
        q=offsets[None,:]/self.widths[:,None]
        kernels=np.exp(-0.5*q*q)*np.maximum(1-q*q/36,0)**3
        self.half=half
        self.fft_length=next_fast_len(self.length+len(offsets)-1)
        self.kernels_fft=rfft(kernels,n=self.fft_length,axis=-1)
        self.squared_fft=rfft(kernels*kernels,n=self.fft_length,axis=-1)
        counts=np.zeros((dictionary.angles,self.length))
        self.ai=dictionary.angle_id.astype(int)
        self.ri=dictionary.offset-self.low
        self.lengths=np.sqrt(np.diff(dictionary.D.indptr))
        counts[self.ai,self.ri]=self.lengths**2
        transformed=rfft(counts,n=self.fft_length,axis=-1)
        norms2=irfft(self.squared_fft[:,None,:]*transformed[None,:,:],n=self.fft_length,axis=-1)
        self.norms=np.sqrt(np.maximum(norms2[:,:,half:half+self.length],1e-20))
        self.valid=counts>0

    def fit(self,target,max_k=32):
        from richlines_parametric import render_numpy
        d=self.d;n=d.n
        max_k=min(32,max_k)
        target=np.asarray(target,dtype=float)
        residual=target.copy()
        columns=[];parameters=[];chosen=[];h=[];x=np.empty(0);snapshots={}
        G=np.zeros((max_k,max_k));state=NNLSActive()
        for step in range(1,max_k+1):
            raw=np.zeros((d.angles,self.length))
            raw[self.ai,self.ri]=(d.D@residual)*self.lengths
            transformed=rfft(raw,n=self.fft_length,axis=-1)
            correlations=irfft(self.kernels_fft[:,None,:]*transformed[None,:,:],n=self.fft_length,axis=-1)
            correlations=correlations[:,:,self.half:self.half+self.length]/self.norms
            correlations[:,~self.valid]=-np.inf
            correlations.reshape(-1)[chosen]=-np.inf
            pick=int(np.argmax(correlations))
            wi,ai,ri=np.unravel_index(pick,correlations.shape)
            theta=d.theta[ai]
            offset=ri+self.low-(n-1)/2*(np.cos(theta)+np.sin(theta))
            primitive=np.array([theta,offset,self.widths[wi],0.0,1.0])
            atom=render_numpy(primitive[None,:],n)
            if not np.isfinite(atom).all():
                raise ValueError("Invalid continuous multiscale initialization atom")
            if columns:
                cross=np.asarray(columns)@atom
                G[step-1,:step-1]=cross;G[:step-1,step-1]=cross
            G[step-1,step-1]=atom@atom
            columns.append(atom);parameters.append(primitive);chosen.append(pick);h.append(float(atom@target))
            x,_=state.refit(G[:step,:step],np.asarray(h),np.r_[x,0.0])
            residual=target-np.asarray(columns).T@x
            p=np.asarray(parameters).copy();p[:,4]=x
            snapshots[step]=p
        return snapshots
