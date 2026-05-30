#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define NUM_ESTADOS 3
#define ITERACOES 100000 // 100 mil iteracoes para convergencia

#define ALTA 0
#define BAIXA 1
#define ESTAVEL 2

double matriz_transicao[NUM_ESTADOS][NUM_ESTADOS];

/* ==========================================================
   GERADOR MLCG (Da Atividade 1)
   ========================================================== */
#define A 2685821657736338717ULL
uint64_t state = 123456789ULL;

double seu_gerador_pseudoaleatorio()
{
    state = state * A; // Modulo de 2^64 por overflow automatico

    // Desloca 32 bits para usar a parte mais "aleatoria" do numero
    uint32_t bits_altos = state >> 32;

    // Divide pelo valor maximo de 32 bits (2^32) para obter [0.0, 1.0)
    return (double)bits_altos / 4294967296.0;
}
/* ========================================================== */

void carregar_matriz()
{
    FILE *file = fopen("matriz_transicao.csv", "r");
    if (file == NULL)
    {
        printf("Erro: Nao foi possivel abrir matriz_transicao.csv\n");
        exit(1);
    }

    char buffer[1024];
    fgets(buffer, sizeof(buffer), file);

    for (int i = 0; i < NUM_ESTADOS; i++)
    {
        if (fscanf(file, "%*[^,],%lf,%lf,%lf",
                   &matriz_transicao[i][ALTA],
                   &matriz_transicao[i][BAIXA],
                   &matriz_transicao[i][ESTAVEL]) != 3)
        {
            printf("Erro ao ler os dados da linha %d do CSV.\n", i + 1);
            exit(1);
        }
    }
    fclose(file);
    printf("Matriz de transicao carregada com sucesso!\n\n");
}

int main()
{
    carregar_matriz();

    int contagem_estados[NUM_ESTADOS] = {0, 0, 0};
    int estado_atual = ESTAVEL;

    // NOVO: Abre o arquivo CSV para salvar o histórico da simulação
    FILE *f_out = fopen("convergencia_simulacao.csv", "w");
    if (f_out == NULL)
    {
        printf("Erro ao criar arquivo de convergencia.\n");
        exit(1);
    }
    // Escreve o cabeçalho no CSV
    fprintf(f_out, "Iteracao,Pi_Alta,Pi_Baixa,Pi_Estavel\n");

    printf("Iniciando simulacao de %d iteracoes...\n", ITERACOES);

    for (int i = 0; i < ITERACOES; i++)
    {
        contagem_estados[estado_atual]++;

        double r = seu_gerador_pseudoaleatorio();
        double probabilidade_acumulada = 0.0;
        int proximo_estado = -1;

        for (int j = 0; j < NUM_ESTADOS; j++)
        {
            probabilidade_acumulada += matriz_transicao[estado_atual][j];
            if (r <= probabilidade_acumulada)
            {
                proximo_estado = j;
                break;
            }
        }
        estado_atual = proximo_estado;

        // NOVO: A cada 100 iterações, anota a probabilidade atual no CSV
        if ((i + 1) % 100 == 0)
        {
            fprintf(f_out, "%d,%.6f,%.6f,%.6f\n",
                    i + 1,
                    (double)contagem_estados[ALTA] / (i + 1),
                    (double)contagem_estados[BAIXA] / (i + 1),
                    (double)contagem_estados[ESTAVEL] / (i + 1));
        }
    }

    fclose(f_out); // Fecha e salva o arquivo

    printf("\n--- Probabilidades Limite (Simulacao Empirica) ---\n");
    printf("Pi(Alta):    %.6f\n", (double)contagem_estados[ALTA] / ITERACOES);
    printf("Pi(Baixa):   %.6f\n", (double)contagem_estados[BAIXA] / ITERACOES);
    printf("Pi(Estavel): %.6f\n", (double)contagem_estados[ESTAVEL] / ITERACOES);
    printf("\nHistorico salvo com sucesso em 'convergencia_simulacao.csv'!\n");

    return 0;
}