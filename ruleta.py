import streamlit as st
import random
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="Slot Machine Personalizada", layout="centered")

# 2. CONFIGURACIÓN DE MARCA Y ESTILOS
COLOR_MARCA = "#8cb744" 

st.markdown(f"""
    <style>
    .stApp {{ background-color: #f9fbf7; }}
    
    /* Botón Girar */
    div.stButton > button:first-child {{
        background-color: {COLOR_MARCA};
        color: white; border-radius: 10px; border: none;
        font-size: 20px; font-weight: bold; height: 3em; transition: 0.3s;
    }}
    div.stButton > button:hover {{ background-color: #7aa33b; border: none; }}

    /* Estilo de los Carretes */
    .reel {{
        background-color: #ffffff;
        border: 5px solid {COLOR_MARCA};
        border-radius: 15px;
        padding: 40px 10px;
        height: 150px;
        display: flex; align-items: center; justify-content: center;
        text-align: center; font-size: 25px; font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1); color: #333;
    }}

    .win-banner {{
        text-align: center; font-size: 40px; color: {COLOR_MARCA};
        font-weight: bold; margin-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN A GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

def registrar_en_sheets(nombre, email, premio):
    try:
        # 1. Leemos los datos actuales
        # Usamos un try/except por si la hoja está totalmente vacía
        try:
            df_existente = conn.read(worksheet="Sheet1")
        except:
            df_existente = pd.DataFrame(columns=["Nombre", "Email", "Premio", "Fecha"])

        # 2. Creamos la nueva fila
        nueva_fila = pd.DataFrame([{
            "Nombre": nombre,
            "Email": email,
            "Premio": premio,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        # 3. Concatenamos: los existentes PRIMERO, la nueva fila DESPUÉS
        # Aseguramos que no haya filas vacías que rompan el orden
        df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True).dropna(how='all')

        # 4. Actualizamos TODA la hoja con el nuevo DataFrame completo
        conn.update(worksheet="Sheet1", data=df_actualizado)
        
        st.toast("✅ ¡Datos guardados correctamente!")
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# 4. CABECERA
try:
    st.image("logo.png", width=200)
except:
    st.title("🎰 Bienvenido a nuestro Stand")

st.write("¡Ingresá tus datos para probar suerte en nuestra ruleta!")

# 5. FORMULARIO DE CAPTURA
with st.container():
    col_n, col_e = st.columns(2)
    with col_n:
        nombre_user = st.text_input("Nombre")
    with col_e:
        email_user = st.text_input("Email")

puedo_jugar = nombre_user != "" and "@" in email_user

# 6. LÓGICA DE JUEGO
premios = ["Regalo sorpresa", "Merch", "5% OFF", "10% OFF", "15% OFF"]
pesos = [5, 10, 25, 20, 10]
probabilidad_ganar = 0.3

# Botón de jugar (Se deshabilita si no completan los datos)
if st.button("¡PROBAR SUERTE!", use_container_width=True, disabled=not puedo_jugar):
    
    esta_ganando = random.random() < probabilidad_ganar

    if esta_ganando:
        resultado = random.choices(premios, weights=pesos, k=1)[0]
        r1, r2, r3 = resultado, resultado, resultado
    else:
        while True:
            r1, r2, r3 = random.choice(premios), random.choice(premios), random.choice(premios)
            if not (r1 == r2 == r3): break
        resultado = None

    # Animación de carretes
    col1, col2, col3 = st.columns(3)
    with col1: reel1 = st.empty()
    with col2: reel2 = st.empty()
    with col3: reel3 = st.empty()

    for t in range(35):
        v1 = random.choice(premios) if t < 15 else r1
        v2 = random.choice(premios) if t < 25 else r2
        v3 = random.choice(premios) if t < 34 else r3

        reel1.markdown(f'<div class="reel">{v1}</div>', unsafe_allow_html=True)
        reel2.markdown(f'<div class="reel">{v2}</div>', unsafe_allow_html=True)
        reel3.markdown(f'<div class="reel">{v3}</div>', unsafe_allow_html=True)
        time.sleep(0.04 + (t * 0.003))

    st.divider()
    
    # 7. RESULTADOS Y GUARDADO
    texto_final = resultado if resultado else "Siga participando"
    
    # Guardamos en Google Sheets
    registrar_en_sheets(nombre_user, email_user, texto_final)

    if esta_ganando:
        st.balloons()
        st.markdown(f'<div class="win-banner">✨ ¡FELICITACIONES! ✨</div>', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>Ganaste: {resultado}</h3>", unsafe_allow_html=True)
    else:
        st.markdown('<p style="text-align: center; font-size:20px; color: #666;">❌ No hubo coincidencia. ¡Seguí participando!</p>', unsafe_allow_html=True)
