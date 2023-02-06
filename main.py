# Projeto Indicius 02/05
import pandas as pd

# Retire os comentários para ler a tabela inteira.
#pd.set_option('display.max_rows', 10000)
#pd.set_option('display.max_columns', 1000)

# ================= #
# Funções de I/O    #
# ================= #

# Função que recupera os dados do arquivo CSV
def csv_fetch(path):
    database = pd.read_csv(path, sep = ",")
    return database

# Função que gurda os dados no arquivo CSV
def csv_commit(database):
    planilha = database.copy()
    #planilha['rowNumber'] = planilha.index
    #planilha = planilha["rowNumber","failure_type"]
    #planilha.columns = ['rowNumber', 'predictedValues']

    planilha = planilha["failure_type"]
    planilha.columns = ['rowNumber','predictedValues']
    planilha.index.name = 'rowNumber'
    planilha.to_csv('predicted.csv', index=True)
    #print(planilha)

# =================== #
# Funções de Analise  #
# =================== #

# Função que ajusta a tabela input com as falhas prováveis de acordo com o dicionário.
def define_failure_limits(database):
    database['failure_type'] = "No Failure"
    
    # Percorrer todas as tuplas procurando possíveis falhas
    for index, row in database.iterrows():
        
        # Falha: Tool Wear Failure
        if (tool_wear_failure(row['tool_wear_min']) == True):
            database.loc[index, 'failure_type'] = "Tool Wear Failure"
            continue

        # Falha: Heat Dissipation Failure
        if (heat_dissipation_failure(row["air_temperature_k"], row["process_temperature_k"], row["rotational_speed_rpm"]) == True):
            database.loc[index, 'failure_type'] = "Heat Dissipation Failure"
            continue

        # Falha: Power Failure
        if (power_failure(row['torque_nm'], row['rotational_speed_rpm']) == True):
            database.loc[index, 'failure_type'] = "Power Failure"
            continue

        # Falha: Overstrain Failure
        if (overstrain_failure(row['tool_wear_min'], row['torque_nm'], row['type']) == True):
            database.loc[index, 'failure_type'] = "Overstrain Failure"
            continue
        
        #print(index, row['udi'], row['failure_type'])
    return database

# ================= #
# Funções de Falha  #
# ================= #

def tool_wear_failure(twm):
    if (240 > twm > 200):
        #print("tool_wear_failure:", twm)
        return True
    return False

def heat_dissipation_failure(air_temp, proc_temp, rpm):
    diff = air_temp - proc_temp
    if ((diff < 8.6) and (rpm < 1380)):
        #print("heat_dissipation_failure:", diff, rpm)
        return True
    return False

def power_failure(torque, rpm):
    rads = 2 * 3.14 * rpm / 60
    power = torque * rads
    if ((power > 9000) or (power < 3500)):
        #print("power_failure:", power)
        return True
    return False

def overstrain_failure(twm, torque, types):
    product = twm * torque
    if (types == "L" and product > 11000):
        return True
    elif (types == "M" and product > 12000):
        return True
    elif (types == "H" and product > 13000):
        return True
    return False

# ================= #
# Função Principal  #
# ================= #

def main():
    print("Idêntificador de falhas, digite o nome do arquivo.csv, caso nenhum seja inserido, o padrão do Desafio será utilizado.")
    csv_name = input("Digite o nome:")

    if (csv_name == ""):
        dadosTest = csv_fetch("desafio_manutencao_preditiva_teste.csv")    
    else:
        dadosTest = csv_fetch(csv_name)    
    
    print("| < Processando... > |")
    dados_finais = define_failure_limits(dadosTest)

    csv_commit(dados_finais)
    print("< Finalizado >")
    print("Resultados guardados em predicted.csv")
    return

main()