from flask import Blueprint, request, jsonify, render_template
import pandas as pd
from models.models import Contrato, Produto, ContratoProduto, Lote, ContratoProdutoLote, Registros, User

from utils.get_user import get_username_from_cookie
from config_db import db
import io
import traceback

from services.user_service import UserService

user_service = UserService()

contrato_produto_route = Blueprint('contrato_produto', __name__)

@contrato_produto_route.route('/contratoproduto', methods=['GET'])
def contrato_produto_page():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    validate = user_service.validate_login(username,password)
    if validate:
        todos_contratos = Contrato.query.order_by(Contrato.nome).all()
        todos_lotes = Lote.query.order_by(Lote.nome_lote).all()
        return render_template('cadastro_contratoproduto.html.j2', 
                               contratos=todos_contratos, 
                               lotes=todos_lotes)
    else:
        return "Erro de autenticação. Por favor, faça login novamente."

def save_produtos_to_db(contrato_id, produtos_data, lote_id):
    """
    Função centralizada para salvar produtos no banco de dados,
    agora com registro de atividade.
    """
    
    # 1. OBTÉM O ID DO USUÁRIO LOGADO A PARTIR DO COOKIE
    user_id = get_username_from_cookie()
    if not user_id:
        # Nota: Retorna 401 aqui, mas idealmente, o tratamento de erro deveria 
        # garantir que 'user_id' seja int ou que a sessão seja fechada mais cedo.
        return jsonify({"message": "Erro de autenticação: ID de usuário logado não encontrado (via cookie)."}, 401)

    try:
        # Garante que os IDs são inteiros, se não forem None
        contrato_id = int(contrato_id)
        lote_id = int(lote_id)
        
        contrato_existente = Contrato.query.get(contrato_id)
        lote_existente = Lote.query.get(lote_id)

        if not contrato_existente:
            return jsonify({"message": "Contrato não encontrado."}), 404
        
        if not lote_existente:
            return jsonify({"message": "Lote não encontrado."}), 404

        # Busca o nome de usuário uma vez, fora do loop (melhor performance e legibilidade)
        user = User.query.get(user_id)
        nome_usuario = user.usuario if user else f"ID {user_id}"

        for prod_item in produtos_data:
            codigo_produto = prod_item.get('codigo_produto')
            descricao_produto = prod_item.get('descricao_produto', '')
            quantidade_max = prod_item.get('quantidade_max', 0)
            preco_unitario = prod_item.get('preco_unitario', 0.0)

            if not codigo_produto:
                db.session.rollback()
                return jsonify({"message": "Cada item de produto deve ter 'codigo_produto'."}), 400
            
            # Checagem de duplicidade (Contrato-Produto-Lote) - (Código omitido por brevidade)
            existing_assoc = db.session.query(ContratoProduto) \
                .join(Produto, ContratoProduto.produto_id == Produto.id) \
                .filter(ContratoProduto.contrato_id == contrato_id,
                        ContratoProduto.lote_id == lote_id,
                        Produto.nome == codigo_produto) \
                .first()
            
            if existing_assoc:
                db.session.rollback()
                return jsonify({"message": f"O produto '{codigo_produto}' já foi cadastrado para este contrato e lote."}), 409

            # Busca o produto existente ou cria um novo
            produto = Produto.query.filter_by(nome=codigo_produto).first()
            is_new_product = False
            if not produto:
                produto = Produto(nome=codigo_produto, descricao=descricao_produto)
                db.session.add(produto)
                db.session.flush()
                is_new_product = True

            # Cria a associação ContratoProduto
            contrato_produto = ContratoProduto(
                contrato_id=contrato_existente.id,
                produto_id=produto.id,
                lote_id=lote_existente.id,
                quantidade_max=quantidade_max,
                preco_unitario=preco_unitario
            )
            db.session.add(contrato_produto)
            db.session.flush() # CRÍTICO: Obtém o ID do ContratoProduto recém-criado
            
            # --- BLOC DE LOG CORRIGIDO 1: ContratoProduto ---
            # CORREÇÃO: Usar o nome do produto e do lote na mensagem para ser descritivo
            mensagem_contrato_produto = (
                f"Associação criada: O produto '{codigo_produto}' (ID: {produto.id}) foi vinculado "
                f"ao Contrato ID {contrato_id} e Lote '{lote_existente.nome_lote}' (ID: {lote_id}) "
                f"pelo usuário {nome_usuario}."
            )

            log_registro = Registros(
                mensagem=mensagem_contrato_produto,
                usuario_id=user_id, 
                tabela='contrato_produtos',
                id_linha=contrato_produto.id, 
                tipo_acao='CREATE_ASSOC', # Renomeado para ser mais específico
                alerta=0
            )
            db.session.add(log_registro)
            
            # --- BLOC DE LOG CORRIGIDO 2: Produto ---
            if is_new_product:
                mensagem_produto_novo = (
                    f"Produto novo criado: O código '{codigo_produto}' foi registrado na tabela 'produtos' "
                    f"pelo usuário {nome_usuario} para uso no Contrato ID {contrato_id}."
                )
                log_produto = Registros(
                    mensagem=mensagem_produto_novo, # Adicionando a mensagem
                    usuario_id=user_id,
                    tabela='produtos',
                    id_linha=produto.id, 
                    tipo_acao='CREATE_PROD',      # Adicionando tipo_acao
                    alerta=0                      # Adicionando alerta
                )
                db.session.add(log_produto)


        db.session.commit()
        return jsonify({
            "message": "Itens do contrato e lote associados com sucesso!",
            "contrato_id": contrato_existente.id
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar produtos: {e}")
        # traceback.print_exc() # Mantendo o traceback para depuração
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

# Rota para cadastro manual (recebe JSON)
@contrato_produto_route.route('/contratoproduto', methods=['POST'])
def add_contratoproduto():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados JSON não fornecidos"}), 400

    contrato_id = data.get('id')
    lote_id = data.get('lote_id') # Recebe o ID do lote
    produtos_data = data.get('produtos', [])

    return save_produtos_to_db(contrato_id, produtos_data, lote_id)

# Rota para upload de arquivos (recebe multipart/form-data)
@contrato_produto_route.route('/upload-contratoproduto', methods=['POST'])
def upload_contrato_produto():
    try:
        contrato_id = request.form.get('contrato_id')
        lote_id = request.form.get('lote_id') # Recebe o ID do lote do formulário
        uploaded_file = request.files.get('file')

        if not contrato_id or not uploaded_file or not lote_id:
            return jsonify({"message": "ID do contrato, lote ou arquivo não fornecido."}), 400

        filename = uploaded_file.filename
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(uploaded_file.stream.read().decode('utf-8')))
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file.stream, engine='openpyxl')
        else:
            return jsonify({"message": "Formato de arquivo não suportado. Use .csv ou .xlsx."}), 400
            
        produtos_data = []
        for index, row in df.iterrows():
            produtos_data.append({
                'codigo_produto': str(row.get('codigo_produto', '')),
                'descricao_produto': str(row.get('descricao_produto', '')),
                'quantidade_max': int(row.get('quantidade_max', 0)),
                'preco_unitario': float(row.get('preco_unitario', 0.0))
            })
        
        return save_produtos_to_db(contrato_id, produtos_data, lote_id)

    except Exception as e:
        db.session.rollback()
        print("--- OCORREU UM ERRO NO UPLOAD ---")
        traceback.print_exc()
        print("---------------------------------")
        return jsonify({"message": f"Erro no processamento do arquivo: {str(e)}"}), 500

# ROTA CORRIGIDA PARA FILTRAR POR CONTRATO E LOTE
@contrato_produto_route.route('/contratoproduto/visualizar', methods=['GET', 'POST'])
def visualizar_contrato_produto_page():
    username=request.cookies.get('username')
    password=request.cookies.get('password')

    validate = user_service.validate_login(username,password)
    if validate:
        todos_contratos = Contrato.query.order_by(Contrato.nome).all()
        todos_lotes = Lote.query.order_by(Lote.nome_lote).all()
        
        produtos_do_contrato = []
        contrato_selecionado = None
        lote_id_enviado = None
    
        if request.method == 'POST':
            # Recebe os IDs do contrato e do lote
            contrato_id = request.form.get('contrato_id')
            lote_id_enviado = request.form.get('lote_id') # Pode ser '' (Todos os Lotes) ou o ID

            if contrato_id:
                contrato_selecionado = Contrato.query.get(contrato_id)
                
                # Query para buscar a associação ContratoProduto, filtrada pelo LOTE_ID
                # Se você manteve lote_id em ContratoProduto, esta é a query correta agora.
                query = db.session.query(ContratoProduto, Produto, Lote) \
                                 .join(Produto, ContratoProduto.produto_id == Produto.id) \
                                 .join(Lote, ContratoProduto.lote_id == Lote.id) \
                                 .filter(ContratoProduto.contrato_id == contrato_id)
                
                # Aplica o filtro de lote se um lote específico foi selecionado
                if lote_id_enviado:
                    # Tenta converter para int e filtra
                    try:
                        lote_id = int(lote_id_enviado)
                        query = query.filter(ContratoProduto.lote_id == lote_id)
                    except ValueError:
                        # Se não for um ID válido, não filtra (trata como 'Todos os Lotes')
                        pass

                # Execute a query para obter os produtos. Note que a tabela ContratoProdutoLote foi removida do JOIN
                produtos_do_contrato = query.all() 

        return render_template('visualizar_contrato_produto.html.j2', 
                               contratos=todos_contratos,
                               lotes=todos_lotes,
                               produtos_contrato=produtos_do_contrato,
                               contrato_selecionado=contrato_selecionado,
                               # Passa o ID do lote enviado de volta para o template manter o select
                               lote_id_enviado=lote_id_enviado)
    else:
        return "Erro de autenticação. Por favor, faça login novamente."