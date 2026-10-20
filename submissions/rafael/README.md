# Submissão — Rafael — Challenge 004

## Sobre mim

- **Nome:** Rafael
- **LinkedIn:** https://www.linkedin.com/in/rafaelcostaf/
- **Challenge escolhido:** 004 — Estratégia Social Media

---

## Executive Summary

Separei o projeto em partes. Fiz o download do dataset e o setup inicial com instruções gerais (organização do repositório, arquivos `.md` com instruções para cada tipo de atividade a ser executada). Mantive agentes não "contaminados" com o problema para atividades como a validação dos resultados encontrados nos dados e a revisão da entrega. A recomendação principal é a **contratação de creators por resultado, não por post** (ex.: pagar creators por mil views ou por interação, medir todo patrocínio contra um grupo orgânico e testar antes de mudar a combinação.)

**Leitura de 5 minutos:** [`docs/resumo-executivo.md`](docs/resumo-executivo.md)

---

## Solução

### Abordagem

1. **Regras primeiro** ([`instructions/`](instructions/)): entregáveis, critérios de valor, padrão de código e uma regra central: todo número vem de código reproduzível.
2. **Entender os dados antes de opinar** (EDA, [`notebooks/01`](solution/notebooks/01_eda.ipynb)): as métricas são Poisson independentes (views ~10.100 ± 100 em todos os posts), os seguidores são uniformes de 0 a 1M e os textos são gerados. Isso mudou a entrega: em vez de vender ruído como insight, **provar com rigor o que não funciona** e entregar um método e uma ferramenta que funcionem com dados reais.
3. **Rigor estatístico em todas as frentes:**
   - correção para muitos testes (FDR), por plataforma e global;
   - comparação justa de patrocínio (269 estratos de plataforma × formato × categoria × porte, mais regressão);
   - efeito mínimo detectável em cada "não há efeito";
   - controle positivo (efeitos de 2–5% plantados precisam ser encontrados);
   - validação temporal nos modelos.
4. **Perguntas do desafio → funções** (`questions.py`, `strategy.py`): cada resposta e cada recomendação é um texto gerado dos números.
5. **Produto:** site FastAPI em linguagem para leigos, com resumo primeiro e detalhes sob demanda.
6. **Checagem independente** em sessões separadas: a descrição do dataset contra as conclusões e a entrega contra os requisitos ([`review/`](review/critica-entrega.md)).

### Resultados / Findings

| Pergunta | Resposta | Evidência |
|---|---|---|
| O que gera engajamento? | Nenhum fator testado | 450 combinações (até plataforma × formato × tema × porte): 22 com p < 0,05, o esperado por acaso; 0 após correção |
| Patrocínio funciona? | Não para desempenho; depende do custo por resultado | +0,008% de engajamento e +0,004% de views em 269 estratos comparáveis; 0 de 17 condições com efeito |
| Que público engaja mais? | Nenhum | 36 contextos (plataforma, formato, tema) × gênero, idade e país: 0 efeitos |
| O que não funciona? | 11 de 11 crenças de mercado | ex.: seguidores × views ρ = 0,005; vídeo vs. imagem/texto −0,03% |
| Modelos de previsão | Nenhum bate a média, e a ferramenta avisa | 14 abordagens de engajamento, previsão de views com validação temporal, chance de top 5% (0 de 12 combinações adotadas); com efeito plantado, o mesmo protocolo adota o modelo certo |
| Quem posta importa? | Não: o desempenho passado não se repete além do acaso | 8,8% dos top 10% do 1º ano continuam no top no 2º (acaso: 10%) |
| Único padrão robusto | TikTok · beauty · espanhol: 2x mais chance de top 5% em likes | 10,0% vs. 4,9%, nos dois anos; q global = 0,035 entre ~14,7 mil testes. Vai para teste, não para regra |
| Auditorias de carteira | Lacunas que valem mesmo sem efeito no engajamento | 47% dos patrocínios com disclosure implícito; só 2,3% com #ad no texto; 60% fora do nicho do creator; só 22% dos posts no idioma do mercado |

**O que a IA diria × o que os dados mostram** (gerado por `strategy.claims_vs_data`):

| "Insight" típico | O que os dados mostram | Veredito |
|---|---|---|
| "Bilibili · vídeo · lifestyle · micro é o segmento que mais engaja: concentre o investimento nele." | índice 100,5 (média = 100), n = 109, p = 0,02, q = 0,88 | maior diferença bruta entre 450 segmentos; some após a correção |
| "Creators maiores entregam mais alcance: priorize macro e mega." | correlação seguidores × views = 0,005 (q = 0,53) | não se sustenta |
| "Vídeo é o formato que mais engaja: migre o mix para vídeo." | −0,03% de engajamento (q = 0,53) | não se sustenta |
| "Publique à noite (18–24h), quando o alcance é maior." | −0,01% de views (q = 0,53) | não se sustenta |
| TikTok · beauty · espanhol: mais posts no top 5% de likes | 10,0% vs. 4,9% (2,0x), nos 2 anos; q global = 0,035 entre 14.763 testes | **único que passou no filtro:** vai para teste A/B |

Detalhe completo, gerado por código: [`docs/respostas.md`](docs/respostas.md) · achados por tema: [`knowledge/`](knowledge/) · 14 notebooks executados: [`solution/notebooks/`](solution/notebooks/).

### Recomendações

**Esta semana. Valem também com os dados reais:**
1. Contratar creators **por resultado** (CPM/CPE), não por post: a diferença de ~134x por mil views entre mega e nano independe do valor do cachê. Medida por seguidor, o nano parece ~138x melhor (0,368 × 0,0027); é efeito da conta, porque as views são iguais em todos os portes (~10.100).
2. **Rótulo de publicidade verificável no texto** (#publi/#ad): reduz o risco regulatório (47% em risco alto) sem custo de engajamento.
3. **Grupo de comparação orgânico em todo patrocínio**, para medir o ganho real.
4. **Não pagar a mais pelo histórico de desempenho do creator** e tirar "melhor horário" e "hashtags ideais" do checklist.

**Recalcular com os preços reais antes de aplicar:**

5. Teto de ~10 mil seguidores para contratos de preço fixo (varia de 1 mil a 40 mil conforme as premissas).
6. Formato padrão pelo custo real de produção.

**Fila de testes** (com o custo de confirmar cada hipótese):
1. TikTok · beauty · espanhol × inglês: A/B com 1.430 posts por grupo; sucesso = taxa de top 5% em likes ≥ 7,5% no grupo espanhol (resto do TikTok: 4,9%), p < 0,05. Brief completo (formato, creator, público, horário, duração) no [resumo](docs/resumo-executivo.md#o-que-testar-e-quanto-custa-confirmar).
2. Horário no YouTube: acompanhar no histórico (um A/B exigiria ~17 mil posts por grupo).
3. Uplift do patrocínio: A/B com os contratos da empresa.

**Ferramenta recorrente:** trocar o CSV pelos dados da empresa e rodar `social-web --rebuild`. Vereditos, recomendações, fila de testes e simulador se recalculam.

### Limitações

- **A base é simulada** (Kaggle: "views simulated via a Poisson distribution"). Os achados descrevem esta base. O que se transfere são o método e a ferramenta, validados com efeitos plantados.
- **Não há preços.** Custos e teto de seguidores vêm de premissas editáveis (`strategy.py`), mostradas com tabela de sensibilidade. Os valores em US$ são ordem de grandeza, não contábeis.
- **Sem posts que fracassaram:** 0 posts com zero views, likes, compartilhamentos ou comentários (mínimo de 1.354 likes; views de 9.676 a 10.551). A base não mostra o que fracassa.
- **`post_date` sem fuso:** os horários assumem um relógio único. `content_length` mistura segundos e palavras e só é analisado por formato.
- **`creator_id` instável** (~10 nomes e contagens de seguidores por id): a frequência de postagem não pôde ser medida por creator.
- Os rótulos de disclosure da base não aparecem no texto dos posts: a auditoria mede a composição declarada, não a prática real.

### Como rodar

**Com Docker (recomendado):** um comando monta e sobe tudo. A imagem fixa o Python (3.14.3) e todos os pacotes na versão exata do ambiente testado (`requirements.lock`), confere o sha256 do CSV, treina os modelos no build e **falha o build se qualquer número ou texto do site, ou a resposta do simulador para 4 posts de teste, divergir da referência** (`solution/reproducibility/reference.json`).

```bash
cd submissions/rafael
docker build -t g4-social . && docker run --rm -p 8000:8000 g4-social   # site em http://127.0.0.1:8000 (build ~10 min)
```
- Sem o CSV em `data/raw/`, passe a credencial do Kaggle no build: `docker build --secret id=kaggle,src=$HOME/.kaggle/kaggle.json -t g4-social .` (o token não fica gravado na imagem).
- Checagem completa (retreina do zero e roda os testes dentro do container): `docker run --rm g4-social python solution/reproducibility/verify.py --retrain --tests`.
- O container roda sem root e tem healthcheck em `/api/health`. Também funciona com `podman`.

**Sem Docker** (Python 3.14 e credencial do Kaggle em `~/.kaggle/kaggle.json`):

```bash
cd submissions/rafael
python3.14 -m venv .venv && .venv/bin/pip install -r requirements.lock && .venv/bin/pip install -e .
bash solution/scripts/get_data.sh                                          # baixa o CSV e confere o sha256
.venv/bin/python -m pytest -q                                              # testes (~2 min)
.venv/bin/python solution/reproducibility/verify.py                        # versões, dados, modelos e resultados = referência
.venv/bin/python solution/cli/answer_questions.py --out docs/respostas.md  # relatório das 4 perguntas + estratégia
.venv/bin/social-web                                                       # site em http://127.0.0.1:8000 (1ª vez treina tudo, ~5 min)
```
Atalhos no [`Makefile`](Makefile): `setup data test verify verify-full report notebooks site docker-build docker-run docker-verify`.

### Organização

```
submissions/rafael/
├── README.md · DEVELOPMENT_PROCESS.md     visão geral · decisões e alternativas descartadas
├── Dockerfile · Makefile                  ambiente encapsulado · atalhos
├── pyproject.toml                         pacote Python (social_insights, social_web)
├── requirements.txt · requirements.lock   dependências diretas · todas as versões exatas (inclui as indiretas)
├── solution/                              tudo que é código (detalhes em solution/README.md)
│   ├── src/social_insights/               análises, modelos, estratégia e auditorias
│   ├── src/social_web/                    site FastAPI (páginas, painel, simulador, API em /docs)
│   ├── cli/                               relatório e previsões pela linha de comando
│   ├── scripts/                           download do dataset com checagem de sha256
│   ├── reproducibility/                   verificador + resultados de referência
│   ├── notebooks/                         14 notebooks executados (gerados por notebooks/build/)
│   ├── tests/                             testes com efeitos plantados
│   └── models/                            modelos treinados (gerados, fora do git)
├── data/raw/                              CSV do Kaggle (baixado, fora do git)
├── docs/                                  resumo executivo, relatório completo e figuras
├── knowledge/                             achados por tema e notas de ambiente
├── process-log/                           uso de IA: narrativa, prompts e sondas
├── evidencias/                            conversas com IA exportadas (3 sessões, completas)
├── review/                                revisão crítica da entrega
└── instructions/                          regras seguidas na entrega
```

---

## Process Log — Como usei IA

Narrativa completa, tabela de erros da IA e evidências: [`process-log/README.md`](process-log/README.md). Conversas completas com a IA: [`evidencias/`](evidencias/).

### Ferramentas usadas

| Ferramenta | Para que usou |
|---|---|
| Claude Code (Opus) | Execução de ponta a ponta: dados, EDA, estatística, modelos, pacote + testes, site, documentação |
| Sessões paralelas do Claude Code | Checagem independente: descrição do dataset × conclusões; revisão crítica × requisitos |
| Outra IA (chat) | Plano de ação de análise ([`knowledge/action-plan.md`](knowledge/action-plan.md)), executado e criticado |
| Jupyter + pytest | Verificação: notebooks executados e 116 testes |

### Workflow

1. Regras e critérios de valor em `instructions/`, antes de qualquer código.
2. EDA para eu entender os dados → descoberta de que as métricas são sorteadas.
3. Análises gerais e por plataforma (clusterização, NLP, público), sempre com correção e controle positivo.
4. Plano de outra IA (correlações, RF/XGBoost/CatBoost, SHAP), com SHAP contra alvo embaralhado.
5. Perguntas e estratégia viraram funções; modelos (14 abordagens); efeito mínimo detectável; varredura de todos os atributos.
6. Previsão antes de postar, duração × views, bolsões com nível de evidência, chance de top 5%.
7. Site com servidor e iterações de UX (resumo primeiro, painel simples, simulador, identidade G4).
8. Duas checagens independentes → auditorias e correção de contradições.

São 33 prompts com conteúdo ([`process-log/prompts.md`](process-log/prompts.md)), 3 sessões e 39 decisões registradas ([`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md)).

### Onde a IA errou e como corrigi

- **Hopkins indicava "há clusters"**, mas dá ~0,9 até em ruído gaussiano → troquei por um nulo por permutação.
- **Ranking de SHAP e R² de treino ~0,1** pareciam "fatores" → comparação com o alvo embaralhado e com a validação (R² ≤ 0).
- **22 segmentos com p < 0,05 viraram candidatos a insight**, exatamente o esperado por acaso em 450 testes → FDR obrigatório.
- **"Disclosure explícito = compliance sem perda"**, mas o rótulo nem aparece no texto do post → auditoria e regra de rótulo verificável.
- **Faixas de duração misturando segundos e palavras** → análise por formato, na unidade certa.
- **"Priorizar TikTok espanhol" e "teto de 10 mil seguidores / US$ 109 mi" como fatos** → a revisão crítica mostrou que contradiziam a tese e vinham das premissas → fila de testes, sensibilidade e classes "robusta × depende de premissa".

### O que eu adicionei que a IA sozinha não faria

- Exigir entender os dados antes da estratégia. Isso revelou que a base é simulada e definiu a entrega.
- Hipóteses de negócio: separar por plataforma, "quem posta importa?", "o que se sabe antes de postar?", chance de virar destaque por formato.
- Contestar a IA com o gráfico ("mais picos entre 20–150 s"), o que forçou a distinguir contagem de taxa.
- Pedir que variações virassem insights, mas com nível de evidência. O resultado foi uma fila de testes em vez de "nada a reportar".
- Checagens em sessões separadas, que pegaram os erros mais graves.
- Produto para leigos, com resumo primeiro; horário tratado como relógio único em vez de inventar fuso.

---

## Evidências

- [ ] Screenshots das conversas com IA
- [ ] Screen recording do workflow
- [x] Chat exports — pasta [`evidencias/`](evidencias/): conversas completas das 3 sessões (principal + 2 checagens), com índice; prompts de todas as sessões em [`process-log/prompts.md`](process-log/prompts.md)
- [x] Git history — branch `submission/rafael` (commits pequenos por etapa)
- [x] Outro: [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md) (decisões e alternativas descartadas), [`review/critica-entrega.md`](review/critica-entrega.md), notebooks comentados, scripts de sondagem em `process-log/`

---

_Submissão enviada em: 19/10/2026_
