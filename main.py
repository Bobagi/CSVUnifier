import pandas as pd
import os
import re

# Diretório onde o script está localizado
diretorio_base = os.path.dirname(os.path.abspath(__file__))

# Diretório onde os arquivos CSV estão (pasta 'files')
diretorio_csv = os.path.join(diretorio_base, "files")

# Diretório onde o arquivo unificado será salvo (pasta 'result')
diretorio_result = os.path.join(diretorio_base, "result")

# Cria o diretório de resultado, se não existir
os.makedirs(diretorio_result, exist_ok=True)

# Caminho completo para o arquivo unificado
caminho_unificado = os.path.join(diretorio_result, "unified.csv")

# Remove o arquivo de destino, se ele já existir
if os.path.exists(caminho_unificado):
    os.remove(caminho_unificado)

print("Iniciando o processo de unificação dos arquivos CSV...")


# Função para extrair o número do nome do arquivo
def extrair_numero(nome_arquivo):
    match = re.search(r"(\d+)", nome_arquivo)
    return int(match.group(0)) if match else -1


# Lista de arquivos no diretório, filtrada e ordenada pelo número no nome
arquivos_csv = sorted(
    [f for f in os.listdir(diretorio_csv) if f.endswith(".csv")],
    key=extrair_numero,
    reverse=True,
)

# Contador para acompanhar o progresso
contador_arquivos = 0

# Percorre todos os arquivos ordenados
for arquivo in arquivos_csv:
    contador_arquivos += 1
    caminho_arquivo = os.path.join(diretorio_csv, arquivo)
    print(f"Lendo o arquivo {contador_arquivos}: {arquivo}")

    # Lê cada arquivo CSV em chunks e escreve no arquivo de destino
    for chunk in pd.read_csv(
        caminho_arquivo, delimiter=",", chunksize=10000
    ):  # substitua ',' pelo delimitador correto
        print(f"Processando chunk do arquivo {arquivo}...")

        # Remove linhas completamente vazias
        chunk.dropna(how="all", inplace=True)

        # Corrige problemas de espaços em branco nos cabeçalhos das colunas
        chunk.columns = chunk.columns.str.strip()

        # Remove colunas extras que podem ter sido criadas por erros de leitura
        chunk = chunk.loc[:, ~chunk.columns.str.contains("^Unnamed")]

        # Verifica se o número de colunas está correto
        if contador_arquivos == 1:
            expected_columns = chunk.columns
        else:
            if not chunk.columns.equals(expected_columns):
                print(
                    f"Atenção: O arquivo {arquivo} tem colunas inconsistentes. Ignorando esse arquivo."
                )
                continue

        # Append para não sobrescrever o arquivo anterior
        chunk.to_csv(
            caminho_unificado,
            mode="a",
            header=not os.path.exists(caminho_unificado),
            index=False,
        )

print(f"Processamento concluído! Arquivo unificado criado em: {caminho_unificado}")
