import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files
import io
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

# 📌 Função para carregar arquivos CSV
def carregar_arquivo(nome_referencia):
    print(f"📂 Faça o upload do arquivo: {nome_referencia}")
    uploaded_files = files.upload()
    
    nome_real = list(uploaded_files.keys())[0]
    
    try:
        df = pd.read_csv(io.BytesIO(uploaded_files[nome_real]))
        print(f"\n✅ Arquivo '{nome_real}' carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.\n")
        print(f"📊 Colunas encontradas: {list(df.columns)}\n")
        return df
    except Exception as e:
        print(f"⚠ Erro ao processar {nome_real}: {e}")
        return None

# 📌 Upload dos arquivos
df_vendas = carregar_arquivo("historico_vendas_wave_surfboards.csv")
df_marketing = carregar_arquivo("campanhas_publicitarias_wave_surfboards.csv")
df_meteorologia = carregar_arquivo("dados_meteorologicos_wave_surfboards.csv")

# 📊 Criar previsão se os dados foram carregados corretamente
if df_vendas is not None and df_marketing is not None and df_meteorologia is not None:
    
    # 🔹 Renomear colunas para facilitar a análise
    df_vendas.rename(columns={"Data": "Data", "Total Venda": "Vendas_Reais"}, inplace=True)
    df_marketing.rename(columns={"Data": "Data", "Investimento (R$)": "Orcamento_Marketing"}, inplace=True)
    df_meteorologia.rename(columns={"Data": "Data", "Temperatura Média (°C)": "Temperatura", "Precipitação (mm)": "Precipitacao"}, inplace=True)

    # 📆 Converter datas
    df_vendas["Data"] = pd.to_datetime(df_vendas["Data"], errors="coerce")
    df_marketing["Data"] = pd.to_datetime(df_marketing["Data"], errors="coerce")
    df_meteorologia["Data"] = pd.to_datetime(df_meteorologia["Data"], errors="coerce")

    # 🔹 Unir os datasets com base na data
    df_merged = df_vendas.merge(df_marketing, on="Data", how="left").merge(df_meteorologia, on="Data", how="left")

    # 📌 Criar colunas de ano e mês
    df_merged["Ano_Mes"] = df_merged["Data"].dt.to_period("M")

    # 📊 Selecionar as variáveis para o modelo
    df_modelo = df_merged.groupby("Ano_Mes").agg({
        "Vendas_Reais": "sum",
        "Orcamento_Marketing": "sum",
        "Temperatura": "mean",
        "Precipitacao": "sum"
    }).reset_index()

    # 🔹 Criar variável numérica para representar o tempo
    df_modelo["Mes_Num"] = np.arange(len(df_modelo))

    # 📌 Preparar dados para o modelo de regressão
    X = df_modelo[["Mes_Num", "Orcamento_Marketing", "Temperatura", "Precipitacao"]]
    y = df_modelo["Vendas_Reais"]

    # 📌 Dividir os dados em treino e teste
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

    # 🔹 Criar e treinar o modelo de regressão linear
    modelo = LinearRegression()
    modelo.fit(X_treino, y_treino)

    # 📌 Fazer previsões
    df_modelo["Vendas_Previstas"] = modelo.predict(X)

    # 📊 Criar gráfico de linha para comparação
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=df_modelo["Ano_Mes"].astype(str), y=df_modelo["Vendas_Reais"], marker="o", label="Vendas Reais", color="blue")
    sns.lineplot(x=df_modelo["Ano_Mes"].astype(str), y=df_modelo["Vendas_Previstas"], marker="s", label="Vendas Previstas", color="orange")
    
    plt.xlabel("Ano e Mês")
    plt.ylabel("Vendas")
    plt.title("📊 Comparação entre Vendas Reais e Previstas")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

else:
    print("❌ Erro no carregamento dos arquivos.")
