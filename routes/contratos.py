from flask import Blueprint, request, jsonify
import pandas as pd


contrato_route = Blueprint('contrato', __name__)

@contrato_route.route('/contratos', methods=['GET'])
def contratos_page():
    return "Página de contratos"

@contrato_route.route('/contratos', methods=['POST'])
def add_contrato():
    data = request

    tipo = data.get('tipo')
    casa = data.get('casa')
    nome = data.get('nome')
    produtos = data.get('produtos', [])

# Array no padrão:
#[{"produto_id": 1, "quantidade_max": 10, "preco_unitario": 5.0}, {"produto_id": 1, "quantidade_max": 10, "preco_unitario": 5.0} ]

    json_to_pd = {"produtos": [], "quantidade_max": [], "preco_unitario": []}, 
    df_contratos = pd.DataFrame()