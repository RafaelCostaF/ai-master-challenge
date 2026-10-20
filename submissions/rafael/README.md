# Submissão — Rafael — Challenge 004

## Sobre mim

- **Nome:** Rafael
- **LinkedIn:** https://www.linkedin.com/in/rafaelcostaf/
- **Challenge escolhido:** 004 — Estratégia Social Media

---

## Executive Summary

Estruturei o projeto em etapas, organizando o repositório, preparando o dataset e definindo instruções específicas para análise, modelagem, validação e revisão independente dos resultados. A análise mostrou que o dataset é sintético e que as métricas de engajamento são essencialmente independentes das características dos posts, fazendo com que diferenças entre formatos, plataformas, creators e patrocínio sejam, em sua maioria, ruído. A recomendação principal é a **contratação de creators por resultado, não por post** (ex.: pagar creators por mil views ou por interação, medir todo patrocínio contra um grupo orgânico e testar antes de mudar a combinação.)

**Leitura de 5 minutos:** [`docs/resumo-executivo.md`](docs/resumo-executivo.md)

---

## Solução

### Abordagem

1. **Preparação e organização do projeto.** O trabalho começou pelo download do dataset, configuração do ambiente e criação das instruções gerais do projeto, incluindo padrões de código, critérios de entrega e regras de reprodutibilidade. Também foi criada uma pasta de `knowledge` para centralizar os achados ao longo da análise e um registro específico para decisões tomadas em pontos críticos, evitando que mudanças de direção ficassem apenas implícitas no histórico de desenvolvimento.

2. **Análise orientada por evidência.** Antes de buscar conclusões, a EDA foi usada para entender a natureza dos dados. Como o dataset se mostrou sintético e com métricas de desempenho praticamente independentes das características dos posts, a abordagem passou a priorizar a separação entre sinal e ruído, evitando transformar pequenas variações aleatórias em recomendações de negócio.

3. **Revisões independentes e agentes não contaminados.** Parte importante do processo foi manter agentes separados do desenvolvimento principal para revisar a documentação, verificar os achados sobre os dados e confrontar as conclusões com a descrição original do dataset e com os requisitos do desafio. Esses agentes recebiam apenas o material necessário para a revisão, reduzindo o risco de simplesmente reproduzir as interpretações já formadas durante a análise.

4. **Rigor estatístico e validação.** As conclusões foram submetidas a múltiplas verificações: correção para muitos testes, análises estratificadas, efeito mínimo detectável, validação temporal e controles positivos com sinais sintéticos conhecidos. Com isso, cada recomendação precisava estar ligada a um resultado reproduzível e suficientemente sustentado pelos dados.

5. **Transformação da análise em produto.** Depois da etapa analítica, os resultados foram organizados em uma aplicação web, com identidade visual inspirada na G4 Company e estrutura voltada à navegação por perguntas de negócio, recomendações, descobertas e painéis de análise.

6. **Simplificação da experiência.** A primeira versão da aplicação ainda refletia o volume de informações produzido durante a análise. Por isso, o site passou por uma nova rodada de revisão visual e de conteúdo, com remoção de textos e métricas excessivas, reorganização dos painéis de BI e priorização das informações realmente úteis para o time de marketing. O objetivo foi transformar uma análise tecnicamente extensa em uma ferramenta simples, direta e acionável, evitando o excesso de conteúdo normalmente gerado por IA.

7. **Revisão final e entrega.** A última etapa foi uma revisão completa da solução, cobrindo consistência entre dados, análises e recomendações, qualidade da documentação, organização da aplicação e aderência aos requisitos do desafio, antes da preparação da entrega final.

### Resultados / Findings

**O que construí.** Uma ferramenta que o time usa sem analista e que se recalcula com os dados reais da empresa (`social-web --rebuild`):

<p>
<img src="docs/screenshots/inicio.png" width="32%" alt="Resumo: as 4 respostas, os destaques e o que fazer agora">
<img src="docs/screenshots/explorar.png" width="32%" alt="Explorar dados: painel com filtros e selo de diferença real">
<img src="docs/screenshots/simular.png" width="32%" alt="Simular post: chance de top 5% antes de publicar e sugestão de melhoria">
</p>

| Entrega | Valor para o time | Onde |
|---|---|---|
| **Resumo** | As 4 respostas, os 2 destaques e o que começar, parar e testar, em uma tela | `/` |
| **Explorar dados** | Painel com filtros que marca só as diferenças reais (corrigidas para muitos testes), para ninguém decidir com base em ruído | `/explorar` |
| **Simular post** | Chance de top 5% antes de publicar e uma versão próxima mais forte, com selo de evidência | `/simular` |
| **Auditorias e estratégia** | Riscos de carteira (disclosure, nicho, idioma), sensibilidade do teto de seguidores e fila de testes com o nº de posts por grupo | `/auditorias`, `/estrategia` |
| **Reprodutibilidade** | Docker que falha se qualquer número divergir da referência; 131 testes com efeitos plantados | [Como rodar](#como-rodar) |

**O que encontrei** (52.214 posts, 5 plataformas, mai/2023 → mai/2025):

| Pergunta | Resposta | Número-chave |
|---|---|---|
| O que gera engajamento? | Nenhum fator que o time controla | 450 combinações testadas: 22 com p < 0,05 (o esperado por acaso), 0 após correção; maior diferença 0,07% |
| Patrocínio funciona? | Não para desempenho: a decisão é de preço | +0,008% de engajamento em 269 estratos comparáveis (p = 0,72); mega custa **~134x mais por mil views** que nano com cachê por seguidor |
| Que público engaja mais? | Nenhum | 36 contextos × gênero, idade e país: 0 efeitos |
| O que não funciona? | 11 de 11 crenças de mercado | seguidores × views ρ = 0,005; vídeo vs. outros −0,03% |
| Vale pagar por "creator campeão"? | Não | 8,8% dos top 10% do 1º ano continuam no top no 2º (acaso: 10%) |
| Algum padrão real? | Um: TikTok · beauty · espanhol | 10,0% vs. 4,9% de chance de top 5% em likes, nos 2 anos; q = 0,035 entre ~14,7 mil testes → teste A/B com 1.430 posts por grupo |
| Riscos de carteira | Valem mesmo sem efeito no engajamento | 47% dos patrocínios com disclosure implícito (só 2,3% com #ad no texto); 60% fora do nicho do creator; só 22% dos posts no idioma do mercado |

"Não faz diferença" é resultado, não falta de dados: os testes enxergam efeitos a partir de 0,3%, e efeitos de 2–5% plantados na base são encontrados.

<details>
<summary><b>O que uma IA diria × o que os dados mostram</b> (gerado por <code>strategy.claims_vs_data</code>)</summary>

| "Insight" típico | O que os dados mostram | Veredito |
|---|---|---|
| "Bilibili · vídeo · lifestyle · micro é o segmento que mais engaja: concentre o investimento nele." | índice 100,5 (média = 100), n = 109, p = 0,02, q = 0,88 | maior diferença bruta entre 450 segmentos; some após a correção |
| "Creators maiores entregam mais alcance: priorize macro e mega." | correlação seguidores × views = 0,005 (q = 0,53) | não se sustenta |
| "Vídeo é o formato que mais engaja: migre o mix para vídeo." | −0,03% de engajamento (q = 0,53) | não se sustenta |
| "Publique à noite (18–24h), quando o alcance é maior." | −0,01% de views (q = 0,53) | não se sustenta |
| TikTok · beauty · espanhol: mais posts no top 5% de likes | 10,0% vs. 4,9% (2,0x), nos 2 anos; q global = 0,035 entre 14.763 testes | **único que passou no filtro:** vai para teste A/B |

</details>

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
| Jupyter + pytest | Verificação: notebooks executados e 131 testes |

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
