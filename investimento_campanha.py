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

# 📌 Upload dos dois arquivos de campanhas
df1 = carregar_arquivo("campanhas_publicitarias_wave_surfboards_1.csv")
df2 = carregar_arquivo("campanhas_publicitarias_wave_surfboards_2.csv")

if df1 is not None and df2 is not None:
    # 🔹 Padronizar nomes de colunas e tipos
    for df in [df1, df2]:
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df["tipo_de_campanha"] = df["tipo_de_campanha"].str.strip().str.title()

    # ✅ Identificar a coluna de investimento dinamicamente
    col_invest = [col for col in df1.columns if "investimento" in col][0]

    # 📆 Criar coluna ano-mês para agrupamento
    df1['ano_mes'] = df1["data"].dt.to_period("M")
    df2['ano_mes'] = df2["data"].dt.to_period("M")

    # 📊 Agrupar por tipo de campanha e mês
    agg1 = df1.groupby(["ano_mes", "tipo_de_campanha"])[col_invest].sum().reset_index().rename(columns={col_invest: "investimento_1"})
    agg2 = df2.groupby(["ano_mes", "tipo_de_campanha"])[col_invest].sum().reset_index().rename(columns={col_invest: "investimento_2"})

    # 🔁 Unir os dois para comparação
    df_comparado = pd.merge(agg1, agg2, on=["ano_mes", "tipo_de_campanha"], how="outer").fillna(0)

    # 📌 Gráfico: comparação de investimento mensal por tipo de campanha
    tipos_campanha = ["Campanha Online", "Promoção De Verão", "Desconto Especial", "Sorteio"]
    for tipo in tipos_campanha:
        df_tipo = df_comparado[df_comparado["tipo_de_campanha"] == tipo]

        plt.figure(figsize=(10, 4))
        sns.lineplot(x=df_tipo["ano_mes"].astype(str), y=df_tipo["investimento_1"], marker="o", label="Arquivo 1")
        sns.lineplot(x=df_tipo["ano_mes"].astype(str), y=df_tipo["investimento_2"], marker="s", label="Arquivo 2")
        plt.title(f"📊 Investimento Mensal - {tipo}")
        plt.xlabel("Ano-Mês")
        plt.ylabel("Investimento (R$)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # 📌 Gráfico: frequência total de campanhas por tipo
    freq1 = df1["tipo_de_campanha"].value_counts().rename("frequência_1")
    freq2 = df2["tipo_de_campanha"].value_counts().rename("frequência_2")
    df_freq = pd.concat([freq1, freq2], axis=1).fillna(0).astype(int).reset_index().rename(columns={"index": "Tipo de Campanha"})

    # 📊 Comparar frequência de campanhas
    df_freq.plot(x="Tipo de Campanha", kind="bar", figsize=(8, 5), color=["skyblue", "orange"])
    plt.title("📊 Frequência de Campanhas por Tipo")
    plt.ylabel("Quantidade de campanhas")
    plt.xticks(rotation=30)
    plt.legend(["Arquivo 1", "Arquivo 2"])
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

else:
    print("❌ Erro no carregamento dos arquivos.")
