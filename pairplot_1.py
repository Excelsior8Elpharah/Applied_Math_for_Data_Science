import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files
import io
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer  # Para tratar valores ausentes

# 📌 Função para carregar arquivos
def carregar_arquivos():
    print("📂 Faça o upload de 3 arquivos CSV:")
    uploaded_files = files.upload()
    
    dataframes = []
    
    for nome_arquivo in uploaded_files.keys():
        try:
            df = pd.read_csv(io.BytesIO(uploaded_files[nome_arquivo]))
            print(f"✅ Arquivo '{nome_arquivo}' carregado! {df.shape[0]} linhas antes da limpeza.")
            
            # 🔹 Limpeza dos dados
            df.drop_duplicates(inplace=True)  # Remove duplicatas
            df.reset_index(drop=True, inplace=True)  # Reseta o índice
            
            print(f"✅ Arquivo '{nome_arquivo}' após limpeza: {df.shape[0]} linhas restantes.")
            dataframes.append(df)
        except Exception as e:
            print(f"⚠ Erro ao processar {nome_arquivo}: {e}")

    # 🔹 Unir todos os arquivos processados em um único dataframe
    if dataframes:
        df_final = pd.concat(dataframes, ignore_index=True)
        return df_final
    else:
        print("❌ Nenhum arquivo válido foi carregado.")
        return None

# 📌 Carregar e processar os arquivos
df_tratado = carregar_arquivos()

# 🔹 Se houver dados tratados, prosseguir com a análise
if df_tratado is not None:
    # 📌 Verificar colunas numéricas para análise
    colunas_numericas = df_tratado.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(colunas_numericas) < 2:
        print("❌ Não há colunas numéricas suficientes para análise de regressão.")
    else:
        # 📌 Imputação de valores NaN com a média
        imputer = SimpleImputer(strategy="mean")
        df_tratado[colunas_numericas] = imputer.fit_transform(df_tratado[colunas_numericas])
        
        # 📊 Análise de Regressão Linear
        x_col = colunas_numericas[0]  # Primeira variável independente
        y_col = colunas_numericas[1]  # Segunda variável dependente

        X = df_tratado[[x_col]].values  # Features
        y = df_tratado[y_col].values  # Target

        # 🔹 Divisão treino/teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 🔹 Modelo de regressão linear
        modelo = LinearRegression()
        modelo.fit(X_train, y_train)

        # 📌 Predições
        y_pred = modelo.predict(X_test)

        # 📊 Métricas de Avaliação
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"📈 Erro Quadrático Médio (MSE): {mse:.4f}")
        print(f"📈 Coeficiente de Determinação (R²): {r2:.4f}")

        # 📊 Gráfico de Dispersão - Correlação entre Variáveis
        sns.pairplot(df_tratado[colunas_numericas], diag_kind='kde')
        plt.show()
