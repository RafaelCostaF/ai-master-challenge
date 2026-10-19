# Site de entrega (com servidor) — arquitetura e como usar

Código: `solution/src/social_web/` · comando: `.venv/bin/social-web` · atualizado em 2026-10-19.
Substitui o site estático anterior (removido): agora há servidor, linguagem para leigos, previsões feitas no servidor e painel estilo Power BI.

## Como rodar
```bash
cd submissions/rafael
python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pip install -e .
.venv/bin/social-web                 # http://127.0.0.1:8000  (1ª vez: treina e calcula tudo, ~5 min; depois sobe em segundos)
.venv/bin/social-web --rebuild       # após trocar o CSV pelos dados da empresa
.venv/bin/social-web --host 0.0.0.0 --port 8080   # para expor na rede
```
Cache: `solution/models/web_models.joblib` (modelos) e `site_payload.json` (conteúdo), fora do git.

## Arquitetura
| Módulo | Papel |
|---|---|
| `server.py` | FastAPI: `create_app(state)` (testável), rotas das páginas (Jinja2), API, filtros pt-BR (`num`, `pct`, `pt`, `label`, `val`, `words`), CLI `main()` |
| `state.py` | carrega o CSV, treina/lê do cache: chance de top 5%, previsão de views, engajamento; monta o payload de conteúdo (`site_export.build_payload`) |
| `predict.py` | `PredictionService`: monta o post (faixas, horário, histórico do creator), chama os 3 modelos, cruza com as descobertas e escreve o resumo em linguagem simples |
| `explore.py` | agregações do painel: filtros, cartões, comparação de grupos (com marcação de "diferença real" corrigida), série mensal sem meses incompletos, matriz e top 10 |
| `schemas.py` | validação das entradas da API (pydantic) |
| `templates/` | 7 páginas: Início · As 4 perguntas · Estratégia · Descobertas · Explorar dados · Prever um post · Como chegamos lá |
| `static/` | CSS (tema claro/escuro, responsivo), `common.js` (formatação, selos de evidência, gráficos) e Chart.js embutido (funciona offline) |

## API (documentação automática em `/docs`)
| Rota | Uso |
|---|---|
| `POST /api/predict` | corpo = post planejado (plataforma, formato, tema, idioma, horário, seguidores, duração, público, patrocínio, creator opcional) → chance de top 5% por métrica, comparação entre formatos, views e engajamento esperados com faixa provável, descobertas que se aplicam, resumo em frases |
| `POST /api/explore` | filtros + agrupamento + métrica + linhas/colunas da matriz + período → tudo que o painel desenha |
| `GET /api/options` | valores dos filtros e métricas disponíveis |
| `GET /api/health` | status |

## Linguagem para leigos (padrão do site)
- "Virar destaque" = top 5%. "Faixa provável" = intervalo de 90%. "2x mais chance" = o dobro do normal.
- Selos: **confirmado** (passou em tudo) · **se repetiu nos 2 anos** (candidato a teste) · **pista** (pode ser coincidência).
- Jargão técnico (q-value, AUC, R²) só dentro de "Detalhes técnicos".

## Testes
`solution/tests/test_web.py` (dados sintéticos e modelos leves) cobre:
- filtros, cartões, marcação de diferença real e ordem natural;
- remoção de meses incompletos e casamento das descobertas;
- as 7 páginas renderizando;
- as APIs `explore` e `predict`, incluindo a validação de entrada (422).
