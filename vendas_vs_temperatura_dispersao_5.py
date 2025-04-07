import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 📌 Carregar os arquivos CSV
df_vendas = pd.read_csv("historico_vendas_wave_surfboards.csv")
df_temp = pd.read_csv("dados_meteorologicos_wave_surfboards.csv")

# 🔹 Padronizar os nomes das colunas para evitar erros de capitalização
df_vendas.columns = df_vendas.columns.str.strip()
df_temp.columns = df_temp.columns.str.strip()

# 📆 Converter a coluna "Data" para o formato de data
df_vendas["Data"] = pd.to_datetime(df_vendas["Data"])
df_temp["Data"] = pd.to_datetime(df_temp["Data"])

# 🔹 Fazer o merge dos DataFrames com base na data
df_merged = pd.merge(df_vendas, df_temp, on="Data", how="inner")

# 📌 Verificar as colunas corretas de temperatura e vendas
col_vendas = [col for col in df_merged.columns if "Venda" in col]
col_temp = [col for col in df_merged.columns if "Temperatura" in col]

if col_vendas and col_temp:
    col_vendas = col_vendas[0]
    col_temp = col_temp[0]

    # 📊 Criar figura e eixo
    fig, ax = plt.subplots(figsize=(10, 6))

    # Normalizar cores para o gráfico
    norm = plt.Normalize(df_merged[col_temp].min(), df_merged[col_temp].max())
    sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
    sm.set_array([])  # Corrigido para evitar erro na barra de cores

    # Criar gráfico de dispersão
    scatter = sns.scatterplot(
        ax=ax,
        x=df_merged[col_temp], 
        y=df_merged[col_vendas], 
        hue=df_merged[col_temp],  # Cores baseadas na temperatura
        palette="coolwarm",
        alpha=0.8,
        edgecolor="black"
    )

    # 🔹 Personalizar gráfico
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Vendas")
    ax.set_title("📈 Impacto da Temperatura nas Vendas")
    ax.grid(True, linestyle="--", alpha=0.5)

    # 📌 Adicionar barra de cores
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Temperatura (°C)")

    plt.show()
else:
    print("❌ Colunas de temperatura ou vendas não encontradas no dataset.")
