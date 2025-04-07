import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files
import io
from sklearn.impute import SimpleImputer  # Para tratar valores ausentes

# 📌 Função para carregar arquivo CSV
def carregar_arquivo(nome):
    print(f"📂 Faça o upload do arquivo CSV de {nome}:")
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

# 📌 Carregar os arquivos
df_vendas = carregar_arquivo("historico_vendas_wave_surfboards")
df_campanhas = carregar_arquivo("campanhas_publicitarias_wave_surfboards")

# 🔹 Verificar se os dois arquivos foram carregados corretamente
if df_vendas is not None and df_campanhas is not None:
    # 📌 Unir os dados pelo índice de tempo, resolvendo conflito de colunas duplicadas
    df = df_vendas.join(df_campanhas, how="inner", lsuffix="_vendas", rsuffix="_campanhas")

    # 📌 Verificar se há colunas de vendas e de campanhas
    col_vendas = [col for col in df.columns if 'venda' in col.lower()]
    col_campanhas = [col for col in df.columns if 'campanha' in col.lower() or 'marketing' in col.lower()]

    if col_vendas and col_campanhas:
        col_vendas = col_vendas[0]
        col_campanhas = col_campanhas[0]

        # 📊 Gráfico de Evolução das Vendas com Campanhas Publicitárias
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # 🔹 Gráfico de Barras para Vendas
        cores = sns.color_palette("husl", len(df))  # Gera uma paleta de cores
        barras = ax1.bar(df.index, df[col_vendas], color=cores, alpha=0.8, label="Vendas")
        ax1.set_xlabel("Tempo")
        ax1.set_ylabel("Vendas", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        # 🔹 Criar segundo eixo Y para Campanhas Publicitárias
        ax2 = ax1.twinx()
        ax2.plot(df.index, df[col_campanhas], color="green", marker="o", linestyle="-", label="Campanhas Publicitárias")
        ax2.set_ylabel("Investimento em Campanhas ($)", color="green")
        ax2.tick_params(axis="y", labelcolor="green")

        # 🔹 Ajustes finais no gráfico
        plt.title("📊 Evolução das Vendas e Campanhas Publicitárias ao Longo do Tempo")
        fig.autofmt_xdate()  # Ajusta rotação das datas
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # 🔹 Legendas
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        plt.show()
    else:
        print("❌ Não foram encontradas colunas adequadas de vendas e/ou campanhas publicitárias.")
