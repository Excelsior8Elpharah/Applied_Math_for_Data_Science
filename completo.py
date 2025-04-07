# 📌 Importação das bibliotecas necessárias
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
        print(f"\n✅ Arquivo '{nome_real}' carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.\n")
        return df
    except Exception as e:
        print(f"⚠ Erro ao processar {nome_real}: {e}")
        return None

# 📌 Upload dos arquivos
df_vendas = carregar_arquivo("historico_vendas_wave_surfboards.csv")
df_marketing = carregar_arquivo("campanhas_publicitarias_wave_surfboards.csv")
df_meteorologia = carregar_arquivo("dados_meteorologicos_wave_surfboards.csv")

# 📊 Criar análise se os dados foram carregados corretamente
if df_vendas is not None and df_marketing is not None and df_meteorologia is not None:

    # 📌 Converter datas para datetime
    df_vendas["Data"] = pd.to_datetime(df_vendas["Data"], errors="coerce")
    df_marketing["Data"] = pd.to_datetime(df_marketing["Data"], errors="coerce")
    df_meteorologia["Data"] = pd.to_datetime(df_meteorologia["Data"], errors="coerce")

    # 📌 Converter valores numéricos corretamente
    df_vendas["Total Venda"] = pd.to_numeric(df_vendas["Total Venda"], errors="coerce")
    df_vendas["Quantidade"] = pd.to_numeric(df_vendas["Quantidade"], errors="coerce")
    df_marketing["Investimento (R$)"] = pd.to_numeric(df_marketing["Investimento (R$)"], errors="coerce")
    df_meteorologia["Temperatura Média (°C)"] = pd.to_numeric(df_meteorologia["Temperatura Média (°C)"], errors="coerce")

    # 📊 🔹 Analisar os produtos mais vendidos
    produtos_mais_vendidos = df_vendas.groupby("Produto").agg({"Quantidade": "sum", "Total Venda": "sum"}).reset_index()
    produtos_mais_vendidos = produtos_mais_vendidos.sort_values(by="Quantidade", ascending=False)

    print("\n📈 **Top 5 Produtos Mais Vendidos:**")
    print(produtos_mais_vendidos.head())

    # 📊 🔹 Analisar a estação do ano com mais vendas
    vendas_por_estacao = df_vendas.groupby("Estação").agg({"Quantidade": "sum", "Total Venda": "sum"}).reset_index()
    vendas_por_estacao = vendas_por_estacao.sort_values(by="Quantidade", ascending=False)

    print("\n🌦 **Vendas por Estação:**")
    print(vendas_por_estacao)

    # 📊 🔹 Analisar o investimento em marketing por estação
    investimento_por_estacao = df_marketing.groupby("Estação").agg({"Investimento (R$)": "sum"}).reset_index()
    investimento_por_estacao = investimento_por_estacao.sort_values(by="Investimento (R$)", ascending=False)

    print("\n💰 **Investimento em Marketing por Estação:**")
    print(investimento_por_estacao)

    # 📊 🔹 Analisar a temperatura média por estação
    temperatura_por_estacao = df_meteorologia.groupby("Estação").agg({"Temperatura Média (°C)": "mean"}).reset_index()
    temperatura_por_estacao = temperatura_por_estacao.sort_values(by="Temperatura Média (°C)", ascending=False)

    print("\n🌡 **Temperatura Média por Estação:**")
    print(temperatura_por_estacao)

    # 📊 🔹 Criar gráfico de barras para os produtos mais vendidos
    plt.figure(figsize=(10, 5))
    sns.barplot(x=produtos_mais_vendidos["Produto"], y=produtos_mais_vendidos["Quantidade"], palette="Blues_r")
    plt.xticks(rotation=45)
    plt.xlabel("Produto")
    plt.ylabel("Quantidade Vendida")
    plt.title("📦 Produtos Mais Vendidos")
    plt.show()

    # 📊 🔹 Criar gráfico de barras para vendas por estação
    plt.figure(figsize=(8, 5))
    sns.barplot(x=vendas_por_estacao["Estação"], y=vendas_por_estacao["Quantidade"], palette="viridis")
    plt.xlabel("Estação do Ano")
    plt.ylabel("Quantidade Vendida")
    plt.title("🌍 Vendas por Estação do Ano")
    plt.show()

    # 📊 🔹 Criar gráfico de barras para investimento em marketing por estação
    plt.figure(figsize=(8, 5))
    sns.barplot(x=investimento_por_estacao["Estação"], y=investimento_por_estacao["Investimento (R$)"], palette="magma")
    plt.xlabel("Estação do Ano")
    plt.ylabel("Investimento (R$)")
    plt.title("💰 Investimento em Marketing por Estação")
    plt.show()

    # 📊 🔹 Criar gráfico de linha para a temperatura média por estação
    plt.figure(figsize=(8, 5))
    sns.lineplot(x=temperatura_por_estacao["Estação"], y=temperatura_por_estacao["Temperatura Média (°C)"], marker="o", color="red")
    plt.xlabel("Estação do Ano")
    plt.ylabel("Temperatura Média (°C)")
    plt.title("🌡 Temperatura Média por Estação")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

else:
    print("❌ Erro no carregamento dos arquivos.")
