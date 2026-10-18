# Ambiente

- Repo clonado de `Gestao-Quatro-Ponto-Zero/ai-master-challenge`; remote renomeado para `upstream`; branch `submission/rafael`.
- `gh` CLI não instalado → fork via web (github.com → Fork) e depois `git remote add origin <fork>`.
- Python 3 sem pandas/sklearn → criar `.venv` com `requirements.txt`.
- Sem credencial Kaggle (`~/.kaggle/kaggle.json` ausente).
- Root `.gitignore` ignora `submissions/` e não pode ser alterado → sempre `git add -f submissions/rafael/<arquivo>` (o `.gitignore` local ainda vale para não usar `-f` em dados).
