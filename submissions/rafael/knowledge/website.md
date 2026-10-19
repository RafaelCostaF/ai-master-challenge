# G4 Marketing — site de entrega (com servidor): arquitetura, design e como usar

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

## Identidade visual e UX (2026-10-19)
- **Marca:** "G4 Marketing" no cabeçalho, com a paleta do G4 Educação levantada do site oficial: azul-marinho `#031A26`/`#001F35`, dourado `#B9915B`, off-white `#F5F4F3` e azul `#184560`.
- **Tipografia:** Playfair Display (o equivalente livre mais próximo da PP Museum usada pelo G4) nos títulos, com algarismos alinhados nos números de destaque; Manrope no texto, como no site do G4.
- **Divulgação progressiva:**
  - o **Resumo** é um painel de uma tela: 4 respostas, 2 destaques, "Comece / Pare / Teste" e atalhos para as ferramentas;
  - cada cartão tem "+ Ver detalhes";
  - nas páginas de aprofundamento, gráficos, tabelas e textos técnicos ficam fechados até o clique.
- **Navegação:** Resumo · Explorar dados · Prever um post · "Aprofundar ▾" (as 4 perguntas, estratégia, descobertas, como chegamos lá). Links do Resumo para `/perguntas#patrocinio` abrem a seção já expandida.
- **Ferramentas:**
  - **Explorar** mostra indicadores e o gráfico principal; evolução mensal, matriz e top 10 ficam em seções expansíveis.
  - **Prever** mostra só os campos essenciais (o resto em "Mais opções"); o resultado traz o resumo, as chances, as views e o engajamento, com "outro formato" e "descobertas" sob demanda.
  - As seções abertas pelo usuário continuam abertas quando o resultado é recalculado.
- **Gráficos em seções fechadas:** `lazyChart` desenha o gráfico ao abrir a seção, e um listener de `toggle` redimensiona gráficos já existentes.

## Painel "Explorar dados" (v2, 2026-10-19): simples e interativo
- **Métrica em um clique:** abas Views · Likes · Comentários · Engajamento + troca **Média / Chance de bombar** (top 5%). Os cartões de indicador também trocam a métrica.
- **Filtros:** chips de plataforma, formato e tema no topo; "Mais filtros" (popover) com os demais; período; etiquetas removíveis dos filtros ativos.
- **6 quadros sempre visíveis:** plataforma, formato, tema, tamanho do creator, uma característica à escolha e mês a mês.
  - As barras mostram a **diferença em relação à média** (centradas no zero, com o valor escrito).
  - Cores: dourado = acima de verdade, vermelho = abaixo de verdade, cinza = variação normal.
  - Cada quadro tem um selo ("sem diferença real" / "N diferenças reais").
- **Filtro cruzado (estilo Power BI):** clicar numa barra filtra o painel inteiro. O quadro da própria característica ignora o próprio filtro, para continuar mostrando todas as opções (as escolhidas ficam contornadas, as demais esmaecidas).
- **Frase-resumo automática:** o destaque real mais forte da seleção, ou "nenhum grupo se destaca".
- **Link compartilhável:** o estado fica no endereço, ex. `/explorar?m=likes&modo=chance&platform=TikTok&content_category=beauty`.
- **API:** `POST /api/explore` aceita `graficos: [...]` e devolve `graficos` (um breakdown por característica), `resumo` (destaque), `kpis`, `serie`, `matriz` e `top`.
