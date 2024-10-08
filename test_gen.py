import jwt
import datetime

# Chave secreta usada para assinar o token
SECRET_KEY = 'jwt-secret-key'  # Substitua pela sua chave secreta

def generate_jwt(payload, exp_minutes=300):
    """
    Gera um token JWT com o payload fornecido e uma data de expiração padrão de 30 minutos.
    
    Args:
        payload (dict): Dados que serão codificados no token JWT.
        exp_minutes (int): Tempo de expiração do token em minutos. Padrão é 30 minutos.
    
    Returns:
        str: Token JWT assinado.
    """
    # Adiciona a data de expiração ao payload
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_minutes)
    payload.update({"exp": expiration})

    # Gera o token JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

# Exemplo de uso:
if __name__ == "__main__":
    # Definindo um payload de exemplo
    payload = {
        "clientID": 'cliente_123',
        "alarmID": "teste"
    }

    # Gerando o token com o payload
    token = generate_jwt(payload)
    print("Token gerado:")
    print(token)
    
