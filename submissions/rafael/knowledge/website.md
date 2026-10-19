# Site de entrega — arquitetura e como usar

Saída: `solution/site/dist/index.html` (arquivo único, abre no navegador sem servidor) · gerado em 2026-10-19.

## Arquitetura (separação de responsabilidades)
| Camada | Arquivo | Papel |
|---|---|---|
| Dados | `solution/src/social_insights/site_export.py` | roda as análises e devolve um payload JSON; **todo número e frase vem dos dados** (vereditos, ações e cards gerados pelas funções) |
| Apresentação | `solution/site/template.html` | HTML + CSS + JS; lê `DATA` e renderiza seções, tabelas, gráficos (Chart.js 4.4.1 via cdnjs) e o simulador |
| Montagem | `solution/site/build_site.py` | injeta o JSON no template → `dist/index.html` (documento completo), `dist/site.html` (fragmento) e `dist/data.json` |
| Testes | `solution/tests/test_site_export.py` | seções completas, JSON seguro, tabelas do simulador, parser de condições, renderização |

## Seções do site (↔ o que o desafio pede)
| Seção | Entrega |
|---|---|
| Resumo | tese, 4 números-chave, aviso sobre o dataset sintético |
| Os dados | qualidade, correlação entre métricas, varredura de 33 atributos × 3 métricas |
| Perguntas 1–4 | o que gera engajamento · patrocínio (comparação estratificada + CPM implícito) · audiência · o que não funciona (11 crenças + duração do vídeo) |
| Estratégia | onde concentrar · política de patrocínio (ponto de equilíbrio) · o que parar · quick wins (esforço, impacto, dono) |
| Insights | destaque robusto (TikTok · beauty · espanhol → likes), horário × comentários por plataforma, replicação, explorador de ~940 bolsões com filtros |
| Modelos | 14 abordagens de engajamento (treino × validação), previsão de views pré-postagem, AUC da chance de top 5%, controle positivo |
| Simulador | monta um post → chance oficial de top 5% por métrica, sinal do segmento com IC90, comparação entre formatos, views esperadas, bolsões que se aplicam |
| Método | testes usados, limitações, comandos para reproduzir |

## Como usar
```bash
cd submissions/rafael
.venv/bin/python solution/site/build_site.py   # ~3 min; regenera dist/ (rodar após trocar o CSV pelos dados reais)
xdg-open solution/site/dist/index.html          # ou abrir no navegador
```
- Funciona offline, exceto os gráficos (Chart.js e fontes vêm de CDN); sem internet, as tabelas continuam com os dados.
- Tema claro/escuro automático; responsivo até ~400 px.
- **Simulador:** usa a chance oficial (modelo adotado ou taxa base) e as tabelas de segmento exportadas. Modelos de ML adotados no futuro são aplicados pela CLI `solution/predict_hit.py`; o site então mostra a taxa base e o sinal do segmento.
