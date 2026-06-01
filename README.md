# Simulador de Cadeias de Markov - Índice Ibovespa

Este projeto implementa um modelo estocástico baseado em Cadeias de Markov de tempo discreto para analisar e simular o comportamento diário do índice financeiro Ibovespa (^BVSP). 

A arquitetura do sistema é híbrida, utilizando **Python** para extração de dados e resolução algébrica, e **C** para o motor de simulação estocástica (Método de Monte Carlo) aliado a um gerador de números pseudoaleatórios customizado (MLCG).

## 📁 Estrutura do Diretório

* `simulacao_markov.c`: Código-fonte em C contendo o gerador MLCG e o motor da simulação (Roleta Viciada).
* `analise_markov.py`: Script de extração da bolsa, consolidação, resolução do sistema linear e geração de gráficos.
* `matriz_transicao.csv`: Ficheiro gerado pelo extrator contendo as probabilidades empíricas.
* `convergencia_simulacao.csv`: Histórico das 100.000 iterações gerado pelo simulador em C.
* `grafico_*.png`: Artefatos visuais gerados pela análise (heatmaps, linhas de convergência e barras).

*(Nota: Os ficheiros CSV e PNG já estão incluídos no pacote para fins de demonstração, mas podem ser regerados executando o pipeline abaixo).*

## ⚙️ Pré-requisitos

Para executar este projeto localmente, é necessário ter instalado:
1. **Compilador C** (ex: `gcc`)
2. **Python 3.8+**
3. Bibliotecas Python listadas abaixo. Para as instalar, execute:
   ```bash
   pip install pandas numpy matplotlib seaborn yfinance

🚀 Como Executar (Pipeline)
O sistema foi desenhado para ser executado numa ordem sequencial específica:

Etapa 1: Simulação de Monte Carlo (C)
Compile e execute o motor estocástico. O programa iterará 100.000 dias de pregão simulados utilizando o gerador MLCG e registará o comportamento de convergência.

Bash
# Compilar o código
gcc simulador.c -o simulador

# Executar (Linux/Mac)
./simulador

# Executar (Windows)
simulador.exe
Saída esperada: Ficheiro convergencia_simulacao.csv.

Etapa 2: Análise Matemática e Visualização (Python)
Por fim, execute o módulo analítico. Ele carrega os resultados, resolve a álgebra linear (autovetores) para achar a probabilidade limite teórica exata e plota os gráficos comparativos.

Bash
python analise_markov.py
Saídas esperadas: Exibição dos dados na consola e geração/atualização das imagens grafico_1_convergencia.png, grafico_2_heatmap.png, etc.

✒️ Autoria
Projeto desenvolvido como requisito prático para a disciplina de Simulação e Análise de Desempenho.