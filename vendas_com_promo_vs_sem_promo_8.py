import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files
import io

# 📌 Função para carregar arquivos CSV
def carregar_arquivo(nome_referencia):
    print(f"📂 Faça o upload do arquivo: {nome_referencia}")
    uploaded_files = files.upload()
    
    # Obtém o nome real do arquivo do dicionário de uploads
    nome_real = list(uploaded_files.keys())[0]
    
    try:
        df = pd.read_csv(io.BytesIO(uploaded_files[nome_real]))
        print(f"\n✅ Arquivo '{nome_real}' carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.\n")
        print(f"📊 Colunas encontradas: {list(df.columns)}\n")  # Exibir colunas para depuração
        return df
    except Exception as e:
        print(f"⚠ Erro ao processar {nome_real}: {e}")
        return None

# 📌 Upload dos arquivos
df_marketing = carregar_arquivo("campanhas_publicitarias_wave_surfboards.csv")
df_vendas = carregar_arquivo("historico_vendas_wave_surfboards.csv")

# 📊 Criar análise se os dados forem carregados corretamente
if df_marketing is not None and df_vendas is not None:
    # 🔹 Normalizar nomes das colunas
    df_marketing.columns = df_marketing.columns.str.strip().str.lower().str.replace(" ", "_")
    df_vendas.columns = df_vendas.columns.str.strip().str.lower().str.replace(" ", "_")

    # 📌 Renomear colunas
    df_marketing.rename(columns={"investimento_(r$)": "orcamento_marketing", "tipo_de_campanha": "tipo_campanha"}, inplace=True)
    df_vendas.rename(columns={"total_venda": "vendas"}, inplace=True)

    # 📆 Converter datas
    if "data" in df_marketing.columns and "data" in df_vendas.columns:
        df_marketing["data"] = pd.to_datetime(df_marketing["data"], errors="coerce")
        df_vendas["data"] = pd.to_datetime(df_vendas["data"], errors="coerce")

        # 🔹 Criar colunas de ano e mês
        df_marketing["ano_mes"] = df_marketing["data"].dt.to_period("M")
        df_vendas["ano_mes"] = df_vendas["data"].dt.to_period("M")

        # 🔹 Unir os DataFrames pelo mês
        df_merged = pd.merge(df_marketing, df_vendas, on="ano_mes", how="inner")

        # 📌 Identificar meses com promoção
        campanhas_promocionais = ["Desconto Especial", "Promoção de Verão", "Sorteio"]
        df_merged["com_promocao"] = df_merged["tipo_campanha"].isin(campanhas_promocionais)

        # 📊 Comparar vendas por mês com e sem promoção
        vendas_comparacao = df_merged.groupby("com_promocao")["vendas"].mean().reset_index()
        vendas_comparacao["com_promocao"] = vendas_comparacao["com_promocao"].map({True: "Com Promoção", False: "Sem Promoção"})

        # 📊 Criar gráfico comparativo
        plt.figure(figsize=(8, 5))
        sns.barplot(x="com_promocao", y="vendas", data=vendas_comparacao, palette=["red", "green"])
        plt.xlabel("Tipo de Mês")
        plt.ylabel("Média de Vendas")
        plt.title("📊 Comparação de Vendas: Com e Sem Promoção")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

                # 📊 Criar Boxplot para comparar a distribuição de vendas
        plt.figure(figsize=(8, 5))
        sns.boxplot(x="com_promocao", y="vendas", data=df_merged, palette=["red", "green"])
        plt.xlabel("Tipo de Mês")
        plt.ylabel("Vendas")
        plt.title("📊 Distribuição de Vendas: Com e Sem Promoção")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()


    else:
        print("❌ Coluna 'Data' não encontrada nos arquivos para realizar a análise.")
else:
    print("❌ Erro no carregamento dos arquivos.")
