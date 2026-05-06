import streamlit as st
import random
import time

# Configuración visual de la página
st.set_page_config(page_title="Slot Machine Personalizada", layout="centered")

# --- CONFIGURACIÓN DE MARCA ---
COLOR_MARCA = "#8cb744"  # Tu verde específico

st.markdown(f"""
    <style>
    /* Fondo de la página y tipografía */
    .stApp {{
        background-color: #f9fbf7;
    }}

    /* Botón personalizado con tu verde */
    div.stButton > button:first-child {{
        background-color: {COLOR_MARCA};
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 20px;
        font-weight: bold;
        height: 3em;
        transition: 0.3s;
    }}

    div.stButton > button:hover {{
        background-color: #7aa33b; /* Un verde un poco más oscuro para el hover */
        color: white;
        border: none;
    }}

    /* Carrete con bordes de tu marca */
    .reel {{
        background-color: #ffffff;
        border: 5px solid {COLOR_MARCA};
        border-radius: 15px;
        padding: 40px 10px;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        color: #333;
    }}

    .win-banner {{
        text-align: center;
        font-size: 40px;
        color: {COLOR_MARCA};
        font-weight: bold;
        margin-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA CON LOGO ---
# Intentamos cargar el logo. Si no existe, solo muestra el título.
try:
    st.image("logo.png", width=200) # Ajustá el ancho según tu logo
except:
    st.title("🎰 Bienvenido a nuestro Stand")

st.write("¡Participá por beneficios exclusivos usando nuestra ruleta!")

# --- LÓGICA DE JUEGO ---
premios = ["Regalo sorpresa", "Merch", "5% OFF", "10% OFF", "15% OFF"]
pesos = [5, 10, 25, 20, 10]
probabilidad_ganar = 0.3

if st.button("¡PROBAR SUERTE!", use_container_width=True):
    esta_ganando = random.random() < probabilidad_ganar

    if esta_ganando:
        resultado = random.choices(premios, weights=pesos, k=1)[0]
        r1, r2, r3 = resultado, resultado, resultado
    else:
        while True:
            r1, r2, r3 = random.choice(premios), random.choice(premios), random.choice(premios)
            if not (r1 == r2 == r3): break
        resultado = None

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
    if esta_ganando:
        st.balloons()
        st.markdown(f'<div class="win-banner">✨ ¡FELICITACIONES! ✨</div>', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>Ganaste: {resultado}</h3>", unsafe_allow_html=True)
    else:
        st.markdown('<p style="text-align: center; color: #666;">❌ No hubo coincidencia. ¡Seguí participando!</p>', unsafe_allow_html=True)
