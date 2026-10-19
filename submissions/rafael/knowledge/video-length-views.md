# Duração do vídeo × views — achados

Fonte: `solution/notebooks/09_duracao_views.ipynb` · figuras para o site: `docs/figures/duracao_x_views_hist2d.png` e `docs/figures/views_por_faixa_de_duracao.png` · 2026-10-19.
Base: 31.500 vídeos (`content_type == "video"`), duração = `content_length` (10–599 s).

## Manchete
**A duração do vídeo não muda as views.** Vídeos de 10 s e de 10 min têm a mesma mediana (~10.100 views).

## Números
| Faixa | Vídeos | Média | Mediana |
|---|---|---|---|
| curto (<60 s) | 4.344 | 10.099,8 | 10.099 |
| médio (60–180 s) | 11.974 | 10.100,7 | 10.100 |
| longo (180–360 s) | 7.265 | 10.100,9 | 10.102 |
| muito longo (360+ s) | 7.917 | 10.099,7 | 10.100 |

Spearman duração × views ρ = +0,001 (p = 0,83) · Kruskal entre faixas p = 0,83 · < 200 s vs. ≥ 200 s: 10.100,2 vs. 10.100,5 (p = 0,79).

## Forma da duração (descoberta sobre o dado)
- 58% dos vídeos ficam entre ~20 e 200 s, com ~2,9x mais vídeos por segundo de duração que acima de 200 s. Entre 200 e 600 s, a distribuição é plana.
- A **mesma forma** aparece em imagem, texto e misto (quartis ~95 / 174 / 359 em todos os formatos), então `content_length` não é uma duração real por formato.

## Leitura dos gráficos (para legenda no site)
- **Histograma 2D:** a mancha escura à esquerda é **quantidade de vídeos, não mais views**. A linha de mediana é reta.
- **Histogramas por faixa:** as 4 curvas de views se sobrepõem.

## Recomendação
Escolher a duração por **custo de produção e formato nativo da plataforma**, não por alcance esperado.

## Como reproduzir
`.venv/bin/jupyter nbconvert --to notebook --execute --inplace solution/notebooks/09_duracao_views.ipynb` (regera as figuras em `docs/figures/`).
