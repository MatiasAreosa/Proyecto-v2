import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AERO-IA",
    page_icon="✈️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("✈ AERO-IA")
    st.caption("Agente de IA Aeronáutico")
    st.markdown("---")
    st.markdown("**Especialidades:**")
    st.markdown("- 🟢 Sabre GDS")
    st.markdown("- 🔵 Amadeus GDS")
    st.markdown("- 📊 Análisis de datos")
    st.markdown("- 📋 Reportes mensuales")
    st.markdown("- 🎟️ Tarifas & PNRs")
    st.markdown("- 💰 Revenue Management")
    st.markdown("---")
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Init agent
# ---------------------------------------------------------------------------
api_key = os.getenv("ANTHROPIC_API_KEY", "")
if not api_key or not api_key.startswith("sk-ant-"):
    st.error("⚠️ ANTHROPIC_API_KEY no configurada. Creá el archivo .env con tu API key.")
    st.stop()

if "agent" not in st.session_state:
    from agent.core import AirlineAgent
    st.session_state.agent = AirlineAgent(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
st.title("✈ AERO-IA")
st.caption("Consultá sobre vuelos, Sabre, Amadeus, tarifas, PNRs, reportes y revenue management")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("tools"):
            for tool in msg["tools"]:
                with st.expander(f"⚙️ {tool['name']}", expanded=False):
                    st.code(tool["result"], language=None)
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Preguntá algo... ej: 'Disponibilidad EZE-MAD 20MAY' o 'Reporte enero 2025'"):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            response_text, tool_outputs = st.session_state.agent.chat_web(prompt)

        if tool_outputs:
            for tool in tool_outputs:
                with st.expander(f"⚙️ {tool['name']}", expanded=False):
                    st.code(tool["result"], language=None)

        st.markdown(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "tools": tool_outputs,
    })
