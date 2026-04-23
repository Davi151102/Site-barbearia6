import streamlit as st
from datetime import datetime, date
import random

# Configuração de alta performance
st.set_page_config(page_title="BARGEND | Premium System", page_icon="✂️", layout="wide")

# --- DATABASE SIMULADO (Persistência na Sessão) ---
if 'agenda' not in st.session_state:
    st.session_state.agenda = []
if 'estoque' not in st.session_state:
    st.session_state.estoque = {
        "Pomada Efeito Matte": 15,
        "Shampoo Ice": 10,
        "Óleo Premium": 5,
        "Creme de Barbear": 8
    }

# --- CONFIGURAÇÕES TÉCNICAS ---
SENHA_ADM = "ramos657"
TELEFONE_DONO = "5531991927401"

UNIDADES = {
    "Unidade 1 - Bairro Ipê": {"endereco": "Rua Herculano Soares, 657", "barbeiros": ["Thailo", "Jefferson", "Junior"]},
    "Unidade 2 - Bairro Boa Vista": {"endereco": "Rua Elvira Augusta, 203", "barbeiros": ["Davi", "Cabral"]}
}

# --- ESTILO CSS CUSTOMIZADO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; }}
    .card {{ background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; }}
    .status-ok {{ color: #00ff00; font-weight: bold; }}
    .status-alerta {{ color: #ff0000; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.title("BARGEND")
    st.write("---")
    aba = st.radio("Navegação", ["📅 Agendar Horário", "❌ Cancelar/Ver Meu Horário", "🛍️ Loja & Estoque", "⚙️ Desenvolvedor"])

# ---------------------------------------------------------
# 1. ÁREA DE AGENDAMENTO (AUTOMÁTICO)
# ---------------------------------------------------------
if aba == "📅 Agendar Horário":
    st.title("Reserve seu Estilo")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            unidade = st.selectbox("Escolha a Unidade", list(UNIDADES.keys()))
            barbeiro = st.selectbox("Profissional", UNIDADES[unidade]["barbeiros"])
        with col2:
            data = st.date_input("Data", min_value=date.today())
            hora = st.selectbox("Horário", ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"])
        
        servico = st.selectbox("Serviço", ["Corte", "Barba", "Combo VIP", "Sobrancelha"])
        nome_cliente = st.text_input("Seu Nome Completo")

        if st.button("CONFIRMAR AGENDAMENTO AGORA"):
            if nome_cliente:
                # Gerar ID único para o cliente poder cancelar depois
                id_agendamento = random.randint(1000, 9999)
                novo_agendamento = {
                    "id": id_agendamento,
                    "cliente": nome_cliente,
                    "unidade": unidade,
                    "barbeiro": barbeiro,
                    "servico": servico,
                    "data": str(data),
                    "hora": hora
                }
                st.session_state.agenda.append(novo_agendamento)
                
                st.balloons()
                st.success(f"✅ AGENDADO COM SUCESSO! Guarde seu ID de cancelamento: {id_agendamento}")
                
                # Notificação para o dono (via WhatsApp link)
                msg_dono = f"NOVO AGENDAMENTO: {nome_cliente} | {servico} | {hora} na {unidade}. ID: {id_agendamento}"
                link_whats = f"https://wa.me/{TELEFONE_DONO}?text={msg_dono.replace(' ', '%20')}"
                st.markdown(f"[📲 Notificar Barbeiro agora]({link_whats})")
            else:
                st.error("Por favor, digite seu nome.")

# ---------------------------------------------------------
# 2. CANCELAMENTO (SEGURANÇA)
# ---------------------------------------------------------
elif aba == "❌ Cancelar/Ver Meu Horário":
    st.title("Gerenciar meu Agendamento")
    id_busca = st.number_input("Digite o ID do seu agendamento", min_value=0, step=1)
    nome_busca = st.text_input("Confirme seu nome completo")
    
    if st.button("BUSCAR E CANCELAR"):
        encontrado = False
        for i, agend in enumerate(st.session_state.agenda):
            if agend["id"] == id_busca and agend["cliente"].lower() == nome_busca.lower():
                st.session_state.agenda.pop(i)
                st.warning("Agendamento cancelado com sucesso.")
                encontrado = True
                break
        if not encontrado:
            st.error("Agendamento não encontrado ou dados incorretos.")

# ---------------------------------------------------------
# 3. LOJA & ESTOQUE
# ---------------------------------------------------------
elif aba == "🛍️ Loja & Estoque":
    st.title("BARGEND Store")
    for prod, qtd in st.session_state.estoque.items():
        with st.container():
            col_a, col_b = st.columns([3,1])
            col_a.write(f"### {prod}")
            if qtd > 0:
                col_a.write(f"Estoque disponível: {qtd}")
                if col_b.button(f"Comprar {prod}", key=prod):
                    st.session_state.estoque[prod] -= 1
                    st.success(f"Compra de {prod} realizada!")
                    if st.session_state.estoque[prod] <= 2:
                        st.error(f"AVISO: {prod} está quase acabando!")
            else:
                col_a.write("❌ ESGOTADO")

# ---------------------------------------------------------
# 4. ÁREA DO DESENVOLVEDOR (ADM)
# ---------------------------------------------------------
elif aba == "⚙️ Desenvolvedor":
    st.title("Painel Administrativo")
    acesso = st.text_input("Senha Master", type="password")
    
    if acesso == SENHA_ADM:
        st.success("Bem-vindo, Administrador.")
        
        tab1, tab2 = st.tabs(["📅 Agenda Geral", "📦 Gestão de Estoque"])
        
        with tab1:
            if not st.session_state.agenda:
                st.write("Nenhum agendamento para hoje.")
            for ag in st.session_state.agenda:
                st.markdown(f"""
                <div class="card">
                    <b>ID: {ag['id']} | Cliente: {ag['cliente']}</b><br>
                    {ag['servico']} com {ag['barbeiro']}<br>
                    {ag['data']} às {ag['hora']} - {ag['unidade']}
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            for prod, qtd in st.session_state.estoque.items():
                nova_qtd = st.number_input(f"Editar estoque: {prod}", value=qtd)
                st.session_state.estoque[prod] = nova_qtd
    elif acesso != "":
        st.error("Senha incorreta.")
