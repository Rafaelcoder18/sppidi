import jwt
import datetime

# Chave secreta usada para assinar o token
SECRET_KEY = 'sua_chave_secreta'  # Substitua pela sua chave secreta

def generate_jwt():
    # Dados a serem incluídos no token (payload)
    payload = {
        'sub': 'usuario_exemplo',  # Identificador do usuário
        'iat': datetime.datetime.utcnow(),  # Data de criação do token
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Data de expiração (1 dia)
    }
    
    # Gerar o token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    print("Token gerado com sucesso:")
    print(token)
    return token

if __name__ == "__main__":
    generate_jwt()
