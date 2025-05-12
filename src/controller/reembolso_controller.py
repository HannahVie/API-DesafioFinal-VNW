from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from flasgger import swag_from

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')

# GET: Listar todos os reembolsos
@bp_reembolso.route('/todos', methods=['GET'])
@swag_from('../docs/reembolso/listar_todos.yml')
def listar_todos_reembolsos():
    reembolsos = db.session.execute(
        db.select(Reembolso)
    ).scalars().all()

    lista_reembolsos = []
    for r in reembolsos:
        lista_reembolsos.append({
            "id": r.id,
            "colaborador": r.colaborador,
            "empresa": r.empresa,
            "tipo_reembolso": r.tipo_reembolso,
            "valor_faturado": str(r.valor_faturado),
            "status": r.status
        })

    return jsonify(lista_reembolsos), 200

# GET: Visualizar por número de prestação
@bp_reembolso.route('/prestacao/<int:num_prestacao>', methods=['GET'])
@swag_from('../docs/reembolso/visualizar_por_prestacao.yml')
def visualizar_por_num_prestacao(num_prestacao):
    reembolso = db.session.execute(
        db.select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)
    ).scalar()

    if reembolso:
        dados = reembolso.__dict__
        dados.pop('_sa_instance_state', None)
        return jsonify(dados), 200
    else:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

# POST: Solicitar um novo reembolso
@bp_reembolso.route('/solicitar', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados = request.get_json()

    # Campos obrigatórios
    campos_obrigatorios = ['colaborador', 'empresa', 'num_prestacao', 'tipo_reembolso',
                           'centro_custo', 'moeda', 'valor_faturado', 'id_colaborador']

    if not all(dados.get(campo) for campo in campos_obrigatorios):
        return jsonify({"mensagem": "Preencha todos os campos obrigatórios"}), 400

    try:
        novo_reembolso = Reembolso(
            colaborador=dados['colaborador'],
            empresa=dados['empresa'],
            num_prestacao=dados['num_prestacao'],
            descricao=dados.get('descricao'),
            data=dados.get('data'),
            tipo_reembolso=dados['tipo_reembolso'],
            centro_custo=dados['centro_custo'],
            ordem_interna=dados.get('ordem_interna'),
            divisao=dados.get('divisao'),
            pep=dados.get('pep'),
            moeda=dados['moeda'],
            distancia_km=dados.get('distancia_km'),
            valor_km=dados.get('valor_km'),
            valor_faturado=dados['valor_faturado'],
            despesa=dados.get('despesa'),
            id_colaborador=dados['id_colaborador']
        )

        db.session.add(novo_reembolso)
        db.session.commit()

        return jsonify({"mensagem": "Reembolso solicitado com sucesso"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500