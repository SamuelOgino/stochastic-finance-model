import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcular_probabilidade_teorica(caminho_matriz):
    # 1. Carrega a matriz gerada pelo Python na Fase 1
    df_matriz = pd.read_csv(caminho_matriz, index_col=0)
    P = df_matriz.values

    # 2. Resolução do sistema pi * P = pi (Método 2 da Etapa 4)
    # Na álgebra linear, isso equivale a encontrar o autovetor à esquerda 
    # associado ao autovalor 1. Usamos a transposta (P.T) para usar autovetores à direita.
    autovalores, autovetores = np.linalg.eig(P.T)

    # 3. Encontra qual autovalor é igual a 1 (ou muito próximo devido ao ponto flutuante)
    indice_estacionario = np.argmin(np.abs(autovalores - 1.0))
    autovetor_estacionario = autovetores[:, indice_estacionario].real

    # 4. Normaliza para garantir que a soma das probabilidades seja exatamente 1.0
    pi_teorico = autovetor_estacionario / np.sum(autovetor_estacionario)

    return df_matriz.columns, pi_teorico

def plotar_convergencia(caminho_simulacao, estados, pi_teorico):
    # Carrega os dados da simulação em C da Fase 2
    df_sim = pd.read_csv(caminho_simulacao)

    plt.figure(figsize=(12, 6))

    # Cores personalizadas: Verde (Alta), Vermelho (Baixa), Azul (Estável)
    cores = ['#2ca02c', '#d62728', '#1f77b4'] 

    for i, estado in enumerate(estados):
        coluna = f'Pi_{estado}'
        
        # Plota a linha contínua da Simulação em C
        plt.plot(df_sim['Iteracao'], df_sim[coluna], color=cores[i], linewidth=2, label=f'Simulação ({estado})')
        
        # Plota a linha pontilhada da Matemática Teórica para comparação visual
        plt.axhline(y=pi_teorico[i], color=cores[i], linestyle='--', alpha=0.8, 
                    label=f'Teórico ({estado}): {pi_teorico[i]:.4f}')

    plt.title('Convergência da Cadeia de Markov: Simulação vs. Teoria', fontsize=14, pad=15)
    plt.xlabel('Número de Iterações (Simulação)', fontsize=12)
    plt.ylabel('Probabilidade Limite ($\pi$)', fontsize=12)
    
    # Posiciona a legenda fora do gráfico para não tampar as linhas
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig('grafico_convergencia.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("--- Fase 3: Análise Teórica e Visualização ---")
    
    estados, pi_teorico = calcular_probabilidade_teorica('matriz_transicao.csv')
    
    print("\nProbabilidades Limites Teóricas (Resolvendo pi * P = pi):")
    for estado, prob in zip(estados, pi_teorico):
        print(f"Pi({estado}): {prob:.6f}")

    print("\nGerando gráfico de convergência...")
    plotar_convergencia('convergencia_simulacao.csv', estados, pi_teorico)
    print("Gráfico salvo como 'grafico_convergencia.png'!")