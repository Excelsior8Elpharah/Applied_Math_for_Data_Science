import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files
import io
from sklearn.impute import SimpleImputer  # Para tratar valores ausentes

# 📌 Função para carregar arquivo CSV com botão
def carregar_arquivo():
    print("📂 Faça o upload do arquivo CSV:")
    uploaded_file = files.upload()
    
    for nome_arquivo in uploaded_file.keys():
        try:
            df = pd.read_csv(io.BytesIO(uploaded_file[nome_arquivo]))
            print(f"\n✅ Arquivo '{nome_arquivo}' carregado! {df.shape[0]} linhas antes da limpeza.")
            
            # 🔹 Limpeza dos dados
            df.drop_duplicates(inplace=True)  # Remove duplicatas
            df.dropna(how='all', inplace=True)  # Remove linhas totalmente vazias
            df.reset_index(drop=True, inplace=True)  # Reseta o índice

            # 📌 Verifica se há uma coluna de data e a converte
            for col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                    df.set_index(col, inplace=True)
                    print(f"📆 Coluna '{col}' definida como índice de tempo.\n")
                    break
                except:
                    continue

            # 🔹 Selecionar apenas colunas numéricas para imputação
            colunas_numericas = df.select_dtypes(include=[np.number]).columns
            
            if colunas_numericas.any():
                imputer = SimpleImputer(strategy="mean")  # Preencher valores ausentes com a média
                df[colunas_numericas] = imputer.fit_transform(df[colunas_numericas])
                print("✅ Valores ausentes preenchidos nas colunas numéricas.\n")
            else:
                print("⚠ Nenhuma coluna numérica encontrada para imputação.\n")

            print(f"✅ Dados após limpeza: {df.shape[0]} linhas restantes.\n")
            return df
        except Exception as e:
            print(f"⚠ Erro ao processar {nome_arquivo}: {e}")
            return None

# 📌 Carregar arquivo e processar os dados
df = carregar_arquivo()

# 🔹 Se houver dados tratados, gerar gráfico de evolução das vendas
if df is not None:
    # 📌 Verificar se a coluna "Vendas" está presente
    col_vendas = [col for col in df.columns if 'venda' in col.lower()]
    
    if col_vendas:
        col_vendas = col_vendas[0]
        
        # 📊 Gráfico de Barras Colorido da Evolução das Vendas
        plt.figure(figsize=(12, 6))
        cores = sns.color_palette("husl", len(df))  # Gera uma paleta de cores
        plt.bar(df.index, df[col_vendas], color=cores, alpha=0.8)  # Gráfico de barras
        plt.xlabel("Tempo")
        plt.ylabel("Vendas")
        plt.title("📊 Evolução das Vendas ao Longo do Tempo")
        plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo X
        plt.grid(axis="y", linestyle="--", alpha=0.7)  # Adiciona grades no eixo Y
        plt.show()
    else:
        print("❌ Nenhuma coluna de vendas foi encontrada no arquivo.")
