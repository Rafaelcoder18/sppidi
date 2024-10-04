import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Chave secreta usada para assinar o token
SECRET_KEY = 'sua_chave_secreta'  # Substitua pela sua chave secreta

def decode_jwt(token):
    try:
        # Decodificando o token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Token decodificado com sucesso:")
        print(decoded_token)
        return decoded_token
    except ExpiredSignatureError:
        print("O token expirou.")
    except InvalidTokenError:
        print("O token é inválido.")
    except Exception as e:
        print(f"Ocorreu um erro ao decodificar o token: {e}")

if __name__ == "__main__":
    # Exemplo de token JWT (substitua por um token real)
    token = input("Digite o token JWT a ser decodificado: ")

    # Decodificar e validar o token
    decode_jwt(token)
