"""Gera wikitext2_train.txt (corpus local usado por todos os experimentos).
Roda UMA vez antes dos phases. Requer `pip install datasets`."""
from datasets import load_dataset

ds = load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1", split="train")
lines = [t.strip() for t in ds["text"] if len(t.strip()) >= 200]
with open("wikitext2_train.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("escritas", len(lines), "linhas uteis")
