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
    df_marketing.rename(columns={"investimento_(r$)": "orcamento_marketing", "tipo_de_campanha": "tipo_campanha"}, inplace=True)
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
    if df_merged is not None and "orcamento_marketing" in df_merged.columns and "vendas" in df_merged.columns and "tipo_campanha" in df_merged.columns:

        # 📌 Função para definir a cor com base no orçamento de marketing e vendas
        def definir_cor(row):
            if row["orcamento_marketing"] <= row["vendas"] * 0.3:  # Bom (baixo custo, alto retorno)
                return "green"
            elif row["orcamento_marketing"] <= row["vendas"] * 0.6:  # Médio (custo razoável, retorno moderado)
                return "yellow"
            else:  # Ruim (alto custo, baixo retorno)
                return "red"

        # 📌 Aplicar a função para definir cores
        df_merged["cor"] = df_merged.apply(definir_cor, axis=1)

        # 📌 Classificação das campanhas
        campanha_eficaz = ["Campanha Online"]
        campanha_media = ["Promoção de Verão"]
        campanha_ruim = ["Desconto Especial", "Sorteio"]

        def classificar_campanha(tipo):
            if tipo in campanha_eficaz:
                return "green"
            elif tipo in campanha_media:
                return "yellow"
            else:
                return "red"

        # 📌 Aplicar classificação nas campanhas
        df_merged["cor_campanha"] = df_merged["tipo_campanha"].apply(classificar_campanha)

        # 📊 Criar gráfico de barras mostrando a relação entre orçamento e vendas, destacando campanhas
        plt.figure(figsize=(12, 6))
        sns.barplot(x=df_merged["orcamento_marketing"], y=df_merged["vendas"], hue=df_merged["cor_campanha"], dodge=False, palette={"green": "green", "yellow": "yellow", "red": "red"})
        plt.xlabel("Orçamento de Marketing (R$)")
        plt.ylabel("Vendas (R$)")
        plt.title("📊 Impacto do Orçamento de Marketing nas Vendas por Tipo de Campanha")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.legend(title="Eficácia da Campanha", labels=["Alta (Verde)", "Média (Amarelo)", "Baixa (Vermelho)"])
        plt.show()

    else:
        print(f"❌ Colunas 'orcamento_marketing', 'vendas' ou 'tipo_campanha' não encontradas após normalização. Verifique os nomes reais: {list(df_merged.columns) if df_merged is not None else 'Nenhum dado disponível'}")
