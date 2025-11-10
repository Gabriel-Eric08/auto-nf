from flask import Blueprint, request, jsonify, render_template
from models.models import Produto, ContratoProduto, Registros
from config_db import db

from services.contrato_service import ContratoService
from services.contrato_lote_service import ContratoLoteService
from services.user_service import UserService
from services.registro_service import RegistroService
from services.lote_service import LoteService

contrato_service=ContratoService()
contrato_lote_service=ContratoLoteService()
user_service = UserService()
registro_service = RegistroService()
lote_service = LoteService()

contrato_route = Blueprint('contrato', __name__)

@contrato_route.route('/contratos', methods=['GET'])
def contratos_page():

    username = request.cookies.get('username')
    password = request.cookies.get('password')

    if not username or not password:
        return jsonify({
            "message": "Erro de autenticação"
        }), 401
    
    validate = user_service.validate_login(username, password)
    if validate:
        todos_contratos = contrato_service.get_all()
        todos_lotes = lote_service.get_all()
        
        return render_template('cadastro_contrato.html.j2', 
                               contratos=todos_contratos, 
                               lotes=todos_lotes)
    else:
        return "Erro de autenticação. Por favor, faça login novamente."


@contrato_route.route('/contratos/add_only', methods=['POST'])
def add_contrato_only():
    
    data = request.get_json()

    if not data:
        return jsonify({"message": "Dados JSON não fornecidos"}), 400

    nome = data.get('nome')
    lotes_ids = data.get('lotes_ids')
    tipo = data.get('tipo')
    data_inicial_str = data.get('data_inicial')
    data_final_str = data.get('data_final')

    if not nome or not lotes_ids or not tipo or not data_inicial_str or not data_final_str:
        return jsonify({"message": "Campos 'nome', 'lotes_ids', 'tipo', 'data_inicial' e 'data_final' são obrigatórios."}), 400

    try:

        existing_contrato = contrato_service.existing_contrato(nome)

        if existing_contrato:
            return jsonify({"message": f"Contrato com o nome '{nome}' já existe."}), 409

        # 1. Cria e adiciona o novo contrato com as datas
        new_contrato_id = contrato_service.add_contrato(data)
        contrato_lote_service.create_association(new_contrato_id, lotes_ids)

        # --- Bloco de Log (Mantido inalterado) ---
        username_cookie = request.cookies.get('username')
        user = user_service.get_user_by_name(username_cookie)

        if not user:
            return jsonify({
                "message": "Usuário não encontrado!"
            }), 401
        
        usuario_id = user.id

        nome_usuario = user.usuario if user else f"ID {usuario_id} (Não Encontrado)"
        
        # Criação de log
        mensagem_pre = f"Contrato de ID {new_contrato_id} salvo com sucesso pelo(a) usuário(a) {nome_usuario}. Vigência: {data_inicial_str} a {data_final_str}"
        registro_service.create_registro(mensagem_pre, usuario_id, new_contrato_id)

        return jsonify({
            "message": "Contrato criado com sucesso!",
            "contrato_id": new_contrato_id
        }), 201

    except ValueError:
        db.session.rollback()
        return jsonify({"message": "Formato de data inválido. Use o formato YYYY-MM-DD."}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar contrato: {e}")
        return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

@contrato_route.route('/contrato/produtos_por_contrato/<int:contrato_id>', methods=['GET'])
def get_produtos_por_contrato(contrato_id):
    
    lista_produtos = contrato_service.lista_produtos(contrato_id)

    if not lista_produtos:
        return jsonify({"message": "Nenhum produto encontrado para este contrato."}), 404

    return jsonify(lista_produtos)