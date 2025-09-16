import pandas as pd

# Caminhos para os seus arquivos
caminho_contrato = "contrato_fic.csv"
caminho_nf = "nf-1931.csv"
pd.set_option('display.max_columns', None)
try:
    # 1. Lê os DataFrames do contrato e da nota fiscal
    df_contrato = pd.read_csv(caminho_contrato, sep=';')
    df_nota_fiscal = pd.read_csv(caminho_nf, sep=';')
except FileNotFoundError:
    print("Erro: Verifique se os nomes dos arquivos estão corretos e se eles estão no mesmo diretório do seu script.")
    exit()

# 2. Renomeia as colunas de quantidade e código para padronizar
df_contrato.rename(columns={'Qtde': 'Quantidade', 'Codigo E-Fisco': 'Codigo'}, inplace=True)
df_nota_fiscal.rename(columns={'Qtd.': 'Quantidade', 'Código do Produto': 'Codigo'}, inplace=True)

# 3. Exibe os DataFrames lidos
print("--- DataFrame do Contrato ---")
print(df_contrato)

print("\n" + "="*50 + "\n")

print("--- DataFrame da Nota Fiscal ---")
print(df_nota_fiscal)

print("\n" + "="*50 + "\n")

# 4. Realiza a mesclagem com base na coluna de Código
# O 'how=left' garante que todos os itens do contrato sejam mantidos
df_restante = pd.merge(df_contrato, df_nota_fiscal, on='Codigo', how='left', suffixes=('_contrato', '_nf'))

# Preenche valores NaN (quando um produto da nota não está no contrato) com 0
df_restante['Quantidade_nf'] = df_restante['Quantidade_nf'].fillna(0)

# Calcula a quantidade restante no contrato
df_restante['Quantidade'] = df_restante['Quantidade_contrato'] - df_restante['Quantidade_nf']

# Remove as colunas temporárias e seleciona as colunas finais
df_restante = df_restante[['Items/Lotes', 'Codigo', 'Descrição', 'Unid.', 'Quantidade', 'Preço Unitário', 'Valor Normal']]

# 5. Exibe o DataFrame do estoque restante
print("--- DataFrame do Estoque Restante (Contrato - Nota Fiscal) ---")
print(df_restante)