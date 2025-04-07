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

# 📊 Criar gráfico se os dados forem carregados corretamente
if df_marketing is not None and df_vendas is not None:
    # 🔹 Normalizar nomes das colunas
    df_marketing.columns = df_marketing.columns.str.strip().str.lower().str.replace(" ", "_")
    df_vendas.columns = df_vendas.columns.str.strip().str.lower().str.replace(" ", "_")

    # 📌 Renomear as colunas para um padrão mais intuitivo
    df_marketing.rename(columns={"investimento_(r$)": "orcamento_marketing"}, inplace=True)
    df_vendas.rename(columns={"total_venda": "vendas"}, inplace=True)

    # 📆 Converter datas se houver uma coluna de data
    if "data" in df_marketing.columns and "data" in df_vendas.columns:
        df_marketing["data"] = pd.to_datetime(df_marketing["data"], errors="coerce")
        df_vendas["data"] = pd.to_datetime(df_vendas["data"], errors="coerce")

        # 🔹 Unir os DataFrames com base na data
        df_merged = pd.merge(df_marketing, df_vendas, on="data", how="inner")
    else:
        df_merged = None
        print("❌ Coluna 'Data' não encontrada nos arquivos para realizar o merge.")

    # 📌 Verificar se as colunas necessárias estão no dataset combinado
    if df_merged is not None and "orcamento_marketing" in df_merged.columns and "vendas" in df_merged.columns:
        plt.figure(figsize=(12, 6))
        cores = sns.color_palette("coolwarm", len(df_merged))  # Paleta de cores
        sns.barplot(x=df_merged["orcamento_marketing"], y=df_merged["vendas"], palette=cores)
        plt.xlabel("Orçamento de Marketing (R$)")
        plt.ylabel("Vendas")
        plt.title("📊 Impacto do Orçamento de Marketing nas Vendas")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()
    else:
        print(f"❌ Colunas 'orcamento_marketing' e 'vendas' não encontradas após normalização. Verifique os nomes reais: {list(df_merged.columns) if df_merged is not None else 'Nenhum dado disponível'}")
