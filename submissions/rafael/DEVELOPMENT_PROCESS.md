# DEVELOPMENT_PROCESS — Decisões e divisores de águas

| Data | Decisão | Motivo | Alternativa descartada |
|------|---------|--------|------------------------|
| 2026-10-18 | Challenge 004 (Social Media) | Objetivo é gerar valor para empresa de marketing | 001, 002, 003 |
| 2026-10-18 | `instructions/`, `knowledge/` dentro de `submissions/rafael/` | PR só aceita arquivos na pasta da submissão; também servem de process log | Pastas na raiz do repo |
| 2026-10-18 | Tratar dataset como **sintético** até prova em contrário | Descrição do Kaggle declara geração aleatória (Poisson) | Assumir dados reais e extrair "insights" do ruído |
| 2026-10-18 | `git add -f` para arquivos da submissão | `.gitignore` raiz ignora `submissions/`; alterar arquivo fora da pasta é proibido | Editar `.gitignore` raiz |
| 2026-10-18 | **Dataset é ruído puro (confirmado)** → entrega foca em provar isso, em um método/ferramenta validados com efeito injetado e em decisões que não dependem de engajamento | Todas as features com p > 0,2; métricas Poisson independentes; seguidores sem efeito | Reportar diferenças de 0,0001 como insights (o que o baseline de LLM faz) |
