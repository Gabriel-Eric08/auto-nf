from flask import Blueprint, request, render_template, jsonify
from models.models import Contrato,User, Produto, Registros, NotaFiscal, ContratoProduto, ControleGasto, Lote, ContratoProdutoLote, ContratoLote
from config_db import db
import traceback
from decimal import Decimal
from utils.get_user import get_username_from_cookie
from utils.validateLogin import validate_login_from_cookies
from sqlalchemy import distinct

nota_fiscal_route = Blueprint('nota_fiscal', __name__)

@nota_fiscal_route.route('/notafiscal/cadastro', methods=['GET', 'POST']) 
def cadastro_nota_fiscal_page():
    """
    Rota para cadastrar uma nova Nota Fiscal (POST) e para renderizar 
    a página de seleção de contratos/lotes (GET).
    """
    # 1. Obtém o nome (string) do usuário logado (ex: 'biel')
    username_sessao = get_username_from_cookie()

    # Se a requisição for POST (salvar NF)
    if request.method == 'POST':
        try:
            data = request.get_json()

            if not data:
                return jsonify({"message": "Dados JSON não fornecidos"}), 400

            # --- CORREÇÃO DO ERRO 1366: BUSCA O ID NUMÉRICO DO USER ---
            user_obj = User.query.filter_by(usuario=username_sessao).first()
            if not user_obj:
                return jsonify({"message": f"Usuário '{username_sessao}' não encontrado no sistema."}), 401
            
            usuario_id_real = user_obj.id  # Agora temos o ID inteiro (ex: 1)
            # ---------------------------------------------------------

            nome_nf = data.get('nome_nf')
            data_emissao = data.get('data_emissao')
            contrato_id = data.get('contrato_id')
            lote_id = data.get('lote_id')
            produtos_data = data.get('produtos', [])

            if not all([nome_nf, data_emissao, contrato_id, lote_id, produtos_data]):
                return jsonify({"message": "Campos obrigatórios faltando."}), 400
            
            contrato_obj = Contrato.query.get(contrato_id)
            if not contrato_obj:
                return jsonify({"message": "Contrato não encontrado."}), 404
                
            if not ContratoLote.query.filter_by(contrato_id=contrato_id, lote_id=lote_id).first():
                return jsonify({"message": "O Lote selecionado não está associado ao Contrato."}), 400

            nf_existente = NotaFiscal.query.filter_by(nome_nf=nome_nf).first()
            if nf_existente:
                 return jsonify({"message": f"A Nota Fiscal {nome_nf} já está cadastrada."}), 409
            
            # --- Início do processamento dos itens ---
            for prod_item in produtos_data:
                produto_id = prod_item.get('produto_id')
                quantidade_recebida = Decimal(str(prod_item.get('quantidade_recebida', 0)))
                preco_unitario_nf = Decimal(str(prod_item.get('preco_unitario_nf', 0)))
                gasto_do_item = quantidade_recebida * preco_unitario_nf
                
                produto_obj = Produto.query.get(produto_id)
                produto_descricao = produto_obj.descricao if produto_obj else f"ID {produto_id}"

                # 1. Salva o item na NotaFiscal
                nova_nf_item = NotaFiscal(
                    nome_nf=nome_nf,
                    data_emissao=data_emissao,
                    contrato_id=contrato_id,
                    produto_id=produto_id,
                    lote_id=lote_id, 
                    quantidade_recebida=quantidade_recebida,
                    preco_unitario_nf=preco_unitario_nf
                )
                db.session.add(nova_nf_item)
                
                # 2. Atualiza ControleGasto
                controle_gasto_item = ControleGasto.query.filter_by(
                    contrato_id=contrato_id,
                    produto_id=produto_id
                ).first()
                
                if controle_gasto_item:
                    controle_gasto_item.gasto_total += gasto_do_item
                    controle_gasto_item.quantidade += quantidade_recebida
                    id_linha_controle = controle_gasto_item.id
                    tipo_acao = "CG_UPDATE_GASTO"
                else:
                    novo_controle = ControleGasto(
                        contrato_id=contrato_id,
                        produto_id=produto_id,
                        lote_id=lote_id, 
                        gasto_total=gasto_do_item,
                        quantidade=quantidade_recebida
                    )
                    db.session.add(novo_controle)
                    db.session.flush() 
                    id_linha_controle = novo_controle.id
                    tipo_acao = "CG_CREATE_GASTO"
                
                db.session.flush() 

                # 3. VERIFICAÇÃO DE ALERTA
                limite_produto = ContratoProduto.query.filter_by(
                    contrato_id=contrato_id, 
                    lote_id=lote_id,
                    produto_id=produto_id
                ).first()
                
                alerta = 0
                percentual_restante = 1.0
                if limite_produto and float(limite_produto.quantidade_max) > 0:
                    quantidade_max = float(limite_produto.quantidade_max)
                    qtd_atual = float(controle_gasto_item.quantidade if controle_gasto_item else novo_controle.quantidade)
                    percentual_restante = (quantidade_max - qtd_atual) / quantidade_max

                mensagem_alerta = f"Nota Fiscal '{nome_nf}' lançada para o Contrato '{contrato_obj.nome}' do produto '{produto_descricao}'."
                
                if percentual_restante <= 0.25:
                    alerta = 2
                    mensagem_alerta += f" ALERTA CRÍTICO: Restam {percentual_restante * 100:.2f}% do estoque!"
                elif percentual_restante <= 0.50:
                    alerta = 1
                    mensagem_alerta += f" ALERTA: Restam {percentual_restante * 100:.2f}% do estoque."

                # --- REGISTRO DE LOG COM O ID CORRETO ---
                novo_registro = Registros(
                    mensagem=mensagem_alerta,
                    usuario_id=usuario_id_real, # <--- AQUI ESTÁ A SOLUÇÃO
                    tabela="ControleGasto", 
                    id_linha=id_linha_controle,
                    tipo_acao=tipo_acao,
                    alerta=alerta
                )
                db.session.add(novo_registro)

            db.session.commit()
            return jsonify({"message": "Nota Fiscal e controle de gastos atualizados com sucesso!"}), 201

        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

    # Se a requisição for GET
    elif request.method == 'GET':
        validate = validate_login_from_cookies()
        if validate:
            todos_contratos = Contrato.query.order_by(Contrato.nome).all()
            lotes_por_contrato = {}
            
            contrato_lotes_db = db.session.query(ContratoLote, Lote)\
                                        .join(Lote, ContratoLote.lote_id == Lote.id)\
                                        .order_by(Lote.nome_lote)\
                                        .all()
            
            for cl, lote in contrato_lotes_db:
                if cl.contrato_id not in lotes_por_contrato:
                    lotes_por_contrato[cl.contrato_id] = []
                
                lotes_por_contrato[cl.contrato_id].append({
                    'id': int(lote.id), 
                    'nome_lote': lote.nome_lote,
                    'ano': lote.ano,
                    'casa': lote.casa
                })

            return render_template('cadastro_nota_fiscal.html.j2', 
                                    contratos=todos_contratos,
                                    lotes_map=lotes_por_contrato) 
        else:
            return "Erro de autenticação. Por favor, faça login novamente."

@nota_fiscal_route.route('/notafiscal/visualizar', methods=['GET'])
def visualizar_notas_fiscais_page():
# ... (manter o código inalterado) ...
    validate = validate_login_from_cookies()
    if validate:
        todos_contratos = Contrato.query.order_by(Contrato.nome).all()
        
        lotes_por_contrato = {}
        
        contrato_lotes_db = db.session.query(ContratoLote, Lote)\
                                     .join(Lote, ContratoLote.lote_id == Lote.id)\
                                     .order_by(Lote.nome_lote)\
                                     .all()
        
        for cl, lote in contrato_lotes_db:
            if cl.contrato_id not in lotes_por_contrato:
                lotes_por_contrato[cl.contrato_id] = []
            
            lotes_por_contrato[cl.contrato_id].append({
                'id': int(lote.id), 
                'nome_lote': lote.nome_lote,
                'ano': lote.ano,
                'casa': lote.casa
            })
            
        return render_template('visualizar_nf.html.j2', 
                                 contratos=todos_contratos,
                                 lotes_map=lotes_por_contrato) 
    else:
        return "Erro de autenticação. Por favor, faça login novamente."

# ROTA CRÍTICA: Ajustada o endpoint para a chamada do Frontend 
# e a query para filtro DUPLO e distinct.
@nota_fiscal_route.route('/notafiscal/por_contrato/<int:contrato_id>/<int:lote_id>', methods=['GET'])
def get_notas_fiscais_por_contrato_lote(contrato_id, lote_id):
# ... (manter o código inalterado) ...
    try:
        # Busca DISTINCT pelo nome_nf para listar a NF apenas uma vez
        notas_fiscais = db.session.query(distinct(NotaFiscal.nome_nf), NotaFiscal.data_emissao)\
                                 .filter(
                                     NotaFiscal.contrato_id == contrato_id,
                                     NotaFiscal.lote_id == lote_id 
                                 )\
                                 .order_by(NotaFiscal.data_emissao.desc())\
                                 .all()
        
        if not notas_fiscais:
            return jsonify([]), 200
        
        lista_notas = []
        for nome_nf, data_emissao in notas_fiscais:
            lista_notas.append({
                'nome_nf': nome_nf,
                'data_emissao': data_emissao.strftime('%d/%m/%Y') 
            })
            
        return jsonify(lista_notas)

    except Exception as e:
        print(f"Erro ao buscar notas fiscais: {e}")
        traceback.print_exc()
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500
    
    
@nota_fiscal_route.route('/notafiscal/detalhes', methods=['POST'])
def visualizar_detalhes_nf():
# ... (manter o código inalterado) ...
    validate = validate_login_from_cookies()
    if not validate:
        return "Erro de autenticação. Por favor, faça login novamente."
        
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
    lote = Lote.query.get(primeiro_item.lote_id) 
    
    produtos_recebidos = []
    total_geral = Decimal('0.00')
    
    for item in itens_nf:
        produto_db = Produto.query.get(item.produto_id)
        # Garante que as variáveis de cálculo sejam Decimais
        qtd = Decimal(str(item.quantidade_recebida))
        preco = Decimal(str(item.preco_unitario_nf))
        
        valor_total_item = qtd * preco
        total_geral += valor_total_item
        
        produtos_recebidos.append({
            'nome_produto': produto_db.nome if produto_db else 'Desconhecido',
            'descricao_produto': produto_db.descricao if produto_db else '',
            'quantidade_recebida': qtd,
            'preco_unitario_nf': preco,
            'valor_total': valor_total_item
        })

    nf_data = {
        'nome_nf': primeiro_item.nome_nf,
        'data_emissao': primeiro_item.data_emissao.strftime('%d/%m/%Y'),
        'contrato_nome': contrato.nome if contrato else 'Desconhecido',
        'contrato_tipo': contrato.tipo if contrato else '',
        
        # Dados do Lote
        'lote_nome': lote.nome_lote if lote else 'N/A',
        'lote_casa': lote.casa if lote else 'N/A',

        'produtos': produtos_recebidos,
        'total_geral': total_geral
    }

    return render_template('detalhes_nf.html.j2', nf_data=nf_data)

# ----------------------------------------------------------------------------------
# Rotas Auxiliares (Lógica de busca correta mantida)
# ----------------------------------------------------------------------------------

@nota_fiscal_route.route('/contrato/lotes_por_contrato/<int:contrato_id>', methods=['GET'])
def get_lotes_por_contrato(contrato_id):
# ... (manter o código inalterado) ...
    try:
        lotes_associados = db.session.query(Lote)\
                                     .join(ContratoLote, ContratoLote.lote_id == Lote.id)\
                                     .filter(ContratoLote.contrato_id == contrato_id)\
                                     .order_by(Lote.nome_lote)\
                                     .all()
        
        lotes_data = [{
            'id': int(lote.id), 
            'nome_lote': lote.nome_lote,
            'casa': lote.casa 
        } for lote in lotes_associados]
        
        return jsonify(lotes_data), 200
        
    except Exception as e:
        print(f"Erro ao buscar lotes: {e}")
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500
    
@nota_fiscal_route.route('/contrato/produtos_por_contrato_lote/<int:contrato_id>/<int:lote_id>', methods=['GET'])
def get_produtos_por_contrato_lote(contrato_id, lote_id):
# ... (manter o código inalterado) ...
    try:
        # Filtra diretamente na tabela ContratoProduto, pois ela JÁ CONTÉM o lote_id
        query = db.session.query(Produto, ContratoProduto) \
                             .join(ContratoProduto, ContratoProduto.produto_id == Produto.id) \
                             .filter(ContratoProduto.contrato_id == contrato_id,
                                     ContratoProduto.lote_id == lote_id) \
                             .order_by(Produto.nome)
        
        produtos_associados = query.all()
        
        if not produtos_associados:
            return jsonify([]), 200

        produtos_data = []
        for produto, cp in produtos_associados:
            # Busca a quantidade consumida para este par Contrato/Produto
            controle_gasto = ControleGasto.query.filter_by(
                contrato_id=contrato_id, 
                produto_id=produto.id
            ).first()
            
            quantidade_consumida = float(controle_gasto.quantidade) if controle_gasto else 0.0
            
            produtos_data.append({
                'id': int(produto.id),
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco_unitario': float(cp.preco_unitario),
                'quantidade_max': float(cp.quantidade_max), # Inclui o limite máximo
                'quantidade_consumida': quantidade_consumida # Inclui o que já foi consumido
            })
            
        return jsonify(produtos_data), 200
        
    except Exception as e:
        print("\n" + "#"*50)
        print(f"ERRO CRÍTICO no backend ao buscar produtos (GET): {e}")
        traceback.print_exc()
        print("#"*50 + "\n")
        
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500