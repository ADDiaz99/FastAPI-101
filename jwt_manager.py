from jwt import encode, decode                      #jwt sirve para generar tokens de informacion que le demos                     

def create_token(data: dict): #con esta funcion creamos un token con la data del usuario en forma de diccionario (lo definimos en main, como email y password)
    token: str = encode(payload= data, key="secretkey", algorithm="HS256")
    return token

def validate_token(token:str) -> dict: #y con esta, decodificamos el token de arriba y lo comparamos con la key, para validar
    data: dict = decode(token, key="secretkey", algorithms=['HS256'])
    return data