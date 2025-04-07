import pandas as pd
import random
import faker
from datetime import datetime, timedelta
from google.colab import files

# Criar instância do Faker
fake = faker.Faker()

# Definição de produtos vendidos na loja Wave Surfboards
produtos_surf = [
    "Prancha de Surf", "Roupa de Neoprene", "Leash", "Deck de Prancha",
    "Capa de Prancha", "Cera para Prancha", "Rash Guard", "Óculos de Sol",
    "Boné", "Bermuda de Surf", "Camisa UV", "Chinelo", "Mochila Impermeável"
]

# Definição das estações do ano e impacto nas vendas
estacoes = {
    "Verão": 1.5,  # Aumento de 50% nas vendas
    "Primavera": 1.2,  # Aumento de 20% nas vendas
    "Outono": 0.8,  # Queda de 20% nas vendas
    "Inverno": 0.4  # Queda drástica de 60% nas vendas
}

# Criar listas para armazenar os dados
historico_vendas = []
dados_meteorologicos = []
campanhas_publicitarias = []

# Simular dados para cada dia do ano
data_inicial = datetime(2024, 1, 1)
data_final = datetime(2024, 12, 31)
data_atual = data_inicial

while data_atual <= data_final:
    mes = data_atual.month

    # Determinar a estação do ano
    if mes in [12, 1, 2]:
        estacao = "Verão"
        temperatura_base = 28
    elif mes in [3, 4, 5]:
        estacao = "Outono"
        temperatura_base = 22
    elif mes in [6, 7, 8]:
        estacao = "Inverno"
        temperatura_base = 15
    else:
        estacao = "Primavera"
        temperatura_base = 24

    # Ajustar fator sazonal
    fator_sazonal = estacoes[estacao]

    # Gerar dados meteorológicos diários
    temperatura = round(random.uniform(temperatura_base - 3, temperatura_base + 3), 1)
    precipitacao = round(random.uniform(10, 200) if estacao in ["Verão", "Outono"] else random.uniform(0, 50), 1)

    dados_meteorologicos.append({
        "Data": data_atual,
        "Estação": estacao,
        "Temperatura Média (°C)": temperatura,
        "Precipitação (mm)": precipitacao
    })

    # Gerar dados de vendas diárias
    num_vendas = random.randint(20, 100) if estacao in ["Verão", "Primavera"] else random.randint(5, 30)

    for _ in range(num_vendas):
        produto = random.choice(produtos_surf)
        quantidade = random.randint(1, 5)
        preco_unitario = round(random.uniform(100, 2000), 2)
        total_venda = round(preco_unitario * quantidade * fator_sazonal, 2)

        historico_vendas.append({
            "Data": data_atual,
            "Produto": produto,
            "Quantidade": quantidade,
            "Preço Unitário": preco_unitario,
            "Total Venda": total_venda,
            "Estação": estacao
        })

    # Gerar campanhas publicitárias mensais
    if data_atual.day == 1:  # Criar campanhas no primeiro dia de cada mês
        num_campanhas = random.randint(3, 6) if estacao in ["Verão", "Primavera"] else random.randint(1, 3)
        for _ in range(num_campanhas):
            campanhas_publicitarias.append({
                "Data": data_atual,
                "Estação": estacao,
                "Tipo de Campanha": random.choice(["Promoção de Verão", "Desconto Especial", "Sorteio", "Campanha Online"]),
                "Investimento (R$)": round(random.uniform(5000, 50000), 2)
            })

    # Avançar para o próximo dia
    data_atual += timedelta(days=1)

# Criar DataFrames
df_vendas = pd.DataFrame(historico_vendas)
df_meteorologia = pd.DataFrame(dados_meteorologicos)
df_campanhas = pd.DataFrame(campanhas_publicitarias)

# Salvar arquivos
arquivo_vendas = "historico_vendas_wave_surfboards.csv"
arquivo_meteorologia = "dados_meteorologicos_wave_surfboards.csv"
arquivo_campanhas = "campanhas_publicitarias_wave_surfboards.csv"

df_vendas.to_csv(arquivo_vendas, index=False)
df_meteorologia.to_csv(arquivo_meteorologia, index=False)
df_campanhas.to_csv(arquivo_campanhas, index=False)

# Fazer download dos arquivos
def download_arquivo(arquivo):
    files.download(arquivo)

download_arquivo(arquivo_vendas)
download_arquivo(arquivo_meteorologia)
download_arquivo(arquivo_campanhas)
