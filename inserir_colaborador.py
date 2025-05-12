from src.app import create_app
from src.model import db
from src.model.colaborador_model import Colaborador
from src.security.security import hash_senha

app = create_app()

with app.app_context():
    novo_colaborador = Colaborador(
        nome="Admin Teste",
        email="admin@teste.com",
        senha=hash_senha("senha123"),  # Senha com hash
        cargo="Administrador",
        salario=5000.00
    )

    db.session.add(novo_colaborador)
    db.session.commit()

    print("✅ Colaborador inserido com sucesso!")
