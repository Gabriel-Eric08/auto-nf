from flask import Blueprint, request, jsonify, render_template
from models.models import Contrato, Produto, ContratoProduto, ContratoLote, Lote, Registros, User
from config_db import db
from utils.validateLogin import validate_login_from_cookies
from utils.get_user import get_user_id_from_cookie

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
    lotes_ids = data.get('lotes_ids')
    tipo = data.get('tipo')

    if not nome or not lotes_ids or not tipo:
        return jsonify({"message": "Campos 'nome', 'lotes_ids' e 'tipo' são obrigatórios."}), 400

    try:
        existing_contrato = Contrato.query.filter_by(nome=nome).first()
        if existing_contrato:
            return jsonify({"message": f"Contrato com o nome '{nome}' já existe."}), 409

        # 1. Cria e adiciona o novo contrato
        new_contrato = Contrato(nome=nome, tipo=tipo)
        db.session.add(new_contrato)
        db.session.flush() # NECESSÁRIO: Gera o ID do novo contrato

        # 2. Cria as associações na tabela ContratoLote
        for lote_id in lotes_ids:
            contrato_lote_assoc = ContratoLote(contrato_id=new_contrato.id, lote_id=lote_id)
            db.session.add(contrato_lote_assoc)

        # --- Bloco de Log (Correções Aplicadas) ---
        usuario_id_cookie = get_user_id_from_cookie()
        user = User.query.filter_by(id=usuario_id_cookie).first()

        # Verifica o usuário para evitar erro 'None'
        nome_usuario = user.usuario if user else f"ID {usuario_id_cookie} (Não Encontrado)"
        
        mensagem_pre = f"Contrato de ID {new_contrato.id} salvo com sucesso pelo(a) usuário(a) {nome_usuario}."
        
        novo_registro = Registros(
            mensagem=mensagem_pre,
            # 'timestamp' é omitido para usar o default=db.func.now()
            usuario_id=usuario_id_cookie,
            tabela='contratos',
            id_linha=new_contrato.id,
            tipo_acao='CREATE',
            alerta=0
        )
        db.session.add(novo_registro)
        # O segundo db.session.flush() foi removido aqui.
        # --- Fim Bloco de Log ---

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