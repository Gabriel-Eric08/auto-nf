from flask import Blueprint, request, jsonify, render_template
import pandas as pd
from models.models import Contrato, Produto, ContratoProduto
from config_db import db

contrato_produto_route = Blueprint('contrato_produto', __name__)

@contrato_produto_route.route('/contratoproduto', methods=['GET'])
def contrato_produto_page():
    # Busca todos os contratos para preencher o select
    todos_contratos = Contrato.query.order_by(Contrato.nome).all()
    return render_template('cadastro_contratoproduto.html', contratos=todos_contratos)

@contrato_produto_route.route('/contratoproduto', methods=['POST'])
def add_contratoproduto():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Dados JSON não fornecidos"}), 400

    contrato_id = data.get('id')
    produtos_data = data.get('produtos', [])

    if not contrato_id:
        return jsonify({"message": "Campo 'id' do contrato é obrigatório."}), 400
    if not produtos_data:
        return jsonify({"message": "Nenhum produto fornecido."}), 400

    try:
        # Busca o contrato existente pelo ID
        contrato_existente = Contrato.query.get(contrato_id)
        if not contrato_existente:
            return jsonify({"message": "Contrato não encontrado."}), 404

        # ---- NOVA CHECAGEM ----
        # Verifica se o contrato já possui produtos associados
        produtos_do_contrato_existentes = ContratoProduto.query.filter_by(contrato_id=contrato_id).first()
        if produtos_do_contrato_existentes:
            return jsonify({"message": "Este contrato já possui produtos cadastrados. Não é possível adicionar novos."}), 409

        for prod_item in produtos_data:
            codigo_produto = prod_item.get('codigo_produto')
            descricao_produto = prod_item.get('descricao_produto', '')
            quantidade_max = prod_item.get('quantidade_max', 0)
            preco_unitario = prod_item.get('preco_unitario', 0.0)
            
            if not codigo_produto:
                db.session.rollback()
                return jsonify({"message": "Cada item de produto deve ter 'codigo_produto'."}), 400

            # Busca o produto existente ou cria um novo
            produto = Produto.query.filter_by(nome=codigo_produto).first()
            if not produto:
                produto = Produto(nome=codigo_produto, descricao=descricao_produto)
                db.session.add(produto)
                db.session.flush()

            # Cria a associação ContratoProduto
            contrato_produto = ContratoProduto(
                contrato=contrato_existente,
                produto=produto,
                quantidade_max=quantidade_max,
                preco_unitario=preco_unitario
            )
            db.session.add(contrato_produto)

        db.session.commit()

        return jsonify({
            "message": "Contrato e produtos associados criados com sucesso!",
            "contrato_id": contrato_existente.id
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar contrato e produtos: {e}")
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500
    

@contrato_produto_route.route('/contratoproduto/visualizar', methods=['GET', 'POST'])
def visualizar_contrato_produto_page():
    """Renderiza a página para visualizar itens de contratos e processa a consulta."""
    
    todos_contratos = Contrato.query.order_by(Contrato.nome).all()
    produtos_do_contrato = []
    contrato_selecionado = None
    
    if request.method == 'POST':
        contrato_id = request.form.get('contrato_id')
        
        if contrato_id:
            # Encontra o contrato principal
            contrato_selecionado = Contrato.query.get(contrato_id)
            
            # Busca os itens do contrato e junta com os dados do produto
            produtos_do_contrato = db.session.query(ContratoProduto, Produto)\
                                            .join(Produto, ContratoProduto.produto_id == Produto.id)\
                                            .filter(ContratoProduto.contrato_id == contrato_id)\
                                            .all()

    # Retorna o template, passando os dados de todos os contratos,
    # os produtos do contrato selecionado (se houver), e o próprio contrato selecionado.
    return render_template('visualizar_contrato_produto.html', 
                           contratos=todos_contratos,
                           produtos_contrato=produtos_do_contrato,
                           contrato_selecionado=contrato_selecionado)