from flask_bcrypt import bcrypt

def hash_senha(senha):
    salt = bcrypt.gensalt()  # Gerando o salt
    return bcrypt.hashpw(senha.encode("UTF-8"), salt)

def checar_senha(senha, senha_hash):
    """
    Verifica se a senha em texto corresponde ao hash armazenado (em formato string).
    
    :param senha: Senha em texto plano (ex: '1234')
    :param senha_hash: Hash da senha armazenado no banco (string)
    :return: True se a senha estiver correta, False caso contrário
    """
    return bcrypt.checkpw(senha.encode("UTF-8"), senha_hash.encode("UTF-8"))
