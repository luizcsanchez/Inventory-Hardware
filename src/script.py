import csv
import mysql.connector

localidade_atual = 'Barretos'

def ler_credenciais_arquivo(nome_arquivo):
    credenciais = {}
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            chave, valor = linha.strip().split(' = ')
            valor = valor.strip('"')
            credenciais[chave] = valor
    return credenciais

# Função para inserir os dados do CSV no banco de dados
def inserir_dados_csv(conn, nome_tabela, nome_arquivo_csv, localidade_atual):
    cursor = conn.cursor()
    with open(nome_arquivo_csv, 'r', encoding='utf-8-sig') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        # Pula o cabeçalho do CSV
        next(leitor_csv)
        for linha in leitor_csv:
            # Adiciona a localidade_atual à linha do CSV
            linha.append(localidade_atual)
            # Constrói a instrução SQL de inserção
            sql = f"INSERT INTO {nome_tabela} (Unidade, Tipo_de_unidade, Fabricante, Tipo_de_produto, Função, Versão_de_firmware, Endereço_IP, Endereço_físico, Fuso_horário, Usuário, Força_da_senha, Esquema_de_autenticação, Protocolo_de_segurança, Status_da_atualização, Próxima_atualização, Progresso_da_atualização, Motivo_para_falha_da_atualização, Versão_do_firmware_proposta, Descrição_proposta_do_firmware, Estado, Versão_da_plataforma, Versão_da_plataforma_proposta, Descrição_da_plataforma_proposta, Última_atualização_de_senha_bem_sucedida, Localidade_atual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # Executa a instrução SQL e passa os valores da linha atual do CSV
            cursor.execute(sql, tuple(linha))
        conn.commit()
    cursor.close()

# Lê as credenciais do arquivo
credenciais = ler_credenciais_arquivo('C:/Users/luizc/OneDrive/Documentos/inventory/Inventory-Hardware/credenciais.txt')

# Conecta ao MySQL
conn = mysql.connector.connect(
    host=credenciais['HOST_DB'],
    user=credenciais['USER_DB'],
    password=credenciais['PASS_DB'],
    database=credenciais['NAME_DB']
)

if conn.is_connected():
    print("Conectado ao MySQL!")
    # Nome da tabela onde você deseja inserir os dados
    nome_tabela = 'inventario'
    # Nome do arquivo CSV
    nome_arquivo_csv = 'C:/Users/luizc/OneDrive/Documentos/inventory/Inventory-Hardware/inventario/salvador.csv' 
    # Inserir os dados do CSV no banco de dados
    inserir_dados_csv(conn, nome_tabela, nome_arquivo_csv, localidade_atual)
else:
    print("Falha na conexão ao MySQL.")

# Fechar a conexão com o banco de dados
conn.close()
