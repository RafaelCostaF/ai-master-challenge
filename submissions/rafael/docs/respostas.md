# Respostas — Challenge 004

## 1. O que gera engajamento?

**Resposta:** Nenhum fator nem combinação gera engajamento diferente. 450 segmentos testados, 22 com p<0,05 cru (~22 esperados por acaso) e 0 após correção. Maior diferença entre grupos: 0.07%.

|    | dimensão         | melhor        | pior        |   diferença melhor−pior (%) |   epsilon² |   p_value |   q_value | significativo   |
|---:|:-----------------|:--------------|:------------|----------------------------:|-----------:|----------:|----------:|:----------------|
|  0 | platform         | RedNote       | Instagram   |                     0.05282 |  8.31e-05  |    0.3621 |    0.4828 | False           |
|  1 | content_type     | text          | video       |                     0.06093 |  8.395e-05 |    0.2229 |    0.4828 | False           |
|  2 | content_category | lifestyle     | tech        |                     0.03765 |  4.768e-05 |    0.288  |    0.4828 | False           |
|  3 | follower_tier    | mid (50–100K) | nano (<10K) |                     0.07206 |  3.821e-05 |    0.7366 |    0.7366 | False           |

### Segmentos com maior índice (aparente)
|    | segmento                                      | dimensões                                                  |   n |   índice |   p_value |   q_value | significativo   |
|---:|:----------------------------------------------|:-----------------------------------------------------------|----:|---------:|----------:|----------:|:----------------|
|  0 | Bilibili · video · lifestyle · micro (10–50K) | platform × content_type × content_category × follower_tier | 109 |    100.5 |  0.02389  |    0.8825 | False           |
|  1 | Bilibili · video · beauty · micro (10–50K)    | platform × content_type × content_category × follower_tier | 107 |    100.5 |  0.06001  |    0.8825 | False           |
|  2 | Bilibili · video · micro (10–50K)             | platform × content_type × follower_tier                    | 272 |    100.5 |  0.00419  |    0.8038 | False           |
|  3 | Instagram · text · beauty · macro (100–500K)  | platform × content_type × content_category × follower_tier | 151 |    100.4 |  0.02517  |    0.8825 | False           |
|  4 | TikTok · video · beauty · mid (50–100K)       | platform × content_type × content_category × follower_tier | 120 |    100.4 |  0.09012  |    0.8825 | False           |
|  5 | TikTok · text · lifestyle · mega (500K+)      | platform × content_type × content_category × follower_tier | 202 |    100.3 |  0.05212  |    0.8825 | False           |
|  6 | TikTok · mixed · beauty · mega (500K+)        | platform × content_type × content_category × follower_tier | 196 |    100.3 |  0.03824  |    0.8825 | False           |
|  7 | RedNote · image · lifestyle · mega (500K+)    | platform × content_type × content_category × follower_tier | 449 |    100.3 |  0.003464 |    0.8038 | False           |
|  8 | Bilibili · text · beauty · macro (100–500K)   | platform × content_type × content_category × follower_tier | 197 |    100.3 |  0.06785  |    0.8825 | False           |
|  9 | RedNote · text · beauty · macro (100–500K)    | platform × content_type × content_category × follower_tier | 141 |    100.3 |  0.1119   |    0.8825 | False           |

### Segmentos significativos
| segmento   | dimensões   | n   | índice   | p_value   | q_value   | significativo   |
|------------|-------------|-----|----------|-----------|-----------|-----------------|

---

## 2. Patrocínio funciona?

**Resposta:** Não: no mesmo estrato (plataforma × formato × categoria × porte), patrocinado vs. orgânico = +0.008% de engajamento e +0.004% de alcance (p=0.72 / 0.63). 0 de 17 condições têm efeito. Como as views não crescem com os seguidores, o custo por mil views (CPM implícito) cresce com o porte: nano (<10K) US$ 5.55 vs. mega (500K+) US$ 744 (premissa: US$ 10 por mil seguidores). Se patrocinar, use creators pequenos e negocie por resultado.

|                                |   diferença |   IC95 inf |   IC95 sup |   diferença (%) |   p_value |   estratos |   q_value |
|:-------------------------------|------------:|-----------:|-----------:|----------------:|----------:|-----------:|----------:|
| eng_rate_views — estratificado |   1.56e-05  | -6.846e-05 |  9.965e-05 |       0.007836  |    0.7161 |        269 |    0.9725 |
| views — estratificado          |   0.4213    | -1.31      |  2.152     |       0.004171  |    0.6334 |        269 |    0.9725 |
| likes — estratificado          |   0.01182   | -0.6593    |  0.683     |       0.0007824 |    0.9725 |        269 |    0.9725 |
| comments_count — estratificado |   0.06128   | -0.1821    |  0.3047    |       0.03064   |    0.6217 |        269 |    0.9725 |
| eng_rate_views — regressão     |  -1.091e-05 | -9.551e-05 |  7.37e-05  |     nan         |    0.8005 |        nan |    0.9725 |

### Em que condições? (uplift do patrocínio por condição)
|    | condição                         |   uplift engajamento (%) |   p_value |   q_value | significativo   |
|---:|:---------------------------------|-------------------------:|----------:|----------:|:----------------|
|  6 | follower_tier = micro (10–50K)   |                  0.1606  |   0.1326  |    0.479  | False           |
|  7 | follower_tier = mid (50–100K)    |                  0.1393  |   0.1382  |    0.479  | False           |
| 16 | content_category = tech          |                  0.123   |   0.01003 |    0.1705 | False           |
| 11 | content_type = mixed             |                  0.08652 |   0.2009  |    0.5693 | False           |
|  1 | platform = Instagram             |                  0.0495  |   0.3157  |    0.5963 | False           |
|  2 | platform = RedNote               |                  0.04947 |   0.3075  |    0.5963 | False           |
| 12 | content_type = text              |                  0.04297 |   0.518   |    0.629  | False           |
| 10 | content_type = image             |                  0.03779 |   0.4384  |    0.629  | False           |
|  4 | platform = YouTube               |                  0.02765 |   0.5551  |    0.6292 | False           |
|  8 | follower_tier = macro (100–500K) |                  0.0249  |   0.4649  |    0.629  | False           |
| 15 | content_category = lifestyle     |                  0.02258 |   0.5115  |    0.629  | False           |
|  0 | platform = Bilibili              |                 -0.01546 |   0.7468  |    0.7934 | False           |

### Custo implícito por porte de creator (patrocinados)
| follower_tier    |        posts |   custo_mediano |   views_medianas |   cpm_implicito_mediano |   engajamento_medio |
|:-----------------|-------------:|----------------:|-----------------:|------------------------:|--------------------:|
| nano (<10K)      |  192         |            55.8 |        1.009e+04 |                   5.554 |              0.1992 |
| micro (10–50K)   |  922         |           295.5 |        1.01e+04  |                  29.31  |              0.1991 |
| mid (50–100K)    | 1108         |           763.5 |        1.01e+04  |                  75.41  |              0.1991 |
| macro (100–500K) | 8968         |          2986   |        1.01e+04  |                 296.4   |              0.1991 |
| mega (500K+)     |    1.112e+04 |          7508   |        1.01e+04  |                 744.3   |              0.199  |

### Engajamento vs. orgânico por categoria de patrocinador (%)
| sponsor_category   |   diferença (%) |
|:-------------------|----------------:|
| cosmetics          |        0.04938  |
| electronics        |       -0.004529 |
| fashion            |       -0.07636  |
| food               |        0.02551  |
| gaming             |       -0.03338  |
| travel             |        0.00634  |

### Engajamento vs. orgânico por tipo de disclosure (%)
| disclosure_type   |   diferença (%) |
|:------------------|----------------:|
| explicit          |         0.01563 |
| implicit          |        -0.0289  |

---

## 3. Qual audiência mais engaja?

**Resposta:** Nenhum perfil de audiência engaja mais: 36 testes (por plataforma, formato e categoria) e 0 significativos. A melhor 'persona' (gênero × idade × país) tem índice 100.5 com q=0.86. Escolha a audiência por objetivo de negócio (quem compra), não por engajamento.

|    | dimensão                     | melhor   | pior       |   diferença melhor−pior (%) |   epsilon² |   p_value |   q_value |
|---:|:-----------------------------|:---------|:-----------|----------------------------:|-----------:|----------:|----------:|
|  0 | audience_gender_distribution | unknown  | non-binary |                    0.003207 |  8.842e-06 |    0.9272 |    0.9272 |
|  1 | audience_age_distribution    | 50+      | 13-18      |                    0.06314  |  6.243e-05 |    0.5153 |    0.773  |
|  2 | audience_location            | UK       | India      |                    0.1061   |  0.0001311 |    0.4454 |    0.773  |

### Por contexto (plataforma, formato, categoria)
|    | contexto                     | audiência                    | segmento que mais engaja   |   diferença melhor−pior (%) |   p_value |   q_value | significativo   |
|---:|:-----------------------------|:-----------------------------|:---------------------------|----------------------------:|----------:|----------:|:----------------|
|  2 | platform = Bilibili          | audience_location            | UK                         |                     0.2923  |   0.06137 |    0.8666 | False           |
|  7 | platform = RedNote           | audience_age_distribution    | 19-25                      |                     0.1259  |   0.1077  |    0.8666 | False           |
|  5 | platform = Instagram         | audience_location            | Brazil                     |                     0.278   |   0.1498  |    0.8666 | False           |
| 32 | content_category = lifestyle | audience_location            | UK                         |                     0.1643  |   0.1556  |    0.8666 | False           |
|  4 | platform = Instagram         | audience_age_distribution    | 26-35                      |                     0.175   |   0.1655  |    0.8666 | False           |
|  1 | platform = Bilibili          | audience_age_distribution    | 50+                        |                     0.1828  |   0.172   |    0.8666 | False           |
| 25 | content_type = video         | audience_age_distribution    | 50+                        |                     0.1023  |   0.1917  |    0.8666 | False           |
| 12 | platform = YouTube           | audience_gender_distribution | male                       |                     0.1038  |   0.261   |    0.8666 | False           |
| 27 | content_category = beauty    | audience_gender_distribution | unknown                    |                     0.06513 |   0.3172  |    0.8666 | False           |
|  8 | platform = RedNote           | audience_location            | USA                        |                     0.2146  |   0.4092  |    0.8666 | False           |
| 35 | content_category = tech      | audience_location            | UK                         |                     0.2385  |   0.425   |    0.8666 | False           |
| 26 | content_type = video         | audience_location            | UK                         |                     0.1215  |   0.4252  |    0.8666 | False           |

### Personas (gênero × idade × país)
|    | segmento                   | dimensões                                                                    |   n |   índice |   p_value |   q_value | significativo   |
|---:|:---------------------------|:-----------------------------------------------------------------------------|----:|---------:|----------:|----------:|:----------------|
|  0 | male · 50+ · UK            | audience_gender_distribution × audience_age_distribution × audience_location | 123 |    100.5 |  0.01911  |    0.8587 | False           |
|  1 | non-binary · 26-35 · China | audience_gender_distribution × audience_age_distribution × audience_location | 213 |    100.5 |  0.002527 |    0.5938 | False           |
|  2 | 50+ · UK                   | audience_age_distribution × audience_location                                | 340 |    100.3 |  0.01526  |    0.8587 | False           |
|  3 | non-binary · 26-35 · UK    | audience_gender_distribution × audience_age_distribution × audience_location | 189 |    100.3 |  0.09662  |    0.9287 | False           |
|  4 | unknown · 13-18 · Japan    | audience_gender_distribution × audience_age_distribution × audience_location | 103 |    100.3 |  0.1846   |    0.9952 | False           |
|  5 | unknown · 26-35 · Germany  | audience_gender_distribution × audience_age_distribution × audience_location | 205 |    100.3 |  0.07395  |    0.8587 | False           |
|  6 | unknown · 50+              | audience_gender_distribution × audience_age_distribution                     | 257 |    100.3 |  0.05434  |    0.8587 | False           |
|  7 | female · 50+ · Russia      | audience_gender_distribution × audience_age_distribution × audience_location | 128 |    100.3 |  0.1613   |    0.9952 | False           |
|  8 | unknown · 19-25 · Japan    | audience_gender_distribution × audience_age_distribution × audience_location | 210 |    100.3 |  0.1674   |    0.9952 | False           |
|  9 | non-binary · 26-35 · Japan | audience_gender_distribution × audience_age_distribution × audience_location | 228 |    100.3 |  0.09741  |    0.9287 | False           |

---

## 4. O que NÃO funciona?

**Resposta:** 11 de 11 crenças comuns NÃO se sustentam: Mais seguidores → mais alcance; Mais seguidores → mais engajamento; Mais hashtags → mais alcance; Vídeo engaja mais que imagem/texto; Conteúdo curto (<60) engaja mais; Postar à noite (18–24h) dá mais alcance; Fim de semana dá mais alcance; Patrocínio aumenta alcance; Disclosure explícito derruba engajamento; Legenda longa engaja mais; Mais views → mais likes. Nenhum segmento é significativamente pior em nenhuma plataforma. Investir para mudar um atributo que não altera o resultado (ex.: pagar mais por seguidores, otimizar horário) é desperdício.

|    | crença de mercado                        | métrica        |     efeito | unidade        |   p_value |   q_value | se sustenta?   |
|---:|:-----------------------------------------|:---------------|-----------:|:---------------|----------:|----------:|:---------------|
|  0 | Mais seguidores → mais alcance           | views          |  0.004628  | ρ de Spearman  |    0.2903 |    0.5322 | não            |
|  1 | Mais seguidores → mais engajamento       | eng_rate_views | -0.002608  | ρ de Spearman  |    0.5513 |    0.8196 | não            |
|  2 | Mais hashtags → mais alcance             | views          | -0.006172  | ρ de Spearman  |    0.1584 |    0.5322 | não            |
|  3 | Vídeo engaja mais que imagem/texto       | eng_rate_views | -0.03168   | % de diferença |    0.1478 |    0.5322 | não            |
|  4 | Conteúdo curto (<60) engaja mais         | eng_rate_views | -0.01399   | % de diferença |    0.6491 |    0.8196 | não            |
|  5 | Postar à noite (18–24h) dá mais alcance  | views          | -0.01243   | % de diferença |    0.2162 |    0.5322 | não            |
|  6 | Fim de semana dá mais alcance            | views          |  0.01108   | % de diferença |    0.249  |    0.5322 | não            |
|  7 | Patrocínio aumenta alcance               | views          |  0.002854  | % de diferença |    0.7451 |    0.8196 | não            |
|  8 | Disclosure explícito derruba engajamento | eng_rate_views |  0.04454   | % de diferença |    0.1776 |    0.5322 | não            |
|  9 | Legenda longa engaja mais                | eng_rate_views | -0.0004897 | ρ de Spearman  |    0.9109 |    0.9109 | não            |
| 10 | Mais views → mais likes                  | likes          |  0.00149   | ρ de Spearman  |    0.7335 |    0.8196 | não            |

### Pior segmento por plataforma
|    | plataforma   | pior segmento (aparente)             |   índice |   q_value | significativo   |
|---:|:-------------|:-------------------------------------|---------:|----------:|:----------------|
|  0 | Instagram    | lifestyle · mid (50–100K)            |    99.61 |    0.578  | False           |
|  1 | TikTok       | mixed · lifestyle · macro (100–500K) |    99.72 |    0.6738 | False           |
|  2 | YouTube      | image · beauty · mega (500K+)        |    99.74 |    0.7656 | False           |
|  3 | Bilibili     | video · beauty · mid (50–100K)       |    99.68 |    0.6918 | False           |
|  4 | RedNote      | mixed · beauty · mega (500K+)        |    99.85 |    0.8414 | False           |