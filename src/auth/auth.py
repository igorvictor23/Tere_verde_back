from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher


pwd = PasswordHash((BcryptHasher(),))

def senha_criptografada(senha):
    return pwd.hash(senha)

def verifica_senha(senha_enviada,senha_banco):
    return pwd.verify(senha_enviada,senha_banco)




