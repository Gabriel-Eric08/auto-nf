from flask import Blueprint, request, jsonify
import pandas as pd
from models.models import Contrato, Produto, ContratoProduto
from config_db import db

contrato_route = Blueprint('contrato', __name__)

@contrato_route.route('/contratos', methods=['GET'])
def contratos_page():
    return "Página de contratos"

@contrato_route.route('/contratos', methods=['POST'])
def add_contrato():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Dados JSON não fornecidos"}), 400

    tipo = data.get('tipo')
    casa = data.get('casa')
    nome = data.get('nome')
    produtos_data = data.get('produtos', []) # Renomeado para evitar conflito com 'produtos' no loop

    # Validação básica dos dados de entrada
    if not nome or not casa or not tipo:
        return jsonify({"message": "Campos 'nome', 'casa' e 'tipo' são obrigatórios."}), 400

    try:
        # 1. Cria e adiciona o novo contrato à sessão
        new_contrato = Contrato(nome=nome, casa=casa, tipo=tipo)
        db.session.add(new_contrato)
        # db.session.flush() # Opcional: para obter o new_contrato.id antes do commit final

        for prod_item in produtos_data: # Usar um nome diferente para a variável do loop
            codigo_produto = prod_item.get('codigo_produto')
            descricao_produto = prod_item.get('descricao_produto', '')
            quantidade_max = prod_item.get('quantidade_max', 0)
            preco_unitario = prod_item.get('preco_unitario', 0.0)
        

            if not codigo_produto:
                db.session.rollback() # Desfaz tudo se um produto não tiver código
                return jsonify({"message": "Cada item de produto deve ter 'codigo_produto'."}), 400

            # 2. Busca o produto existente ou cria um novo
            produto = Produto.query.filter_by(nome=codigo_produto).first()
            if not produto:
                produto = Produto(nome=codigo_produto, descricao=descricao_produto) # Cria o novo produto
                db.session.add(produto) # Adiciona o novo produto à sessão
            
            # Uma forma mais idiomática com relationships configurados:
            new_contrato.produtos_do_contrato.append(
                ContratoProduto(
                    produto=produto, # Passa o objeto produto, não apenas o ID
                    quantidade_max=quantidade_max,
                    preco_unitario=preco_unitario
                )
            )

        db.session.commit() # Realiza o commit de todas as operações (contrato, produtos novos, associações)

        return jsonify({
            "message": "Contrato e produtos associados criados com sucesso!",
            "contrato_id": new_contrato.id
        }), 201 # HTTP 201 Created

    except Exception as e:
        db.session.rollback() # Desfaz todas as operações em caso de erro
        print(f"Erro ao criar contrato: {e}") # Para debug
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500