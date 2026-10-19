# Atalhos para reproduzir a entrega do zero (rodar dentro de submissions/rafael). Requer Python 3.14.
PY := .venv/bin/python
NOTEBOOK_BUILDERS := $(wildcard solution/notebooks/build/build_*.py)

.PHONY: all setup data test report notebooks site

all: setup data test report notebooks   ## tudo, menos subir o site

setup:                                   ## ambiente virtual + dependências fixadas + pacotes locais
	python3.14 -m venv .venv
	.venv/bin/pip install -q -r requirements.txt
	.venv/bin/pip install -q -e .

data:                                    ## baixa o CSV do Kaggle e confere o sha256
	bash scripts/get_data.sh data/raw

test:                                    ## testes automatizados (efeitos plantados + rotas do site)
	$(PY) -m pytest -q

report:                                  ## regenera docs/respostas.md (4 perguntas + estratégia + fila de testes)
	$(PY) solution/answer_questions.py --out docs/respostas.md

notebooks:                               ## regenera e executa os 14 notebooks
	for b in $(NOTEBOOK_BUILDERS); do \
		name=$$(basename $$b .py | sed 's/^build_//'); \
		$(PY) $$b solution/notebooks/$$name.ipynb || exit 1; \
		.venv/bin/jupyter nbconvert --to notebook --execute --inplace solution/notebooks/$$name.ipynb || exit 1; \
	done

site:                                    ## sobe o site em http://127.0.0.1:8000 (1ª vez treina tudo, ~5 min)
	.venv/bin/social-web
