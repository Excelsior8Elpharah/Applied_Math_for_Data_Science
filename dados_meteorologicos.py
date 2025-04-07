import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files
import io

# 📌 Função para carregar arquivos CSV
def carregar_arquivo(nome_referencia):
    print(f"📂 Faça o upload do arquivo: {nome_referencia}")
    uploaded_files = files.upload()
    nome_real = list(uploaded_files.keys())[0]
    try:
        df = pd.read_csv(io.BytesIO(uploaded_files[nome_real]))
        print(f"\n✅ Arquivo '{nome_real}' carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.")
        print(f"📊 Colunas encontradas: {list(df.columns)}\n")
        return df
    except Exception as e:
        print(f"⚠ Erro ao processar {nome_real}: {e}")
        return None

# 📌 Upload dos dois arquivos meteorológicos
df1 = carregar_arquivo("dados_meteorologicos_wave_surfboards_.csv")
df2 = carregar_arquivo("dados_meteorologicos_wave_surfboards_.csv")

if df1 is not None and df2 is not None:
    # 🔹 Padronizar nomes de colunas
    for df in [df1, df2]:
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # 📆 Agrupar por mês
    df1['ano_mes'] = df1["data"].dt.to_period("M")
    df2['ano_mes'] = df2["data"].dt.to_period("M")

    df1_agg = df1.groupby("ano_mes").agg({
        "temperatura_média_(°c)": "mean",
        "precipitação_(mm)": "sum"
    }).rename(columns={
        "temperatura_média_(°c)": "temp_média_1",
        "precipitação_(mm)": "precipitação_1"
    }).reset_index()

    df2_agg = df2.groupby("ano_mes").agg({
        "temperatura_média_(°c)": "mean",
        "precipitação_(mm)": "sum"
    }).rename(columns={
        "temperatura_média_(°c)": "temp_média_2",
        "precipitação_(mm)": "precipitação_2"
    }).reset_index()

    # 🔁 Juntar os dois DataFrames pela data
    df_comparado = pd.merge(df1_agg, df2_agg, on="ano_mes", how="inner")

    # 📊 Gráfico de comparação de temperatura média
    plt.figure(figsize=(12, 5))
    sns.lineplot(x=df_comparado["ano_mes"].astype(str), y=df_comparado["temp_média_1"], marker="o", label="Estação 1")
    sns.lineplot(x=df_comparado["ano_mes"].astype(str), y=df_comparado["temp_média_2"], marker="s", label="Estação 2")
    plt.title("📈 Comparação de Temperatura Média por Mês")
    plt.xlabel("Ano-Mês")
    plt.ylabel("Temperatura Média (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.show()

    # 📊 Gráfico de comparação de precipitação
    plt.figure(figsize=(12, 5))
    sns.lineplot(x=df_comparado["ano_mes"].astype(str), y=df_comparado["precipitação_1"], marker="o", label="Estação 1")
    sns.lineplot(x=df_comparado["ano_mes"].astype(str), y=df_comparado["precipitação_2"], marker="s", label="Estação 2")
    plt.title("🌧️ Comparação de Precipitação por Mês")
    plt.xlabel("Ano-Mês")
    plt.ylabel("Precipitação (mm)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.show()

else:
    print("❌ Erro no carregamento dos arquivos.")
