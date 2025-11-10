from flask import Blueprint, render_template, request
# Importe o objeto 'db' e o modelo 'Registros'
from models.models import Registros, db 
from sqlalchemy import desc
from datetime import datetime, timedelta

notficacoes_route = Blueprint('Notificacoes', __name__, url_prefix='/notificacoes') 

@notficacoes_route.route('/')
def notificaoes_page():
    # Coleta os filtros da URL (que serão enviados pelo formulário HTML)
    data_inicial_str = request.args.get('data_inicial')
    data_final_str = request.args.get('data_final')
    alerta_filtro_str = request.args.get('alerta_filtro') # Pode ser '', '0', '1', '2'

    # 1. Inicia a consulta principal (para a aba 'Todas')
    query = Registros.query

    # 2. Aplica filtro de Nível de Alerta (se diferente de 'Todos' ou vazio)
    if alerta_filtro_str:
        try:
            alerta_int = int(alerta_filtro_str)
            # Filtra pelo nível de alerta exato
            query = query.filter(Registros.alerta == alerta_int)
        except ValueError:
            # Ignora filtro se o valor for inválido (deixa a query inalterada)
            pass

    # 3. Aplica filtro de Data Inicial (>= data)
    if data_inicial_str:
        try:
            # Converte a string YYYY-MM-DD para um objeto datetime
            data_inicial = datetime.strptime(data_inicial_str, '%Y-%m-%d')
            query = query.filter(Registros.timestamp >= data_inicial)
        except ValueError:
            pass

    # 4. Aplica filtro de Data Final (<= data)
    if data_final_str:
        try:
            # Para incluir o dia final completo na pesquisa:
            data_final = datetime.strptime(data_final_str, '%Y-%m-%d')
            # Garante que o filtro inclua registros até o final do dia
            data_final_com_hora = data_final + timedelta(days=1)
            query = query.filter(Registros.timestamp < data_final_com_hora)
        except ValueError:
            pass

    # 5. Executa a consulta principal, ordenada pela mais recente (TODAS as notificações filtradas)
    todas = query.order_by(desc(Registros.timestamp)).all()

    # 6. Deriva as listas 'Não Lidas' e 'Lidas' do resultado filtrado
    # Importante: A lista 'todas' já está filtrada por data e alerta, 
    # e agora separamos por status de alerta (0 vs. 1, 2)
    nao_lidas = [r for r in todas if r.alerta in [1, 2]]
    lidas = [r for r in todas if r.alerta == 0]

    return render_template(
        'notificacoes.html.j2',
        todas=todas,
        nao_lidas=nao_lidas,
        lidas=lidas,
        # Passa os filtros de volta para que o HTML possa pré-preencher
        data_inicial=data_inicial_str,
        data_final=data_final_str,
        alerta_filtro=alerta_filtro_str
    )


@notficacoes_route.route('/mark_read_all', methods=['POST'])
def mark_read_all():
    """
    Atualiza todos os registros ativos (alerta 1 ou 2) para o status de processado (alerta 0).
    """
    # ... (O código desta função permanece inalterado)
    try:
        Registros.query.filter(
            Registros.alerta.in_([1, 2])
        ).update({'alerta': 0})
        
        db.session.commit()
        
        return {'success': True}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}, 500