# Estratégia recomendada — decisões e como usar

Fonte: `solution/src/social_insights/strategy.py` · relatório: `docs/respostas.md` (seções 1–4 de estratégia) · gerado em 2026-10-18 sobre 52.214 posts.
Complementa `questions-answers.md` (diagnóstico) com as **decisões**. Mesmo formato para o site: manchete, números-chave, ações, premissas.

> **Regra de decisão (vale para tudo):** opções que **não são significativamente piores** que a melhor são "equivalentes" (teste de Welch + correção FDR). **Entre equivalentes, vence a mais barata.** Com dados reais, se uma opção for de fato melhor, ela vence mesmo sendo cara (coberto por teste).

> **Premissas de custo** (o dataset não tem preços, e todas são parâmetros configuráveis):
> custo de patrocínio = US$ 10 por mil seguidores por post · produção própria por post: texto US$ 50, imagem US$ 100, misto US$ 150, vídeo US$ 300 · CPM-alvo US$ 10 · CPE-alvo US$ 0,05.

---

## 1. Onde concentrar esforço?

- **Manchete:** nenhuma plataforma, formato ou faixa de creator entrega mais, então a escolha é pelo menor custo por resultado.

| Decisão | Escolha | Evidência |
|---|---|---|
| Plataforma | Nenhuma vence: concentrar em 1–2 por custo operacional e por onde está o cliente-alvo | diferenças ≤ 0,01% em views e ≤ 0,05% em engajamento, todas equivalentes |
| Formato | **Texto** (pela premissa de custo) | 4 formatos equivalentes (diferença ≤ 0,06%); texto custa 6x menos que vídeo |
| Faixa de creator | **Nano (<10K)** | 5 faixas equivalentes; custo mediano US$ 56 (nano) vs. US$ 7.508 (mega) |
| Frequência | Limite = capacidade de produção | ~14 posts/dia por plataforma; dias de alto volume não têm pior desempenho por post (0 de 5 plataformas com saturação) |

- **Ações:** fixar o mix padrão no formato mais barato equivalente; priorizar nano; focar 1–2 plataformas; aumentar a frequência e monitorar a saturação mensalmente.
- **Atenção para o site:** "texto" é consequência da premissa de custo, não de desempenho. Com custos reais, o formato recomendado pode mudar.

## 2. Política de patrocínio

- **Manchete:** patrocinar **não** compra desempenho. Patrocine só quando o post se pagar como mídia: **até ~10 mil seguidores**.
- **Números-chave:**
  - uplift do patrocínio: **+0,008%** de engajamento e **+0,004%** de alcance (nulos; 269 estratos comparáveis)
  - **0 de 17** condições com efeito (plataforma, porte, formato, categoria)
  - **threshold: ~10.050 seguidores** (CPM ≤ US$ 10 e CPE ≤ US$ 0,05 com ~10.100 views e ~2.010 interações por post)
  - hoje **só 1%** dos posts patrocinados estão abaixo do threshold
- **Ponto de equilíbrio por tamanho de creator:**

| Seguidores | Custo/post | CPM | CPE | Vale? |
|---|---|---|---|---|
| 5 mil | US$ 50 | US$ 4,95 | US$ 0,02 | ✓ |
| 10 mil | US$ 100 | US$ 9,90 | US$ 0,05 | ✓ |
| 25 mil | US$ 250 | US$ 24,75 | US$ 0,12 | ✗ |
| 100 mil | US$ 1.000 | US$ 99 | US$ 0,50 | ✗ |
| 1 milhão | US$ 10.000 | US$ 990 | US$ 4,98 | ✗ |

- **Threshold de engajamento:** um creator de 25 mil precisaria de engajamento de ~50% (hoje é 20%) para valer o preço, e um de 100 mil precisaria de ~198%, o que é impossível. O engajamento histórico **não** é critério, porque não diferencia creators.
- **Perfil:** nano, em qualquer plataforma ou categoria.
- **Ações:**
  1. Teto de contratação em ~10 mil seguidores (ou pagamento por desempenho acima disso).
  2. Contratos por CPM/CPE garantido, não por post fixo.
  3. Disclosure sempre explícito (sem perda de engajamento, sem risco regulatório).
  4. Todo patrocínio novo com grupo de controle orgânico pareado.

## 3. O que parar de fazer

| Investimento de baixo retorno | Tamanho | Excedente estimado |
|---|---|---|
| Patrocínio acima de ~10 mil seguidores | 22.122 posts (99% dos patrocinados) | **~US$ 109 mi** sobre o preço justo (**98%** do gasto implícito com patrocínio) |
| Formatos mais caros sem ganho de engajamento | 47.016 posts | **~US$ 8,9 mi** de produção |
| Otimizações sem efeito: horário, nº de hashtags, legenda longa, conteúdo curto, fim de semana… | 11 práticas testadas | tempo do time |

- **Ações:** congelar renovações acima do threshold até renegociar; migrar a produção padrão para o formato mais barato equivalente; tirar "melhor horário", "hashtags ideais" e "legenda longa" do checklist.
- **Atenção:** os valores em US$ são **implícitos** (premissas × 2 anos de posts). No site, apresentar como ordem de grandeza e em %, não como valor contábil.

## 4. Quick wins (esta semana)

| # | Ação | Esforço | Impacto | Dono |
|---|---|---|---|---|
| 1 | Teto de ~10 mil seguidores para novos contratos | baixo | evita ~98% do excedente | Head de Marketing / Compras |
| 2 | Renegociar contratos ativos acima do teto para CPM/CPE garantido | médio | custo por resultado no nível do mercado | Parcerias |
| 3 | Disclosure explícito como padrão | baixo | compliance sem perda de engajamento | Social media |
| 4 | Mix de produção padrão no formato mais barato equivalente | baixo | ~US$ 8,9 mi de economia potencial | Conteúdo |
| 5 | Retirar "melhor horário" e "hashtags ideais" do checklist | baixo | horas do time liberadas | Social media |
| 6 | Rodar `answer_questions.py` e o 1º teste A/B (patrocinado vs. orgânico pareado) | médio | medir o uplift real com dados da empresa | AI Master / Analytics |

Resumo: 3 ações cortam custo, 1 reduz risco, 1 libera tempo e 1 cria a medição contínua. Nenhuma exige contratação ou ferramenta nova.

---

## Como utilizar

### Relatório (diagnóstico + estratégia)
```bash
cd submissions/rafael
.venv/bin/python solution/answer_questions.py --out docs/respostas.md
```

### Em Python
```python
import sys; sys.path.insert(0, "solution/src")
from social_insights import data, strategy

df = data.load_posts()
rec = strategy.sponsorship_policy(df, cost_per_follower=0.008, target_cpm=12, target_cpe=0.04)  # premissas próprias
rec.verdict    # decisão executiva (gerada dos números)
rec.actions    # list[str] — próximos passos
rec.evidence   # DataFrame principal; rec.details: tabelas de apoio
rec.to_markdown()
strategy.recommend_all(df)  # as 4 decisões
```

| Função | Pergunta | Retorna |
|---|---|---|
| `where_to_focus(df, production_cost, cost_per_follower)` | Onde concentrar esforço | plataforma, formato, faixa de creator, saturação de frequência |
| `sponsorship_policy(df, cost_per_follower, target_cpm, target_cpe)` | Política de patrocínio | decisão, threshold, ponto de equilíbrio, perfil |
| `stop_doing(df, ...)` | O que parar | investimentos de baixo retorno com excedente estimado |
| `quick_wins(df, ...)` | Quick wins | ações com esforço, impacto e dono |
| `break_even(df, ...)` | (apoio) | teto de seguidores e engajamento necessário por porte |
| `frequency_effect(df, metric)` | (apoio) | saturação por plataforma (volume diário × desempenho por post) |
| `equivalence_table(df, by, metric)` | (apoio) | opções equivalentes à melhor |

### Parâmetros (premissas)
| Constante | Padrão | Trocar por |
|---|---|---|
| `COST_PER_FOLLOWER` | 0,01 | preço real por seguidor (ou tabela de cachês) |
| `PRODUCTION_COST` | texto 50 · imagem 100 · misto 150 · vídeo 300 | custo interno real por formato |
| `TARGET_CPM` | 10 | CPM máximo aceito (benchmark de mídia paga) |
| `TARGET_CPE` | 0,05 | custo máximo por interação |

### Qualidade
`solution/tests/test_strategy.py` testa a fórmula do threshold e a regra "mais barato entre equivalentes". Também testa, com efeitos plantados, que o formato melhor vence mesmo sendo caro, que a saturação é detectada e que o patrocínio vira "SIM" quando há efeito.
