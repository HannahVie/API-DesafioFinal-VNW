from src.app import create_app
from src.model import db
from src.model.colaborador_model import Colaborador
from src.security.security import hash_senha

app = create_app()

with app.app_context():
    novo_colaborador = Colaborador(
        nome="Mari",
        email="Mariana@teste.com",
        senha=hash_senha("1234"),  # Senha com hash
        cargo="Administrador",
        salario=3000.00
    )

    db.session.add(novo_colaborador)
    db.session.commit()

    print("✅ Colaborador inserido com sucesso!")
