import streamlit as st
import json
import re
import time
import requests
import urllib.parse

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA (ESTILO HACKER)
# ==========================================
st.set_page_config(
    page_title="OSINT MULTI-AHEAD SYSTEM",
    page_icon="🌐",
    layout="wide" # Cambiado a wide para ver múltiples columnas de resultados
)

st.markdown("""
    <style>
    .stApp { background-color: #0d0f12; color: #00ff66; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #1a1f26 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #00ff66 !important; color: #0d0f12 !important; font-weight: bold !important; border: 1px solid #00ff66 !important; box-shadow: 0px 0px 10px #00ff66; width: 100%; }
    h1, h2, h3 { color: #00ff66 !important; text-shadow: 0px 0px 8px #00ff66; }
    .terminal-box { background-color: #05070a; border: 1px dashed #00ff66; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; margin-bottom: 15px; }
    .source-header { color: #00ffff; font-weight: bold; border-bottom: 1px solid #00ffff; padding-bottom: 3px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# MÓDULOS DE RASTREO (LOGICA DE FUENTES)
# ==========================================

def buscar_en_redes_sociales(username_or_name):
    """Genera los enlaces de auditoría directa para perfiles en plataformas."""
    # Limpieza básica para generar un username probable si ponen nombre compuesto
    query_slug = username_or_name.lower().replace(" ", "")
    query_encoded = urllib.parse.quote(username_or_name)
    
    return {
        "instagram": f"https://www.instagram.com/{query_slug}/",
        "tiktok": f"https://www.tiktok.com/@{query_slug}",
        "facebook": f"https://www.facebook.com/search/top/?q={query_encoded}",
        "twitter_x": f"https://x.com/search?q={query_encoded}&f=user",
        "linkedin": f"https://www.linkedin.com/search/results/all/?keywords={query_encoded}"
    }

def generar_google_dorks(nombre, telefono, curp):
    """Automatiza la creación de dorks avanzados para indexación de fugas de datos."""
    dorks = []
    if nombre:
        dorks.append(f'intitle:"{nombre}" OR intext:"{nombre}"')
        dorks.append(f'filetype:pdf OR filetype:xlsx "{nombre}"')
    if telefono:
        dorks.append(f'intext:"{telefono}"')
    if curp:
        dorks.append(f'intext:"{curp}"')
        
    links_dorks = {}
    for i, dork in enumerate(dorks):
        links_dorks[f"Dork_Analisis_{i+1}"] = {
            "query": dork,
            "url_ejecucion": f"https://www.google.com/search?q={urllib.parse.quote(dork)}"
        }
    return links_dorks

def consultar_truecaller_api(numero, token):
    """Consulta estructurada del módulo Truecaller (Live/Simulado)."""
    if not token:
        time.sleep(0.5)
        return {"status": "Muestra local", "registrado": True, "posible_operador": "Movistar / Telcel"}
    
    url = f"https://search5-noneu.truecaller.com/v2/search?q={numero}&countryCode=MX&type=4"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "Truecaller/11.5.7 (Android;10)"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        return res.json() if res.status_code == 200 else {"error": f"HTTP {res.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# ==========================================
# INTERFAZ GRÁFICA INTERACTIVA
# ==========================================
st.text("""
OOOOOO
OO       OO
OO       OO  
OOOOOO
                        [ CREADO POR: J-I-A-M ]
""")

st.markdown("### 🌐 ENTORNO DE RECOLECCIÓN CENTRALIZADO")

with st.sidebar:
    st.markdown("### 🔑 CREDENCIALES DE ACCESO")
    st.write("Configura tus llaves de API si deseas análisis en tiempo real en sistemas cerrados.")
    tc_token = st.text_input("Truecaller Bearer Token", type="password", placeholder="Opcional...")
    st.markdown("---")
    st.info("💡 Consejo OSINT: Dejar los tokens vacíos ejecutará el script en modo de reconocimiento estructural y generador de dorks.")

# Formulario principal de búsqueda
with st.form(key='multi_search_form'):
    c1, c2, c3 = st.columns(3)
    with c1:
        nombre = st.text_input("Nombre Completo / Objetivo", placeholder="Ej. Juan Pérez López")
    with c2:
        telefono = st.text_input("Número Telefónico (10 dig)", placeholder="Ej. 5512345678")
    with c3:
        curp = st.text_input("Clave CURP", placeholder="Ej. ABCD123456HXXXXX01")
        
    submit = st.form_submit_button(label="⚡ DEPLOY MULTI-ENGINE SEARCH (CORRER ESCANEO GLOBAL)")

# Procesamiento global de resultados
if submit:
    if not nombre and not telefono and not curp:
        st.error("❌ Error en el despliegue: Requiere al menos un parámetro de entrada.")
    else:
        st.markdown("### 📊 INTEL LOGS - PANEL DE RESULTADOS CONSOLIDADOS")
        
        # Crear 3 columnas visuales para organizar el exceso de información
        col_redes, col_motores, col_telefonia = st.columns(3)
        
        # ----- COLUMNA 1: SOCIAL MEDIA INFERENCE -----
        with col_redes:
            st.markdown('<div class="source-header">📱 REDES SOCIALES (ENLACES DE AUDITORÍA)</div>', unsafe_allow_html=True)
            if nombre:
                with st.spinner("Mapeando alias en redes..."):
                    enlaces_sociales = buscar_en_redes_sociales(nombre)
                
                st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
                st.write("🟢 **Rastreador de perfiles listo:**")
                for red, url in enlaces_sociales.items():
                    st.markdown(f"🔹 **{red.upper()}:** [Abrir búsqueda de objetivo]({url})")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write("⚠️ Ingrese un Nombre para activar el módulo de Redes.")

        # ----- COLUMNA 2: GOOGLE ADVANCED DORKS -----
        with col_motores:
            st.markdown('<div class="source-header">🔍 GOOGLE DORKS (WEB ABIERTA)</div>', unsafe_allow_html=True)
            if nombre or telefono or curp:
                with st.spinner("Estructurando Dorks de búsqueda..."):
                    diccionario_dorks = generar_google_dorks(nombre, telefono, curp)
                
                st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
                st.write("🟢 **Fugas de datos e indexaciones públicas:**")
                st.write("Haz clic en los enlaces para forzar a Google a buscar archivos confidenciales:")
                for dork_name, info in diccionario_dorks.items():
                    st.markdown(f"🔸 **{dork_name}:** [Ejecutar dork en Google]({info['url_ejecucion']})")
                    st.code(info['query'], language="bash")
                st.markdown('</div>', unsafe_allow_html=True)

        # ----- COLUMNA 3: TELEPHONY & REPUTATION -----
        with col_telefonia:
            st.markdown('<div class="source-header">📞 MÓDULO TELEFÓNICO (TRUECALLER)</div>', unsafe_allow_html=True)
            if telefono:
                tel_limpio = re.sub(r'\D', '', telefono)
                if len(tel_limpio) == 10:
                    with st.spinner("Analizando base de datos Truecaller..."):
                        res_tc = consultar_truecaller_api(tel_limpio, tc_token)
                    
                    st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
                    st.write(f"🟢 **Respuesta del segmento +52 {tel_limpio}:**")
                    st.json(res_tc)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ Formato de teléfono inválido para el módulo.")
            else:
                st.write("⚠️ Ingrese un número telefónico para activar este bloque.")
