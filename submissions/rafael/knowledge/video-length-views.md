# Duração do vídeo × views — achados

Fonte: `solution/notebooks/09_duracao_views.ipynb` · figuras para o site: `docs/figures/duracao_x_views_hist2d.png` e `docs/figures/views_por_faixa_de_duracao.png` · 2026-10-19.
Base: 31.500 vídeos (`content_type == "video"`), duração = `content_length` (10–599 s).

## Manchete
**A duração do vídeo não muda as views.** Vídeos de 10 s e de 10 min têm a mesma mediana (~10.100 views).

## Números
| Faixa | Vídeos | Mínimo | Média | Mediana | Máximo |
|---|---|---|---|---|---|
| curto (<60 s) | 4.344 | 9.751 | 10.099,8 | 10.099 | 10.483 |
| médio (60–180 s) | 11.974 | 9.717 | 10.100,7 | 10.100 | 10.491 |
| longo (180–360 s) | 7.265 | 9.725 | 10.100,9 | 10.102 | 10.474 |
| muito longo (360+ s) | 7.917 | 9.748 | 10.099,7 | 10.100 | 10.477 |

**Máximos e mínimos por faixa de 30 s:** máximo entre 10.399 e 10.491, mínimo entre 9.717 e 9.809, sem tendência com a duração.
A amplitude (máx − mín) acompanha o **nº de vídeos da faixa** (ρ = +0,58, p = 0,008): faixas abaixo de 200 s têm ~3x mais vídeos e, por isso, extremos mais abertos (mais sorteios → extremos mais distantes). O "vídeo recordista" e o "pior vídeo" são acaso, não efeito da duração.

Spearman duração × views ρ = +0,001 (p = 0,83) · Kruskal entre faixas p = 0,83 · < 200 s vs. ≥ 200 s: 10.100,2 vs. 10.100,5 (p = 0,79).

## Forma da duração (descoberta sobre o dado)
- 58% dos vídeos ficam entre ~20 e 200 s, com ~2,9x mais vídeos por segundo de duração que acima de 200 s. Entre 200 e 600 s, a distribuição é plana.
- A **mesma forma** aparece em imagem, texto e misto (quartis ~95 / 174 / 359 em todos os formatos), então `content_length` não é uma duração real por formato.

## Leitura dos gráficos (para legenda no site)
- **Histograma 2D:** a mancha escura à esquerda é **quantidade de vídeos, não mais views**. A linha de mediana é reta, e as linhas de máximo (roxo) e mínimo (verde) oscilam sem tendência.
- **Histogramas por faixa:** as 4 curvas de views se sobrepõem.

## Recomendação
Escolher a duração por **custo de produção e formato nativo da plataforma**, não por alcance esperado.

## Como reproduzir
`.venv/bin/jupyter nbconvert --to notebook --execute --inplace solution/notebooks/09_duracao_views.ipynb` (regera as figuras em `docs/figures/`).
