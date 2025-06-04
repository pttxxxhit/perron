import streamlit as st
import requests
from datetime import datetime

# URL de la API de Aztro (Horóscopos)
HOROSCOPE_API_URL = "https://aztro.sameerkumar.website/"

# URL de la API de ZenQuotes (Frases motivadoras)
QUOTES_API_URL = "https://zenquotes.io/api/random"

# Traducción de los signos zodiacales al inglés
ZODIAC_TRANSLATIONS = {
    "Capricornio": "capricorn",
    "Acuario": "aquarius",
    "Piscis": "pisces",
    "Aries": "aries",
    "Tauro": "taurus",
    "Géminis": "gemini",
    "Cáncer": "cancer",
    "Leo": "leo",
    "Virgo": "virgo",
    "Libra": "libra",
    "Escorpio": "scorpio",
    "Sagitario": "sagittarius"
    }

# Datos de las fechas asociadas con cada signo zodiacal
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

# Horóscopos falsos como respaldo
FAKE_HOROSCOPES = {
    "aries": "Hoy es un buen día para tomar nuevas decisiones. Confía en tu instinto.",
    "taurus": "El trabajo duro siempre da recompensas. Sigue perseverando.",
    "gemini": "Hoy es un día perfecto para ahondar en el entendimiento con tus seres queridos.",
    "cancer": "La tranquilidad será tu mejor aliada para enfrentar los retos del día.",
    "leo": "Las estrellas te favorecen. Es el momento de tomar riesgos calculados.",
    "virgo": "La organización será clave para aprovechar las oportunidades del día.",
    "libra": "El equilibrio en tus decisiones marcará una pauta positiva en tu destino.",
    "scorpio": "Hoy sentirás una fuerza interna que te impulsará a lograr grandes cosas.",
    "sagittarius": "La curiosidad será tu mejor guía. Explora nuevas ideas y oportunidades.",
    "capricorn": "Tu perseverancia te llevará lejos. No te rindas ante dificultades menores.",
    "aquarius": "Piensa fuera de la caja y hallarás la solución que buscas.",
    "pisces": "El arte y la creatividad te darán claridad. Déjate llevar por tus emociones."
    }


# Función para determinar el signo zodiacal según la fecha
def get_zodiac_sign(day, month):
    for sign, start_date, end_date in ZODIAC_SIGNS:
        start_month, start_day = start_date
        end_month, end_day = end_date
        if ((month == start_month and day >= start_day) or
                (month == end_month and day <= end_day)):
            return sign
    return None


# Función para traducir un signo zodiacal del español al inglés
def get_zodiac_in_english(sign):
    return ZODIAC_TRANSLATIONS.get(sign, "").lower()


# Función para obtener el horóscopo desde la API de Aztro o usar el respaldo
def get_horoscope(sign):
    """
    Obtiene el horóscopo diario desde la API de Aztro o muestra un respaldo local.
    :param sign: El signo zodiacal en inglés
    :return: Descripción del horóscopo
    """
    try:
        # Realizar solicitud POST a la API
        response = requests.post(HOROSCOPE_API_URL, params={'sign': sign, 'day': 'today'}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("description", "No se pudo obtener el horóscopo.")
        elif response.status_code == 503:
            # Si la API no está disponible, usar un respaldo local
            return FAKE_HOROSCOPES.get(sign, "No tenemos un horóscopo para este signo en este momento.")
        else:
            return f"⚠️ Error inesperado en la API de Horóscopo: Código {response.status_code}"
    except requests.exceptions.Timeout:
        return FAKE_HOROSCOPES.get(sign, "No tenemos un horóscopo para este signo en este momento.")
    except Exception as e:
        return f"⚠️ Error inesperado: {e}"


# Función para obtener una frase motivadora desde ZenQuotes
def get_motivational_quote():
    """
    Obtiene una frase motivadora desde la API de ZenQuotes.
    :return: Texto de la frase motivadora o error
    """
    try:
        response = requests.get(QUOTES_API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data[0]['q']  # Texto de la frase
        else:
            return f"⚠️ Error en la API de Frases: Código {response.status_code}"
    except requests.exceptions.Timeout:
        return "⏳ La solicitud de la frase motivadora tardó demasiado. Por favor, intenta más tarde."
    except Exception as e:
        return f"⚠️ Error inesperado: {e}"


# Función para manejar la entrada de la fecha de nacimiento
def handle_birthday_input():
    try:
        # Obtener fecha introducida
        birthday = st.session_state.birthday
        birth_date = datetime.strptime(birthday, "%Y-%m-%d")  # Validar formato YYYY-MM-DD

        # Obtener el signo zodiacal en español e inglés
        sign = get_zodiac_sign(birth_date.day, birth_date.month)
        sign_in_english = get_zodiac_in_english(sign)

        # Obtener el horóscopo y la frase motivadora
        horoscope = get_horoscope(sign_in_english)
        quote = get_motivational_quote()

        # Guardar los resultados y pasar a la página de resultados
        st.session_state.page = "results"
        st.session_state.sign = sign
        st.session_state.horoscope = horoscope
        st.session_state.quote = quote

    except ValueError:
        st.error("⚠️ Fecha no válida. Por favor utiliza el formato YYYY-MM-DD.")
    except Exception as e:
        st.error(f"⚠️ Un error inesperado ocurrió: {e}")


# Función para mostrar la página principal
def main_page():
    st.title("🔮Fasbiola hoy es tu dia de suerte 🌟")
    st.write("¡Descubre lo que las estrellas tienen preparado para ti hoy!")
    if st.button("Ver mi Horóscopo del Día"):
        st.session_state.page = "birthday_input"


# Función para mostrar la página de entrada de fecha de nacimiento
def birthday_input_page():
    st.title("📅 Ingresa tu fecha de nacimiento")
    st.write("Por favor escribe tu fecha de nacimiento en el formato **YYYY-MM-DD** (ejemplo: 2000-05-23).")
    st.text_input("Fecha de nacimiento:", key="birthday", placeholder="YYYY-MM-DD")
    if st.button("Obtener mi Horóscopo"):
        handle_birthday_input()


# Función para mostrar la página de resultados con el horóscopo y frase
def results_page():
    st.title(f"⭐ Tu Horóscopo del Día ⭐")
    st.subheader(f"Tu signo zodiacal es: **{st.session_state.sign}**")
    st.write(f"✨ **Horóscopo:** {st.session_state.horoscope}")
    st.write(f"🌟 **Frase motivadora:** {st.session_state.quote}")
    if st.button("Volver al inicio"):
        st.session_state.page = "main"


# Navegación entre páginas
if 'page' not in st.session_state:
    st.session_state.page = "main"

# Renderizar páginas según la navegación
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "birthday_input":
    birthday_input_page()
elif st.session_state.page == "results":
    results_page()
