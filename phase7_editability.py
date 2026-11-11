"""P0 V1 ANOVA intervention: offset mask, last-token evaluation, intact row 0."""
from sampling import MODELS
import argparse
import torch
from phase2_downstream import attention_forward, normalize_reconstruction, validate_attention, record_reconstruction_rows, run_suite, factor_svd
from phase8_lostmiddle import finish_sink_edit

RECON = {"mode": "identity", "k": 8, "stats": {}, "empty_row_policy": "uniform", "svd_driver": None, "parallel_svd": False}

def reconstruct(weights):
    mode = RECON["mode"]
    if mode == "identity":
        record_reconstruction_rows(weights, RECON["stats"])
        validate_attention(weights, RECON["stats"])
        return weights
    x = weights.float()
    q, kk = x.shape[-2:]
    mu = x.mean(dim=(-1, -2), keepdim=True)
    additive = x.mean(dim=-1, keepdim=True) + x.mean(dim=-2, keepdim=True) - mu
    u, s, vh = factor_svd(x - additive, RECON["svd_driver"], RECON["parallel_svd"])
    k = min(RECON["k"], q, kk)
    recon = additive + (u[..., :k] * s[..., None, :k]) @ vh[..., :k, :]
    # Reconstruct first, using the same uniform completion as SVD/geom/S+L.
    # Sink edits then preserve the reconstructed baseline if no alternative
    # exists. They never restore a row from the uncompressed attention.
    baseline = normalize_reconstruction(recon, weights, RECON["stats"],
                                        RECON["empty_row_policy"], cast_to_original=False)
    if mode in ("nosink", "zerocol_mid"):
        col = 0 if mode == "nosink" else kk // 2
        edited = baseline.clone()
        edited[..., col] = 0
        baseline = finish_sink_edit(baseline, edited, RECON["stats"])
    elif mode != "anova":
        raise ValueError(f"Unknown ANOVA mode {mode}")
    result = baseline.to(weights.dtype)
    validate_attention(result, RECON["stats"])
    if mode in ("nosink", "zerocol_mid") and q == kk:
        if getattr(RECON["stats"], "defer_validation", False):
            RECON["stats"].add_scalar("sink_edit_first_row_changes", (result[...,0,:] != weights[...,0,:]).sum())
        elif not torch.equal(result[..., 0, :], weights[..., 0, :]):
            raise RuntimeError("Sink intervention changed the first row")
    return result

def recon_attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0.0, **kwargs):
    return attention_forward(module, query, key, value, attention_mask, scaling, dropout, reconstruct_fn=reconstruct, **kwargs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--empty-row-policy", choices=["uniform"], default="uniform")
    args = ap.parse_args()
    run_suite(args.models, ("phase7",), args.batch, args.empty_row_policy)

if __name__ == "__main__":
    main()
