# No seu arquivo controlegasto.py

from flask import Blueprint, request, render_template, jsonify
from models.models import Contrato, Produto, NotaFiscal, ContratoProduto, ControleGasto
from config_db import db
import traceback # Importa o módulo para rastreamento de erros

controle_gasto_route = Blueprint('controle_gasto', __name__)

@controle_gasto_route.route('/controle_gasto', methods=['GET'])
def controle_gasto_page():
    contratos = Contrato.query.all()
    return render_template('controle_gastos.html', controle_gastos=[], contratos=contratos)

@controle_gasto_route.route('/controle_gasto', methods=['POST'])
def controle_gasto_especifico():
    try:
        data = request.get_json()
        print(f"Dados recebidos do HTML: {data}")
        contrato_id = data.get('contrato_id')
        
        if not contrato_id:
            return jsonify({"error": "ID do contrato não fornecido"}), 400

        controle_gasto = []

        notas_empenho = ContratoProduto.query.filter_by(contrato_id=contrato_id).all()
        
        for ne in notas_empenho:
            valor_gasto = ControleGasto.query.filter_by(
                contrato_id=contrato_id, 
                produto_id=ne.produto_id
            ).first()

            print(f"Processando produto ID: {ne.produto_id} para o contrato ID: {contrato_id}")
            
            if valor_gasto:
                # Converter para float antes de enviar para o JSON
                quantidade_restante = float(ne.quantidade_max) - float(valor_gasto.quantidade)
                gasto_restante = (ne.quantidade_max * ne.preco_unitario) - float(valor_gasto.gasto_total)
                print(f"Gasto encontrado: Quantidade: {valor_gasto.quantidade}, Total: {valor_gasto.gasto_total}")
            else:
                quantidade_restante = float(ne.quantidade_max)
                gasto_restante = ne.quantidade_max * ne.preco_unitario
                print("Nenhum gasto encontrado para este item.")
            
            produto = Produto.query.filter_by(id=ne.produto_id).first()
            if produto:
                codigo_produto = produto.nome
                descricao_produto = produto.descricao
            else:
                codigo_produto = "Produto não encontrado"
                descricao_produto = ""
            
            nova_linha = {
                "codigo_produto": codigo_produto,
                "descricao": descricao_produto,
                "quantidade_restante": quantidade_restante,
                "valor_total_restante": gasto_restante
            }
            controle_gasto.append(nova_linha)

        return jsonify(controle_gasto)

    except Exception as e:
        print("--- OCORREU UM ERRO ---")
        traceback.print_exc()
        print("------------------------")
        return jsonify({"error": "Erro interno do servidor. Verifique o terminal para detalhes."}), 500

@controle_gasto_route.route('/get_contrato_details/<int:contrato_id>', methods=['GET'])
def get_contrato_details(contrato_id):
    contrato = Contrato.query.get(contrato_id)
    if contrato:
        return jsonify({
            'casa': contrato.casa,
            'tipo': contrato.tipo
        })
    return jsonify({"error": "Contrato não encontrado"}), 404