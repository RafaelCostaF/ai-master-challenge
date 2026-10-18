# DEVELOPMENT_PROCESS — Decisões e divisores de águas

| Data | Decisão | Motivo | Alternativa descartada |
|------|---------|--------|------------------------|
| 2026-10-18 | Challenge 004 (Social Media) | Objetivo é gerar valor para empresa de marketing | 001, 002, 003 |
| 2026-10-18 | `instructions/`, `knowledge/` dentro de `submissions/rafael/` | PR só aceita arquivos na pasta da submissão; também servem de process log | Pastas na raiz do repo |
| 2026-10-18 | Tratar dataset como **sintético** até prova em contrário | Descrição do Kaggle declara geração aleatória (Poisson) | Assumir dados reais e extrair "insights" do ruído |
| 2026-10-18 | `git add -f` para arquivos da submissão | `.gitignore` raiz ignora `submissions/`; alterar arquivo fora da pasta é proibido | Editar `.gitignore` raiz |
| 2026-10-18 | **Dataset é ruído puro (confirmado)** → entrega foca em provar isso, em um método/ferramenta validados com efeito injetado e em decisões que não dependem de engajamento | Todas as features com p > 0,2; métricas Poisson independentes; seguidores sem efeito | Reportar diferenças de 0,0001 como insights (o que o baseline de LLM faz) |
| 2026-10-18 | EDA em notebook executado (`solution/notebooks/01_eda.ipynb`) antes de definir a estratégia | Usuário quer entender colunas, valores e relações por conta própria antes de decidir a direção | Pular direto para a estratégia "dados = ruído" |
| 2026-10-18 | Duas frentes de análise: **geral** (notebook 02) e **por plataforma** (notebook 03), com as mesmas funções | Pedido do usuário; o time de marketing opera por plataforma | Uma análise só, agregada |
| 2026-10-18 | Código em pacote (`solution/src/social_insights`) + pytest; notebooks gerados por scripts em `notebooks/build/` | Clean Code, reuso entre frentes, reprodutibilidade | Lógica duplicada dentro dos notebooks |
| 2026-10-18 | FDR (Benjamini-Hochberg) obrigatório em toda bateria de testes, e correção **global** entre plataformas | Milhares de testes geram ~5% de falsos positivos; no 03, 3 "achados" por tabela somem na correção global | Reportar p < 0,05 cru (o que o baseline de LLM faz) |
| 2026-10-18 | Nulo por permutação em vez de Hopkins para testar se há clusters | Hopkins deu 0,88–0,94 (falso positivo em nuvem gaussiana) | Estatística de Hopkins |
| 2026-10-18 | NLP também em legendas/hashtags, não só em comentários | Comentário é consequência; legenda/hashtag é alavanca do time | Só comentários |
| 2026-10-18 | Controle positivo (+2% views plantado) em todas as frentes | Provar que "sem achados" não é falta de sensibilidade do método | Confiar no resultado nulo sem validação |
| 2026-10-18 | Adotar o plano de ação do usuário (`knowledge/action-plan.md`) como notebook 04, reaproveitando `social_insights` | Pedido do usuário; o plano acrescenta pré×pós-publicação, taxas por seguidor, RF/XGBoost/CatBoost, SHAP e recomendações | Manter só os notebooks 02/03 |
| 2026-10-18 | SHAP comparado com modelo de alvo embaralhado; R² de treino mostrado ao lado da validação | Sem esse contraste, rankings de importância e R² de treino (~0,1) seriam lidos como fatores reais | Reportar ranking SHAP/feature importance isolado |
| 2026-10-18 | Módulo `questions.py` + CLI `answer_questions.py`: uma função por pergunta do desafio, com veredito gerado dos dados | Resposta direta e reproduzível às 4 perguntas obrigatórias; serve de ferramenta recorrente | Respostas escritas à mão nos notebooks |
| 2026-10-18 | Patrocínio: diferença estratificada (plataforma × formato × categoria × porte) + regressão com controles; custo implícito = US$ 10 por mil seguidores (premissa configurável) | O desafio exige comparação justa; o dataset não tem preço | Comparar médias brutas; ignorar custo |
| 2026-10-18 | Estratégia (`strategy.py`): "entre opções equivalentes, vence a mais barata"; threshold de patrocínio por ponto de equilíbrio (CPM/CPE-alvo); frequência via volume diário × desempenho por plataforma | Os dados não mostram vencedor, então a decisão racional é por custo; `creator_id` instável impede medir frequência por creator | Recomendar o "melhor" aparente (ruído); frequência por creator |
