# Ambiente

- Repo clonado de `Gestao-Quatro-Ponto-Zero/ai-master-challenge`; remote renomeado para `upstream`; branch `submission/rafael`.
- Fork: `origin` = git@github.com:RafaelCostaF/ai-master-challenge.git (SSH; HTTPS falha sem TTY). `gh` não instalado.
- Python 3.14; `.venv` com `requirements.txt` (versões fixadas pelo pip freeze; as versões antigas não compilam no 3.14).
- Kaggle: `~/.kaggle/kaggle.json` (chmod 600); download via API com curl.
- Root `.gitignore` ignora `submissions/` e não pode ser alterado → sempre `git add -f submissions/rafael/<arquivo>` (o `.gitignore` local ainda vale para não usar `-f` em dados).
- `git add -f <pasta>` também adiciona arquivos ignorados (`__pycache__`, dados) → adicionar arquivo por arquivo ou conferir `git status` antes do commit.
