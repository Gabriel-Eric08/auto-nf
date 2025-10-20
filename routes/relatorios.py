from flask import Blueprint, render_template, request
from config_db import db
from models.models import ContratoProduto, Contrato, Lote, ControleGasto, Produto, ContratoLote, NotaFiscal
# Assumindo que você tem uma tabela de associação ou relacionamento para ligar Contrato a Lote
# Se não usar uma tabela de associação, você precisará adaptar a rota GET.
from sqlalchemy.orm import joinedload 

# Certifique-se de que 'ContratoLote' está no seu models.py se você usa uma tabela de associação
# Se não for uma tabela de associação, o Contrato deve ter uma propriedade .lotes (relacionamento)
# Exemplo de importação se fosse necessário: from models.models import ContratoLote

relatorios_route = Blueprint('Relatorio', __name__, url_prefix='/relatorio')

# ----------------------------------------------------------------------
# ROTA 1: RENDERIZAÇÃO DA PÁGINA (MÉTODO GET)
# ----------------------------------------------------------------------
@relatorios_route.route('/', methods=['GET'])
def visualizar_relatorio_page():
    # Otimização: Carrega os objetos de Lote junto com o ContratoLote
    contratos = Contrato.query.options(
        db.joinedload(Contrato.lotes_associados).joinedload(ContratoLote.lote)
    ).all()
    
    lotes_map = {}
    
    # Itera sobre os Contratos
    for contrato in contratos:
        lotes_data = []
        
        # 💡 CORREÇÃO AQUI: Itera sobre a lista de objetos ContratoLote
        for associacao in contrato.lotes_associados:
            lote_obj = associacao.lote
            
            # Garante que o lote foi carregado
            if lote_obj:
                lotes_data.append({
                    'id': lote_obj.id,
                    'nome_lote': lote_obj.nome_lote, # Nome puro para o POST
                    'ano': lote_obj.ano,
                    'casa': lote_obj.casa
                })
        
        # A chave do mapa continua sendo o ID do Contrato (inteiro)
        lotes_map[contrato.id] = lotes_data

    # Renderiza o template
    return render_template(
        'relatorio_geral_gasto.html', 
        contratos=contratos, 
        lotes_map=lotes_map
    )


# ----------------------------------------------------------------------
# ROTA 2: PROCESSAMENTO DOS DADOS (MÉTODO POST)
# ----------------------------------------------------------------------
@relatorios_route.route('/', methods=['POST'])
def relatorio_geral_gasto():
    data = request.get_json()
    
    if not data:
        return {"erro": "Dados JSON ausentes ou mal formatados."}, 400
    
    contrato = data.get('contrato')
    lote = data.get('lote') # Espera o nome puro do lote

    # =======================================================
    # 💡 CÓDIGO DE DEPURAÇÃO (Verifique o terminal do servidor)
    # =======================================================
    print("-----------------------------------------")
    print(f"DEBUG B/E: Recebido Contrato: {contrato}")
    print(f"DEBUG B/E: Recebido Lote: {lote}")
    print("-----------------------------------------")
    # =======================================================
    
    # Busca os objetos pelo NOME, conforme enviado pelo JS
    contrato_obj = Contrato.query.filter_by(nome=contrato).first()
    lote_obj = Lote.query.filter_by(nome_lote=lote).first()

    if not contrato_obj or not lote_obj:
        print("DEBUG B/E: Contrato ou Lote NÃO encontrado. Retornando 404.")
        return {"erro": "Contrato ou Lote não encontrado."}, 404
        
    print(f"DEBUG B/E: Contrato ID: {contrato_obj.id}, Lote ID: {lote_obj.id}. Buscando estoque.")

    # Busca principal (ContratoProduto)
    # Tente otimizar usando 'joinedload' se os relacionamentos estiverem configurados.
    estoque = ContratoProduto.query.filter_by(
        contrato_id=contrato_obj.id, 
        lote_id=lote_obj.id
    ).all()

    tabela_relatorio = [] 

    for linha in estoque:
        # Acessa os objetos relacionados ou faz a busca explícita se o relacionamento falhar
        produto_linha = getattr(linha, 'produto', Produto.query.filter_by(id=linha.produto_id).first())
        lote_linha = getattr(linha, 'lote', Lote.query.filter_by(id=linha.lote_id).first())
        
        if not produto_linha or not lote_linha:
             print(f"DEBUG B/E: Alerta! Produto ID {linha.produto_id} ou Lote ID {linha.lote_id} não encontrado, ignorando linha.")
             continue 
        
        # Busca em ControleGasto
        item_gasto = ControleGasto.query.filter_by(
            contrato_id=linha.contrato_id, 
            produto_id=linha.produto_id,
            lote_id=linha.lote_id 
        ).first()

        try:
            # Garante que os valores são floats para cálculo
            valor_total = float(linha.quantidade_max) * float(linha.preco_unitario)
            
            # Define os valores de gasto de forma segura (tratando None)
            gasto_qtd = float(item_gasto.quantidade) if item_gasto and item_gasto.quantidade is not None else 0.0
            gasto_valor = float(item_gasto.gasto_total) if item_gasto and item_gasto.gasto_total is not None else 0.0

            nova_linha = {
                "Cód. Prod.": produto_linha.nome,
                "Desc.": produto_linha.descricao,
                "Lote": lote_linha.nome_lote,
                "Qtd.Total": linha.quantidade_max,
                "Valor Unt": linha.preco_unitario,
                "Valor Total": valor_total,
                "Qtd. Gasta": gasto_qtd,
                "Valor Gasto": gasto_valor
            }
            
            tabela_relatorio.append(nova_linha)
        
        except Exception as e:
            # Captura erros de conversão de tipo (ex: DB NULL em campo float/int)
            print(f"DEBUG B/E: ERRO DE PROCESSAMENTO (Linha ID: {getattr(linha, 'id', 'N/A')}): {e}")
            # Você pode optar por continuar o loop ou retornar um erro. Aqui, continuamos.

    print(f"DEBUG B/E: Relatório concluído. Total de linhas: {len(tabela_relatorio)}")
    return {
        "status": "Relatório geral de gasto gerado com sucesso!", 
        "data": tabela_relatorio
    }, 200

@relatorios_route.route('/consumo-por-periodo-api')
def consumo_por_periodo():
    data = request.get_json()
    data_inicial = data['data_inicial']
    data_final = data['data_final']   

    notas_fiscais_filtradas = NotaFiscal.query.filter_by()
    controle_gasto =0