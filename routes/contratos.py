from flask import Blueprint, request, jsonify, render_template
from models.models import Contrato, Produto, ContratoProduto, ContratoLote, Lote
from config_db import db
from utils.validateLogin import validate_login_from_cookies

contrato_route = Blueprint('contrato', __name__)

@contrato_route.route('/contratos', methods=['GET'])
def contratos_page():
    """
    Renderiza a página de cadastro de contratos e exibe os contratos existentes.
    Também busca os lotes para preencher o campo de seleção.
    """
    validate = validate_login_from_cookies()
    if validate == True:
        todos_contratos = Contrato.query.order_by(Contrato.nome).all()
        # Busque todos os lotes para o multiselect
        todos_lotes = Lote.query.order_by(Lote.nome_lote).all()
        
        return render_template('cadastro_contrato.html', 
                               contratos=todos_contratos, 
                               lotes=todos_lotes)
    else:
        return "Erro de autenticação. Por favor, faça login novamente."


@contrato_route.route('/contratos/add_only', methods=['POST'])
def add_contrato_only():
    """
    Salva um novo contrato no banco de dados com base nos dados JSON fornecidos.
    Agora lida com a associação de múltiplos lotes a um único contrato.
    """
    data = request.get_json()

    if not data:
        return jsonify({"message": "Dados JSON não fornecidos"}), 400

    nome = data.get('nome')
    lotes_ids = data.get('lotes_ids')  # Recebe a lista de IDs de lotes
    tipo = data.get('tipo')

    # Validação dos campos obrigatórios
    if not nome or not lotes_ids or not tipo:
        return jsonify({"message": "Campos 'nome', 'lotes_ids' e 'tipo' são obrigatórios."}), 400

    try:
        # Verifica se já existe um contrato com o mesmo nome
        existing_contrato = Contrato.query.filter_by(nome=nome).first()
        if existing_contrato:
            return jsonify({"message": f"Contrato com o nome '{nome}' já existe."}), 409

        # Cria e adiciona o novo contrato à sessão
        new_contrato = Contrato(nome=nome, tipo=tipo)
        db.session.add(new_contrato)
        db.session.flush() # Importante para gerar o ID do novo contrato antes de associar

        # Cria as associações na tabela ContratoLote
        for lote_id in lotes_ids:
            contrato_lote_assoc = ContratoLote(contrato_id=new_contrato.id, lote_id=lote_id)
            db.session.add(contrato_lote_assoc)

        db.session.commit()

        return jsonify({
            "message": "Contrato criado com sucesso!",
            "contrato_id": new_contrato.id
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar contrato: {e}")
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

@contrato_route.route('/contrato/produtos_por_contrato/<int:contrato_id>', methods=['GET'])
def get_produtos_por_contrato(contrato_id):
    """
    Retorna os produtos associados a um contrato específico.
    """
    produtos_do_contrato = db.session.query(ContratoProduto, Produto)\
                                 .join(Produto, ContratoProduto.produto_id == Produto.id)\
                                 .filter(ContratoProduto.contrato_id == contrato_id)\
                                 .all()
    
    if not produtos_do_contrato:
        return jsonify({"message": "Nenhum produto encontrado para este contrato."}), 404

    lista_produtos = []
    for cp, produto in produtos_do_contrato:
        lista_produtos.append({
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco_unitario': cp.preco_unitario
        })
    
    return jsonify(lista_produtos)