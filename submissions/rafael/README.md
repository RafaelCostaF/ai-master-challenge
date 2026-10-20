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

Narrativa completa: [`process-log/README.md`](process-log/README.md) · conversas: [`evidencias/`](evidencias/).

### Ferramentas usadas

| Ferramenta | Para que usou |
|---|---|
| Claude Code (Opus) | Toda a execução: dados, estatística, modelos, site e documentação |
| Sessões paralelas do Claude Code | Revisão independente dos achados e da entrega |
| ChatGPT | Plano de análise de dados diferente do Claude, com o objetivo de tentar identificar lacunas na proposta de análise do Claude ([`knowledge/action-plan.md`](knowledge/action-plan.md)) |
| Jupyter | Análise manual dos dados |
| pytest | Testes automatizados para <preencher> |


### Workflow

1. Criação das regras gerais em `instructions/` antes de qualquer código (instruções de código, como submeter, regras do repositório, valores importantes para a entrega, etc).
2. EDA <preencha melhor>.
3. Análises gerais e por plataforma. + processo de auditoria com sessão limpa, para validar as análises (agir como crítico para validar e também buscar novos insights)
5. Adaptação das perguntas do desafio e transformação destas em funções: os textos se recalculam com novos dados. <explique brevemente o motivo pelo qual isso é necessário, vendendo o peixe>
6. Criação do site
7. Limpeza de conteúdo textual excessivo
8. Melhorias em UI e UX para facilitar o uso pela equipe de marketing
9. Duas revisões independentes → auditorias e correção de contradições.

33 prompts ([`process-log/prompts.md`](process-log/prompts.md)), 3 sessões e 39 decisões registradas ([`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md)).

### Onde a IA errou e como corrigi

- **Disse que havia grupos naturais de posts**, com uma métrica que dá o mesmo resultado em ruído → troquei por um teste contra dados embaralhados.
- **Apresentou "fatores importantes" do modelo** que também apareciam com dados embaralhados → toda importância agora é mostrada ao lado desse controle.
- **Tratou 22 resultados "significativos" como insights**, exatamente o esperado por acaso em 450 testes → correção para muitos testes obrigatória.
- **Disse que o disclosure explícito estava em dia**, mas o rótulo nem aparece no texto → auditoria de disclosure.
- **Misturou segundos e palavras na mesma faixa de duração** → análise por formato.
- **Recomendou "priorizar TikTok em espanhol" e o limite de 10 mil seguidores como fatos** → viraram teste e cálculo dependente de preço.

### O que eu adicionei que a IA sozinha não faria

- Exigi entender os dados antes da estratégia: foi assim que descobri que a base é simulada. Execução de diversas sessões com abordagens diferentes e não contaminadas para a análise do dataset.
- Levantei as hipóteses de negócio: análise por plataforma, "quem posta importa?", "o que se sabe antes de postar?".
- Contestação constante das afirmações sobre os dados, muitas vezes sensacionalistas ou sem valor real para o negócio.
- Pedi que as variações virassem insights com nível de evidência, o que gerou a fila de testes.
- Usei revisores independentes (sempre com dupla checagem sobre os dados e as análises), que pegaram os erros mais graves.
- Transformação das informações obtidas em formato executivo e simples para a equipe de marketing

---

## Evidências

- [ ] Screenshots das conversas com IA
- [ ] Screen recording do workflow
- [x] Chat exports — [`evidencias/`](evidencias/) (3 sessões completas) e prompts em [`process-log/prompts.md`](process-log/prompts.md)
- [x] Git history — branch `submission/rafael`
- [x] Outro: screenshots do site em [`docs/screenshots/`](docs/screenshots/), [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md) e [`review/critica-entrega.md`](review/critica-entrega.md)

---

_Submissão enviada em: 19/10/2026_
