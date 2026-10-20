# Submissão — Rafael — Challenge 004

## Sobre mim

- **Nome:** Rafael
- **LinkedIn:** https://www.linkedin.com/in/rafaelcostaf/
- **Challenge escolhido:** 004 — Estratégia Social Media

---

## Executive Summary

Estruturei o projeto em etapas, organizando o repositório, preparando o dataset e definindo instruções específicas para análise, modelagem, validação e revisão independente dos resultados. A análise mostrou que o dataset é sintético e que as métricas de engajamento são essencialmente independentes das características dos posts, fazendo com que diferenças entre formatos, plataformas, creators e patrocínio sejam, em sua maioria, ruído. A recomendação principal é a **contratação de creators por resultado, não por post** (ex.: pagar creators por mil views ou por interação, medir todo patrocínio contra um grupo orgânico e testar antes de mudar a combinação.)

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

**O que construí:** um site que o time usa sem analista. Com os dados da empresa, basta trocar o CSV e rodar `social-web --rebuild`.

<p>
<img src="docs/screenshots/inicio.png" width="32%" alt="Resumo: as 4 respostas, os destaques e o que fazer agora">
<img src="docs/screenshots/explorar.png" width="32%" alt="Explorar dados: painel com filtros e selo de diferença real">
<img src="docs/screenshots/simular.png" width="32%" alt="Simular post: chance de top 5% antes de publicar e sugestão de melhoria">
</p>

Depois de [rodar](#como-rodar), abra http://127.0.0.1:8000. O menu do topo tem 4 páginas principais e o menu "Aprofundar", com os detalhes.

| Página | O que mostra | Quando usar |
|---|---|---|
| **Resumo** | As respostas às 4 perguntas do desafio, os 2 padrões que merecem teste e uma lista do que começar, parar e testar | Para entender o resultado em 2 minutos |
| **Explorar dados** | Painel com filtros (plataforma, formato, tema, período…). Gráficos mostram quanto cada grupo fica acima ou abaixo da média, e um selo indica se a diferença é real ou acaso | Para tirar uma dúvida própria, ex.: "vídeo vai melhor no TikTok?" |
| **Simular post** | Você descreve um post (plataforma, formato, tema, idioma, dia, hora, creator). A página mostra a chance de ele ficar entre os 5% com mais views, likes ou comentários e sugere uma mudança que aumentaria essa chance | Antes de publicar ou aprovar um post |
| **Agrupamento de audiência** | Junta perfis de público (idade × gênero × país) que consomem conteúdo parecido e mostra o que cada grupo consome a mais. Um selo diz se os grupos são confiáveis o bastante para segmentar campanhas (nesta base, não são) | Para definir segmentos de público |
| **Aprofundar** → 4 perguntas, Estratégia, Descobertas, Auditorias, Como chegamos lá | Respostas com gráficos, as ações com o motivo de cada uma, os grupos fora da média com nível de evidência, os riscos da carteira (rótulo de publicidade, nicho, idioma) e o método | Para conferir o porquê de uma recomendação |

Cada número do site é reproduzível: o Docker falha se algum valor divergir da referência, e há 131 testes automatizados.

**O que encontrei** (52.214 posts, 5 plataformas, mai/2023 a mai/2025):

| Pergunta | Resposta | Dado |
|---|---|---|
| O que gera engajamento? | Nada que o time controla | 450 combinações testadas, nenhuma com efeito real; maior diferença: 0,07% |
| Patrocínio funciona? | Não melhora o desempenho; a decisão é de preço | Patrocinado engaja igual ao orgânico (+0,008%). Pagando por seguidor, o creator mega custa **~134x mais por mil views** que o nano |
| Que público engaja mais? | Nenhum | Gênero, idade e país engajam igual em 36 contextos |
| O que não funciona? | 11 de 11 crenças de mercado | Ex.: mais seguidores não trazem mais views (correlação 0,005) |
| Vale pagar a mais por creator "campeão"? | Não | Só 8,8% dos melhores do 1º ano continuaram entre os melhores no 2º (acaso: 10%) |
| Há algum padrão real? | Um, para testar | TikTok · beauty · espanhol: 10% dos posts entre os 5% com mais likes, contra 4,9% no resto, nos 2 anos |
| Riscos da carteira | Independem do engajamento | 47% dos patrocínios sem rótulo claro de publicidade; 60% fora do nicho do creator; só 22% dos posts no idioma do mercado |

<details>
<summary><b>O que uma IA diria × o que os dados mostram</b></summary>

| "Insight" típico | O que os dados mostram |
|---|---|
| "Bilibili · vídeo · lifestyle · micro engaja mais: concentre o investimento." | Foi a maior diferença entre 450 grupos (+0,5%), mas some quando se desconta o acaso |
| "Creators maiores dão mais alcance." | Seguidores e views não têm relação (correlação 0,005) |
| "Vídeo engaja mais: migre o mix." | Vídeo engaja 0,03% menos; diferença nula |
| "Publique à noite." | Views 0,01% menores; diferença nula |
| TikTok · beauty · espanhol | Único padrão que resistiu ao acaso: vai para teste A/B |

</details>

Relatório completo: [`docs/respostas.md`](docs/respostas.md) · achados por tema: [`knowledge/`](knowledge/) · notebooks: [`solution/notebooks/`](solution/notebooks/).

### Recomendações

**Fazer já (valem também com os dados reais):**
1. **Contratar creators por resultado** (por mil views ou por interação). As views não crescem com os seguidores, então pagar por seguidor encarece os creators grandes.
2. **Comparar todo patrocínio com posts orgânicos** para medir o ganho real.
3. **Não pagar a mais pelo histórico do creator** e tirar "melhor horário" e "nº ideal de hashtags" do checklist.

**Recalcular com os preços reais antes de aplicar:**

4. Limite de ~10 mil seguidores em contratos de preço fixo (entre 1 mil e 40 mil, conforme os preços).
5. Escolher o formato mais barato de produzir, já que nenhum engaja mais.

**Testar:**
1. TikTok · beauty: mesmo conteúdo em espanhol × inglês, 1.430 posts por grupo. Detalhes no [resumo](docs/resumo-executivo.md#o-que-testar-e-quanto-custa-confirmar).
2. YouTube, posts até 12h: só acompanhar, porque um teste exigiria ~17 mil posts por grupo.
3. Ganho do patrocínio: teste A/B com os contratos da empresa.

### Limitações

- **A base é simulada** (segundo o próprio Kaggle). Os achados valem para ela; o que se transfere é o método e o site.
- **Não há preços.** Valores em US$ vêm de premissas editáveis (`strategy.py`) e são só ordem de grandeza.
- **Nenhum post fracassou** (mínimo de 1.354 likes), então a base não mostra o que dá errado.
- **Datas sem fuso horário:** os horários assumem um relógio único.
- **`content_length` mistura segundos e palavras:** só é analisado por formato.
- **`creator_id` instável** (vários nomes por id): não deu para medir frequência de postagem por creator.
## Process Log — Como usei IA

Narrativa completa: [`process-log/README.md`](process-log/README.md) · prompts: [`process-log/prompts.md`](process-log/prompts.md) · conversas: [`evidencias/`](evidencias/).

A IA foi utilizada ao longo de todo o projeto, mas com funções separadas entre **execução, exploração e revisão**. O objetivo não foi apenas gerar análises, mas criar um processo em que os resultados pudessem ser questionados, reproduzidos e revisados por sessões que não carregavam as conclusões das etapas anteriores.


## Process Log — Como usei IA

Narrativa completa: [`process-log/README.md`](process-log/README.md) · prompts: [`process-log/prompts.md`](process-log/prompts.md) · conversas: [`evidencias/`](evidencias/).

Usei IA como ferramenta de execução e análise, mas mantive separadas as funções de desenvolvimento, exploração e revisão. Meu objetivo foi reduzir vieses de confirmação: quem produzia a análise não era necessariamente quem validava os resultados.

### Ferramentas usadas

| Ferramenta | Uso |
|---|---|
| **Claude Code (Opus)** | Desenvolvimento principal: dados, estatística, modelos, aplicação e documentação |
| **Sessões independentes do Claude Code** | Revisão crítica dos achados e da entrega, sem carregar o contexto completo das sessões anteriores |
| **ChatGPT** | Geração de um plano de análise independente para confrontar a estratégia inicial e identificar lacunas |
| **Jupyter** | Exploração dos dados e inspeção dos resultados |
| **pytest** | Testes automatizados das funções analíticas, controles e componentes da aplicação |

### Workflow

1. **Estruturei o projeto antes de analisar os dados.** Fiz o download do dataset, defini padrões de código, critérios de entrega e regras de reprodutibilidade em `instructions/`. Também criei `knowledge/` para consolidar achados e mantive um registro de decisões para documentar mudanças de direção relevantes.

2. **Comecei pela EDA para validar as premissas da base.** Identifiquei que o dataset era sintético e que as métricas de desempenho tinham pouca ou nenhuma relação com as características dos posts. A partir disso, deixei de procurar “insights” por força e passei a testar explicitamente se os padrões encontrados eram reais ou apenas ruído.

3. **Separei análise e revisão.** Executei análises gerais, por plataforma, creator, audiência, conteúdo e patrocínio, e usei sessões independentes para tentar refutar os resultados, encontrar erros metodológicos e buscar relações que a análise principal pudesse ter ignorado.

4. **Exigi evidência estatística antes de transformar um padrão em conclusão.** Usei correção para múltiplos testes, efeito mínimo detectável, validação temporal, análises estratificadas e controles positivos com sinais artificiais conhecidos. Isso permitiu diferenciar ausência real de efeito de falha metodológica.

5. **Transformei as perguntas do desafio em funções.** Implementei respostas e recomendações em `questions.py` e `strategy.py`, para que textos e números fossem recalculados a partir dos dados. Isso reduz inconsistência entre análise, documentação e aplicação.

6. **Organizei os resultados em uma aplicação web.** Estruturei o site para que o time de marketing pudesse consultar conclusões, explorar dados e simular cenários sem depender dos notebooks. A interface foi adaptada à identidade visual da G4 Company.

7. **Revisei a aplicação com foco no usuário final.** A primeira versão tinha excesso de texto, métricas e painéis. Reorganizei a navegação, reduzi conteúdo redundante e simplifiquei os dashboards para priorizar decisões e perguntas de negócio.

8. **Fiz uma revisão final independente.** Revalidei achados, documentação e requisitos do desafio antes da entrega e corrigi as contradições encontradas.

O processo ficou registrado em **33 prompts**, **3 sessões principais** e **39 decisões de desenvolvimento** ([`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md)).

### Onde a IA errou e como corrigi

- **Apontou clusters que não existiam.** A estatística de Hopkins deu 0,88–0,94 ("há grupos"). *Como percebi:* o teste com efeito plantado mostrou que ela dá o mesmo valor em dados sem grupos. *Correção:* comparação com dados embaralhados.
- **Ranking de SHAP lido como "fatores de engajamento"** (pedido no plano da outra IA). *Como percebi:* o R² caiu de 0,09 no treino para ~0 na validação, e o modelo com alvo embaralhado teve as mesmas importâncias. *Correção:* toda importância aparece ao lado desse controle.
- **Disse que disclosure explícito era compliance sem risco.** *Como percebi:* pedi, numa sessão separada, que a descrição do Kaggle fosse confrontada com as conclusões. Os posts marcados "disclosure em hashtags" têm #ad só em 0,23% dos casos, quase o mesmo que os orgânicos (0,21%). *Correção:* auditoria de disclosure.
- **Misturou segundos e palavras em `content_length`** ("conteúdo curto engaja mais"). *Como percebi:* na mesma sessão; a descrição diz que o campo é em segundos para vídeo e em palavras para texto. *Correção:* análise só por formato.
- **Recomendou horários fixos ("10h", "YouTube antes do meio-dia").** *Como percebi:* na mesma sessão; `post_date` não tem fuso e o público está em 8 países. *Correção:* decidi assumir um relógio único e mostrar um aviso no site.
- **Contradisse a própria tese.** Dizia que os dados eram ruído, mas mandava "priorizar beauty em espanhol no TikTok". Também apresentava o teto de 10.050 seguidores e "US$ 109 mi" como achados, quando saíam das premissas de custo. *Como percebi:* pedi uma revisão crítica contra os requisitos, também em sessão separada. *Correção:* esses casos viraram testes com tamanho de amostra ou cálculos dependentes de preço, com tabela de sensibilidade.

### Minha contribuição no processo

Minha principal contribuição foi controlar o processo de decisão, não apenas gerar análises.

- Defini que nenhuma recomendação seria aceita antes de entender a estrutura do dataset.
- Mantive achados e decisões documentados para evitar perda de contexto entre sessões.
- Formulei perguntas adicionais de negócio, como persistência de desempenho dos creators e previsibilidade antes da publicação.
- Questionei conclusões fortes quando o efeito estatístico ou o valor de negócio era baixo.
- Separei achados em **robustos**, **hipóteses para teste** e **variações compatíveis com acaso**.
- Usei agentes independentes para revisar resultados e documentação.
- Converti a análise técnica em uma ferramenta orientada a decisão para o time de marketing.
- Fiz uma etapa específica de redução do conteúdo gerado por IA, removendo texto, métricas e gráficos sem valor operacional.

---

## Evidências

- [ ] Screenshots das conversas com IA
- [ ] Screen recording do workflow
- [x] Chat exports — [`evidencias/`](evidencias/)
- [x] Prompts — [`process-log/prompts.md`](process-log/prompts.md)
- [x] Git history — branch `submission/rafael`
- [x] Registro de decisões — [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md)
- [x] Revisão independente — [`review/critica-entrega.md`](review/critica-entrega.md)
- [x] Screenshots da aplicação — [`docs/screenshots/`](docs/screenshots/)

---

_Submissão enviada em: 19/10/2026_
