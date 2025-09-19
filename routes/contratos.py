from flask import Blueprint, request, jsonify, render_template
import pandas as pd
from models.models import Contrato, Produto, ContratoProduto
from config_db import db

contrato_route = Blueprint('contrato', __name__)

@contrato_route.route('/contratos', methods=['GET'])
def contratos_page():
    todos_contratos = Contrato.query.order_by(Contrato.nome).all()
    # Passa a lista de contratos para o template
    return render_template('cadastro_contrato.html', contratos=todos_contratos)


@contrato_route.route('/contratos/add_only', methods=['POST'])
def add_contrato_only():
    """
    Salva um novo contrato no banco de dados com base nos dados JSON fornecidos.
    A verificação de duplicação do nome do contrato é realizada antes do salvamento.
    """
    data = request.get_json()

    if not data:
        return jsonify({"message": "Dados JSON não fornecidos"}), 400

    nome = data.get('nome')
    casa = data.get('casa')
    tipo = data.get('tipo')

    # Validação dos campos obrigatórios
    if not nome or not casa or not tipo:
        return jsonify({"message": "Campos 'nome', 'casa' e 'tipo' são obrigatórios."}), 400

    try:
        # Verifica se já existe um contrato com o mesmo nome
        existing_contrato = Contrato.query.filter_by(nome=nome).first()
        if existing_contrato:
            return jsonify({"message": f"Contrato com o nome '{nome}' já existe."}), 409 # 409 Conflict

        # Cria e adiciona o novo contrato à sessão
        new_contrato = Contrato(nome=nome, casa=casa, tipo=tipo)
        db.session.add(new_contrato)
        db.session.commit()

        return jsonify({
            "message": "Contrato criado com sucesso!",
            "contrato_id": new_contrato.id
        }), 201 # 201 Created

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar contrato: {e}")
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

@contrato_route.route('/contrato/produtos_por_contrato/<int:contrato_id>', methods=['GET'])
def get_produtos_por_contrato(contrato_id):
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