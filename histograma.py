import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

environmentType = os.environ.get('APP_ENV', 'production')

if environmentType == 'development':
    file_path = '.env/titanic.csv'
    print("--- Programa rodando em modo de desenvolvimento. ---")
else:
    file_path = ''

print(">> Digite o caminho do arquivo CSV:")

# Dados
if file_path == '':
    while True:
        try:
            file_path = input("> ")
            df = pd.read_csv(file_path)
            break
        except FileNotFoundError:
            print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        except Exception as e:
            print("Erro ao ler o arquivo:", e)
else:
    df = pd.read_csv(file_path)

# Select Coluna
mapCollum = {col.lower(): col for col in df.columns}

while True:
    try:
        print(">> Colunas disponíveis:", list(df.columns))
        print(">> Digite o nome da coluna que deseja analisar:")
        collum_input = input("> ").strip().lower()

        print(f">> Coluna selecionada: {mapCollum[collum_input]}")
        break
    except Exception as e:
        print("Erro ao selecionar coluna:", e)

# Numero de Colunas histograma (Bins)
binType = ['sturges', 'fd', 'auto']
bins = ''

while True:
    try:
        print(">> Digite o tipo de coluna ou quantidade de colunas a ser usada no histograma:",
        "(Sturges, FD para Freedman-Diaconis; Padrão: 'auto')")
        bins_input = input("> ").strip().lower()
        
        if not bins_input:
            bins = 'auto'
            print(">> Usando regra padrão: 'auto'")
            break
        elif bins_input in binType:
            bins = bins_input
            print(f">> Usando regra: '{bins_input}'")
            break
        else:
            bins = int(bins_input)
            print(f">> Usando número de colunas: {bins}")
            break            
    except ValueError:
        print("Por favor, insira uma regra ou um número inteiro válido.")
    except Exception as e:
        print("Erro ao ler entrada:", e)

# Gerar grafico
data = df[mapCollum[collum_input]].dropna().to_numpy()
print('Bins:', bins, 'data:', data)

plt.hist(data, bins=bins, edgecolor='black')
plt.tight_layout()
plt.show()

# Exportar grafico png
#plt.savefig(format="png")
#plt.close()

# Perguntar se quer recomeçar ou encerrar
while True:
    print(">> Deseja analisar outra coluna? (s/n)")
    restart_input = input("> ").strip().lower()
        
    if restart_input == 's':
        # Recomeçar o programa
        exec(open(__file__).read())
        break
    elif restart_input == 'n':
        print(">> Encerrando o programa.")
        break
    else:
        print("Por favor, responda com 's' para sim ou 'n' para não.")