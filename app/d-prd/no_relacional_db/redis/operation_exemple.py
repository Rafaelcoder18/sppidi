import redis

# Conectar ao Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def create_value(key, value):
    """
    Cria um valor no Redis com a chave especificada.
    """
    client.set(key, value)
    print(f"CREATE: {key} -> {value}")

def read_value(key):
    """
    Lê o valor associado a uma chave no Redis.
    """
    value = client.get(key)
    if value:
        print(f"READ: {key} -> {value}")
    else:
        print(f"READ: A chave '{key}' não existe no Redis.")

def update_value(key, new_value):
    """
    Atualiza o valor de uma chave existente no Redis.
    """
    if client.exists(key):
        client.set(key, new_value)
        print(f"UPDATE: {key} -> {new_value}")
    else:
        print(f"UPDATE: A chave '{key}' não existe no Redis.")

def delete_value(key):
    """
    Remove uma chave e seu valor associado no Redis.
    """
    if client.exists(key):
        client.delete(key)
        print(f"DELETE: {key} removido com sucesso.")
    else:
        print(f"DELETE: A chave '{key}' não existe no Redis.")

if __name__ == "__main__":
    # Exemplo das operações CRUD

    # Criar (Create)
    create_value('nome', 'John Doe')
    create_value('idade', '30')
    
    # Ler (Read)
    read_value('nome')
    read_value('idade')
    
    # Atualizar (Update)
    update_value('idade', '31')
    read_value('idade')  # Lendo novamente para verificar a atualização
    
    # Deletar (Delete)
    delete_value('nome')
    read_value('nome')  # Tentando ler uma chave deletada
