import pandas as pd
from google.colab import files
import io

# Função para carregar os arquivos
def carregar_arquivos():
    print("Faça o upload dos arquivos CSV:")
    uploaded_files = files.upload()
    
    dataframes = []
    
    for nome_arquivo in uploaded_files.keys():
        try:
            df = pd.read_csv(io.BytesIO(uploaded_files[nome_arquivo]))
            print(f"Arquivo '{nome_arquivo}' carregado com sucesso! {df.shape[0]} linhas antes da limpeza.")
            
            # Limpeza dos dados
            df.dropna(inplace=True)  # Remove valores nulos
            df.drop_duplicates(inplace=True)  # Remove duplicatas
            df.reset_index(drop=True, inplace=True)  # Reseta o índice
            
            print(f"Arquivo '{nome_arquivo}' após limpeza: {df.shape[0]} linhas restantes.")
            dataframes.append(df)
        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")

    # Unir todos os arquivos processados em um único dataframe
    if dataframes:
        df_final = pd.concat(dataframes, ignore_index=True)
        return df_final
    else:
        print("Nenhum arquivo válido foi carregado.")
        return None

# Chamar função para upload e processamento
df_tratado = carregar_arquivos()

# Se houver dados tratados, salvar e permitir download
if df_tratado is not None:
    nome_saida = "dados_tratados.csv"
    df_tratado.to_csv(nome_saida, index=False)
    print(f"Arquivo '{nome_saida}' salvo com sucesso!")
    
    # Iniciar download automaticamente
    files.download(nome_saida)
