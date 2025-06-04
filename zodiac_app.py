import streamlit as st
import requests
from datetime import datetime

# URL de la API de horóscopos
HOROSCOPE_API_URL = "https://aztro.sameerkumar.website/?sign={}&day=today"

# URL de la API de frases motivadoras
QUOTES_API_URL = "https://zenquotes.io/api/random"

# Datos de los signos del zodiaco
ZODIAC_SIGNS = [
    ("Capricornio", (1, 1), (1, 19)),
    ("Acuario", (1, 20), (2, 18)),
    ("Piscis", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Tauro", (4, 20), (5, 20)),
    ("Géminis", (5, 21), (6, 20)),
    ("Cáncer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Escorpio", (10, 23), (11, 21)),
    ("Sagitario", (11, 22), (12, 21)),
    ("Capricornio", (12, 22), (12, 31))
    ]


# Función para determinar el signo zodiacal según la fecha
def get_zodiac_sign(day, month):
    for sign, start_date, end_date in ZODIAC_SIGNS:
        start_month, start_day = start_date
        end_month, end_day = end_date
        if ((month == start_month and day >= start_day) or
                (month == end_month and day <= end_day)):
            return sign
    return None


# Función para obtener el horóscopo desde la API
def get_horoscope(sign):
    try:
        response = requests.post(HOROSCOPE_API_URL.format(sign.lower()))
        if response.status_code == 200:
            data = response.json()
            return data.get("description", "No se pudo obtener el horóscopo.")
        else:
            return "⚠️ No pudimos obtener el horóscopo. Intenta más tarde."
    except Exception as e:
        return f"⚠️ Error al conectarse a la API del horóscopo: {e}"


# Función para obtener una frase motivadora desde la API
def get_motivational_quote():
    try:
        response = requests.get(QUOTES_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data[0]['q']  # Texto de la frase
        else:
            return "⚠️ No pudimos obtener una frase motivadora. ¡Intenta más tarde!"
    except Exception as e:
        return f"⚠️ Error al conectarse a la API de frases: {e}"


# Función para mostrar el horóscopo y frase motivadora
def show_horoscope_page(sign, horoscope, quote):
    st.title(f"⭐ Tu Horóscopo del Día ⭐")
    st.subheader(f"Tu signo zodiacal es: **{sign}**")
    st.write(f"✨ **Horóscopo:** {horoscope}")
    st.write(f"🌟 **Frase motivadora:** {quote}")
    st.button("Volver al inicio", on_click=go_back_to_main)


# Volver al menú principal
def go_back_to_main():
    st.session_state.page = "main"


# Verificar la fecha de nacimiento y calcular signo zodiacal
def handle_birthday_input():
    try:
        # Obtener la fecha ingresada por el usuario
        birthday = st.session_state.birthday
        birth_date = datetime.strptime(birthday, "%Y-%m-%d")  # Convertir a objeto datetime
        sign = get_zodiac_sign(birth_date.day, birth_date.month)

        # Obtener datos dinámicos desde las APIs
        horoscope = get_horoscope(sign)
        quote = get_motivational_quote()

        # Cambiar página a resultados
        st.session_state.page = "results"
        st.session_state.sign = sign
        st.session_state.horoscope = horoscope
        st.session_state.quote = quote

    except ValueError:
        st.error("⚠️ Por favor, ingresa una fecha válida en formato YYYY-MM-DD.")


# Inicio de la app
def main_page():
    st.title("🔮Hola Fabiola es tu dia de suerte🌟")
    st.write("¡Descubre lo que las estrellas tienen preparado para ti hoy!")
    if st.button("no salgas de casa sin ver esto"):
        st.session_state.page = "birthday_input"


# Pantalla para ingresar la fecha de nacimiento
def birthday_input_page():
    st.title("📅 Ingresa tu fecha de nacimiento")
    st.write("Por favor escribe tu fecha de nacimiento en el formato **YYYY-MM-DD** (ejemplo: 2000-05-23).")
    st.text_input("Fecha de nacimiento:", key="birthday", placeholder="YYYY-MM-DD")
    if st.button("Obtener mi Horóscopo"):
        handle_birthday_input()


# Pantalla de resultado del horóscopo
def results_page():
    show_horoscope_page(
        st.session_state.sign,
        st.session_state.horoscope,
        st.session_state.quote
        )


# Configuración de la página inicial
if 'page' not in st.session_state:
    st.session_state.page = "main"

# Navegador de páginas
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "birthday_input":
    birthday_input_page()
elif st.session_state.page == "results":
    results_page()
