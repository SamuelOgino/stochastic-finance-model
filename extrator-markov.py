import yfinance as yf
import pandas as pd
import numpy as np

# Configurações Iniciais
TICKER = "^BVSP"
DATA_INICIO = "2019-01-01"
DATA_FIM = "2024-01-01"
LIMITE_ESTABILIDADE = 0.005 # 0.5%

def obter_dados_financeiros(ticker, start, end):
    print(f"Baixando dados para {ticker}...")
    df = yf.download(ticker, start=start, end=end, progress=False)
    # Mantemos apenas o preço de fechamento ajustado
    df = df[['Adj Close']].copy()
    df.columns = ['Preco_Fechamento']
    return df

def classificar_estados(df):
    # Calcula o retorno percentual diário
    df['Retorno'] = df['Preco_Fechamento'].pct_change()
    
    # Define as condições para cada estado
    condicoes = [
        (df['Retorno'] > LIMITE_ESTABILIDADE),
        (df['Retorno'] < -LIMITE_ESTABILIDADE)
    ]
    escolhas = ['Alta', 'Baixa']
    
    # Aplica a classificação; o padrão (se não for Alta nem Baixa) é Estável
    df['Estado'] = np.select(condicoes, escolhas, default='Estavel')
    
    # Remove a primeira linha, que terá Retorno NaN (não tem dia anterior)
    return df.dropna()

def calcular_matriz_transicao(df):
    # Desloca a coluna Estado em 1 dia para mapear "Ontem -> Hoje"
    df['Estado_Anterior'] = df['Estado'].shift(1)
    df = df.dropna() # Remove o primeiro dia que ficou sem 'Estado_Anterior'
    
    # Cria uma tabela de contingência cruzando o estado de ontem com o de hoje
    # O parâmetro normalize='index' garante que a soma das linhas seja estritamente 1.0
    matriz_transicao = pd.crosstab(
        df['Estado_Anterior'], 
        df['Estado'], 
        normalize='index'
    )
    
    # Garante a ordem das colunas e linhas para padronização
    ordem_estados = ['Alta', 'Baixa', 'Estavel']
    matriz_transicao = matriz_transicao.reindex(index=ordem_estados, columns=ordem_estados, fill_value=0)
    
    return matriz_transicao

if __name__ == "__main__":
    # 1. Download e Preparação
    dados_ibov = obter_dados_financeiros(TICKER, DATA_INICIO, DATA_FIM)
    
    # 2. Definição dos Estados
    dados_classificados = classificar_estados(dados_ibov)
    
    # 3. Construção da Matriz
    matriz = calcular_matriz_transicao(dados_classificados)
    
    print("\nMatriz de Probabilidades de Transição:")
    print(matriz)
    
    # 4. Exportação para uso no código em C
    matriz.to_csv("matriz_transicao.csv")
    print("\nArquivo 'matriz_transicao.csv' gerado com sucesso!")