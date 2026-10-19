# Resumo executivo — Estratégia de Social Media

Para: Head de Marketing · Base: 52.214 posts (mai/2023 → mai/2025), 5 plataformas · Leitura: 5 minutos.

## A conclusão em uma frase

**Nos dados entregues, nada do que o time controla (plataforma, formato, tema, tamanho do creator, horário, hashtags, patrocínio) muda o engajamento ou o alcance. Então a decisão é de preço e de medição, não de "receita de post".**

Antes de qualquer conclusão, verificamos se os testes enxergariam um efeito real: eles detectariam diferenças de até 0,3%. Por isso, "não faz diferença" aqui é um resultado, não falta de dados. O próprio Kaggle descreve a base como **simulada** (views sorteadas). Com os dados da empresa, o mesmo site e as mesmas funções recalculam tudo.

## As 4 perguntas

| Pergunta | Resposta | Número-chave |
|---|---|---|
| O que gera engajamento? | Nenhuma plataforma, formato, tema, porte de creator ou combinação | 450 combinações testadas, 0 com efeito real; maior diferença 0,07% |
| Patrocínio funciona? | Não para ganhar desempenho. Comparando posts parecidos (mesma plataforma, formato, tema e porte), o patrocinado engaja igual | +0,008% de engajamento (p = 0,72) |
| Que público engaja mais? | Nenhum: gênero, idade e país engajam igual em todo contexto | 36 contextos testados, 0 com efeito |
| O que não funciona? | 11 de 11 "verdades" de mercado testadas | ex.: "mais seguidores = mais alcance" (correlação 0,005) |

## O que fazer nesta semana

**Valem também com os dados reais da empresa:**
1. **Contratar creators por resultado** (por mil views ou por interação), não por post. As views não crescem com os seguidores: com cachê proporcional aos seguidores, o creator mega paga **~134x mais por mil views** que o nano, e essa proporção vale para qualquer valor de cachê.
2. **Exigir rótulo de publicidade no texto (#publi/#ad).** 47% dos patrocinados usam divulgação implícita (risco regulatório alto) e só 2,3% mostram o rótulo no texto. O tipo de divulgação não muda o engajamento.
3. **Todo patrocínio novo com um grupo de comparação orgânico**, para medir o ganho real (≥ 30 posts por grupo nesta base; o site refaz a conta com os seus dados).
4. **Não pagar a mais por creator "campeão" e tirar "melhor horário" e "nº ideal de hashtags" do checklist.** Só 8,8% dos melhores creators do 1º ano continuaram entre os melhores no 2º, menos que os 10% do acaso.

**Dependem dos preços reais (recalcular antes de aplicar):**
5. Teto de ~10 mil seguidores para contratos de preço fixo. Sai das premissas (US$ 10 por mil seguidores, até US$ 10 por mil views); com outros preços, varia de 1 mil a 40 mil.
6. Formato padrão pelo custo real de produção: nenhum formato engaja mais, então o mais barato que a plataforma comporta vence.

## O que testar (e quanto custa confirmar)

| # | Hipótese | Evidência | Posts por grupo | Como tratar |
|---|---|---|---|---|
| 1 | TikTok · beauty · espanhol: mais chance de top 5% em likes | 10,0% vs. 4,9% (2x), nos dois anos; único padrão que passou na correção entre ~14,7 mil testes | ~1.430 | teste A/B (mesmo conteúdo em espanhol × inglês) |
| 2 | YouTube: posts até 12h entram mais no top 1% de comentários | 1,45% vs. 0,85%; a média de comentários não muda | ~17.000 | acompanhar no histórico; usar como desempate de agenda |
| 3 | Patrocínio aumenta o engajamento em ≥ 5% | nenhum efeito nesta base | 30 | teste A/B com os contratos da empresa |

## O que parar

- Pagar preço fixo por seguidores: pelas premissas, ~98% do gasto implícito com patrocínio é excedente sobre o preço justo.
- Pagar a mais por formatos caros "porque engajam mais".
- Usar como regra geral horário, hashtags, tamanho de legenda ou duração.

## Lacunas de carteira (valem mesmo sem efeito no engajamento)

- 60% dos patrocínios estão fora do nicho do creator (ex.: games em beleza).
- Só 22% dos posts estão no idioma do mercado e numa rede disponível lá. Brasil, Alemanha e Rússia não têm conteúdo no idioma local.

## Ferramenta para o dia a dia

Site em linguagem simples (`.venv/bin/social-web`):
- **Início:** este resumo, gerado dos dados.
- **Explorar:** painel com filtros para comparar grupos, com selo de "diferença real".
- **Simular post:** antes de publicar, mostra a chance de virar destaque e uma versão próxima mais forte, com selo de evidência.
- **Auditorias, Estratégia e Descobertas:** detalhes sob demanda.

Para usar com os dados da empresa: trocar o CSV e rodar `social-web --rebuild`. Textos, números e recomendações se recalculam sozinhos.

## Limites

- A base é simulada: os achados descrevem esta base. O valor que se transfere são o método e a ferramenta, validados com efeitos plantados.
- Não há preços na base. Todos os valores em US$ vêm de premissas editáveis.
- `post_date` não tem fuso: os horários assumem um relógio único.
