# No seu arquivo controlegasto.py

from flask import Blueprint, request, render_template, jsonify
# Importamos ContratoLote (assumindo que você o criou)
from models.models import Contrato, Produto, NotaFiscal, ContratoProduto, ControleGasto, ContratoLote 
from config_db import db
import traceback 

# Importe a função de validação de cookies
from utils.validateLogin import validate_login_from_cookies

controle_gasto_route = Blueprint('controle_gasto', __name__)

@controle_gasto_route.route('/controle_gasto', methods=['GET'])
def controle_gasto_page():
    validate = validate_login_from_cookies()
    if validate:
        contratos = Contrato.query.all()
        
        lotes_map = {}
        for contrato in contratos:
            # Acessamos os lotes associados através do relacionamento 'lotes_associados'
            lotes_do_contrato = ContratoLote.query.filter_by(contrato_id=contrato.id).all()
            
            lotes_map[contrato.id] = [
                {
                    'id': assoc.lote_id, 
                    'nome_lote': assoc.lote.nome_lote, # 💡 CORREÇÃO AQUI: Acessa o objeto Lote
                    'casa': assoc.lote.casa,           # 💡 CORREÇÃO AQUI: Acessa o objeto Lote
                    'ano': assoc.lote.ano              # 💡 CORREÇÃO AQUI: Acessa o objeto Lote
                }
                for assoc in lotes_do_contrato
            ]

        contratos_data = [{'id': c.id, 'nome': c.nome, 'tipo': c.tipo} for c in contratos]

        return render_template('controle_gastos.html', 
                               controle_gastos=[], 
                               contratos=contratos_data, 
                               lotes_map=lotes_map)
    else:
        return "Erro de autenticação. Por favor, faça login novamente."

@controle_gasto_route.route('/controle_gasto', methods=['POST'])
def controle_gasto_especifico():
    try:
        data = request.get_json()
        print(f"Dados recebidos do HTML: {data}")
        contrato_id = data.get('contrato_id')
        lote_id = data.get('lote_id') # 💡 Novo parâmetro
        
        if not contrato_id or not lote_id:
            return jsonify({"error": "ID do contrato e do lote são obrigatórios."}), 400

        controle_gasto = []

        # 💡 Filtrar ContratoProduto por contrato_id E lote_id
        # Assumindo que a tabela ContratoProduto agora possui a coluna lote_id
        notas_empenho = ContratoProduto.query.filter_by(
            contrato_id=contrato_id, 
            lote_id=lote_id
        ).all()
        
        for ne in notas_empenho:
            # 💡 Filtrar ControleGasto por contrato_id, lote_id E produto_id
            # Assumindo que a tabela ControleGasto agora possui a coluna lote_id
            valor_gasto = ControleGasto.query.filter_by(
                contrato_id=contrato_id, 
                lote_id=lote_id, 
                produto_id=ne.produto_id
            ).first()

            print(f"Processando produto ID: {ne.produto_id} para o Contrato {contrato_id} e Lote {lote_id}")
            
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

# 💡 A rota get_contrato_details está obsoleta, pois Casa e Tipo são exibidos pelo JS/Jinja
# A informação Casa e Tipo agora será buscada do lote selecionado, para padronização. 
@controle_gasto_route.route('/get_contrato_details/<int:contrato_id>', methods=['GET'])
def get_contrato_details(contrato_id):
    # Rota mantida, mas pode ser removida se o frontend usar apenas o lote_map
    validate = validate_login_from_cookies()
    if not validate:
        return jsonify({"error": "Erro de autenticação"}), 401

    contrato = Contrato.query.get(contrato_id)
    if contrato:
        # Assumindo que o Contrato ainda pode ter a coluna 'tipo'
        return jsonify({
            'tipo': contrato.tipo if hasattr(contrato, 'tipo') else 'N/A'
        })
    return jsonify({"error": "Contrato não encontrado"}), 404