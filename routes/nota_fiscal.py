# No seu arquivo de rota (nota_fiscal_route.py)

from flask import Blueprint, request, render_template, jsonify
from models.models import Contrato, Produto, NotaFiscal, ContratoProduto, ControleGasto
from config_db import db
import traceback
from decimal import Decimal

nota_fiscal_route = Blueprint('nota_fiscal', __name__)

@nota_fiscal_route.route('/notafiscal/cadastro', methods=['GET', 'POST'])
def cadastro_nota_fiscal_page():
    if request.method == 'POST':
        try:
            data = request.get_json()

            if not data:
                return jsonify({"message": "Dados JSON não fornecidos"}), 400

            nome_nf = data.get('nome_nf')
            data_emissao = data.get('data_emissao')
            contrato_id = data.get('contrato_id')
            produtos_data = data.get('produtos', [])

            if not all([nome_nf, data_emissao, contrato_id, produtos_data]):
                return jsonify({"message": "Campos obrigatórios faltando."}), 400
            
            nf_existente = NotaFiscal.query.filter_by(nome_nf=nome_nf).first()
            if nf_existente:
                 return jsonify({"message": f"A Nota Fiscal com o nome {nome_nf} já está cadastrada."}), 409

            for prod_item in produtos_data:
                produto_id = prod_item.get('produto_id')
                quantidade_recebida = prod_item.get('quantidade_recebida')
                preco_unitario_nf = prod_item.get('preco_unitario_nf')
                
                # Calcular o total do item
                gasto_do_item = quantidade_recebida * preco_unitario_nf
                
                # Salva cada item na tabela de notas fiscais
                nova_nf_item = NotaFiscal(
                    nome_nf=nome_nf,
                    data_emissao=data_emissao,
                    contrato_id=contrato_id,
                    produto_id=produto_id,
                    quantidade_recebida=quantidade_recebida,
                    preco_unitario_nf=preco_unitario_nf
                )
                db.session.add(nova_nf_item)
                
                # Busca um registro existente para o par contrato/produto
                controle_gasto_item = ControleGasto.query.filter_by(
                    contrato_id=contrato_id,
                    produto_id=produto_id
                ).first()
                
                # Conversão para Decimal para evitar erros de tipo
                gasto_do_item_decimal = Decimal(str(gasto_do_item))
                quantidade_recebida_decimal = Decimal(str(quantidade_recebida))

                if controle_gasto_item:
                    # Se o registro existe, atualiza o total e a quantidade
                    controle_gasto_item.gasto_total += gasto_do_item_decimal
                    controle_gasto_item.quantidade += quantidade_recebida_decimal
                else:
                    # Se não existe, cria um novo registro
                    novo_controle = ControleGasto(
                        contrato_id=contrato_id,
                        produto_id=produto_id,
                        gasto_total=gasto_do_item_decimal,
                        quantidade=quantidade_recebida_decimal
                    )
                    db.session.add(novo_controle)
            
            db.session.commit()
            
            return jsonify({
                "message": "Nota Fiscal e produtos salvos com sucesso!"
            }), 201

        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

    if request.method == 'GET':
        todos_contratos = Contrato.query.order_by(Contrato.nome).all()
        return render_template('cadastro_nota_fiscal.html', contratos=todos_contratos)
    
    return jsonify({"message": "Método de requisição não suportado."}), 405

@nota_fiscal_route.route('/notafiscal/visualizar', methods=['GET'])
def visualizar_notas_fiscais_page():
    """
    Renderiza a página de visualização de notas fiscais.
    """
    todos_contratos = Contrato.query.order_by(Contrato.nome).all()
    return render_template('visualizar_nf.html', contratos=todos_contratos)


@nota_fiscal_route.route('/notafiscal/por_contrato/<int:contrato_id>', methods=['GET'])
def get_notas_fiscais_por_contrato(contrato_id):
    """
    Retorna uma lista de notas fiscais únicas para um contrato,
    agrupadas por nome e data.
    """
    try:
        # A consulta seleciona as colunas de nome e data, filtra pelo contrato,
        # e agrupa para garantir que cada nota fiscal apareça apenas uma vez na lista
        notas_fiscais = db.session.query(NotaFiscal.nome_nf, NotaFiscal.data_emissao)\
                                  .filter(NotaFiscal.contrato_id == contrato_id)\
                                  .group_by(NotaFiscal.nome_nf, NotaFiscal.data_emissao)\
                                  .all()
        
        if not notas_fiscais:
            return jsonify({"message": "Nenhuma nota fiscal encontrada para este contrato."}), 404
        
        lista_notas = []
        for nome_nf, data_emissao in notas_fiscais:
            lista_notas.append({
                'nome_nf': nome_nf,
                'data_emissao': data_emissao.strftime('%d/%m/%Y') # Formata a data para o Brasil
            })
            
        return jsonify(lista_notas)

    except Exception as e:
        print(f"Erro ao buscar notas fiscais: {e}")
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500
    
@nota_fiscal_route.route('/notafiscal/detalhes', methods=['POST'])
def visualizar_detalhes_nf():
    """
    Rota POST para visualizar os detalhes completos de uma nota fiscal.
    Recebe o nome_nf no corpo da requisição e renderiza a página de detalhes.
    """
    data = request.get_json()
    nome_nf = data.get('nome_nf')

    if not nome_nf:
        return jsonify({"message": "Nome da nota fiscal não fornecido."}), 400

    # Busca todos os registros da NF, pois cada linha na tabela é um produto
    itens_nf = NotaFiscal.query.filter_by(nome_nf=nome_nf).all()

    if not itens_nf:
        return jsonify({"message": "Nota fiscal não encontrada."}), 404

    # Pega os dados gerais da NF do primeiro item
    primeiro_item = itens_nf[0]
    contrato = Contrato.query.get(primeiro_item.contrato_id)
    
    produtos_recebidos = []
    total_geral = 0
    
    for item in itens_nf:
        produto_db = Produto.query.get(item.produto_id)
        valor_total_item = item.quantidade_recebida * item.preco_unitario_nf
        total_geral += valor_total_item
        
        produtos_recebidos.append({
            'nome_produto': produto_db.nome if produto_db else 'Desconhecido',
            'descricao_produto': produto_db.descricao if produto_db else '',
            'quantidade_recebida': item.quantidade_recebida,
            'preco_unitario_nf': item.preco_unitario_nf,
            'valor_total': valor_total_item
        })

    nf_data = {
        'nome_nf': primeiro_item.nome_nf,
        'data_emissao': primeiro_item.data_emissao.strftime('%d/%m/%Y'),
        'contrato_nome': contrato.nome if contrato else 'Desconhecido',
        'contrato_casa': contrato.casa if contrato else '',
        'contrato_tipo': contrato.tipo if contrato else '',
        'produtos': produtos_recebidos,
        'total_geral': total_geral
    }

    return render_template('detalhes_nf.html', nf_data=nf_data)