import streamlit as st
import numpy as np


# Función para inicializar el estado del juego
def initialize_game_state():
    st.session_state['board_size'] = 10  # Tamaño del tablero
    st.session_state['snake'] = [[5, 5]]  # Posición inicial de la serpiente
    st.session_state['direction'] = 'RIGHT'  # Dirección inicial
    st.session_state['score'] = 0  # Puntaje inicial
    st.session_state['food'] = [
        np.random.randint(0, st.session_state['board_size']),
        np.random.randint(0, st.session_state['board_size']),
        ]  # Generar comida inicial
    st.session_state['game_over'] = False  # Estado inicial del juego


# Renderizar el tablero del juego
def render_board():
    board = np.zeros((st.session_state['board_size'], st.session_state['board_size']), dtype=int)
    for segment in st.session_state['snake']:
        board[segment[0]][segment[1]] = 1  # Segmentos de la serpiente
    board[st.session_state['food'][0]][st.session_state['food'][1]] = 2  # Comida

    st.write("Score:", st.session_state['score'])
    st.table(board)


# Actualizar el estado del juego
def update_game_state():
    if st.session_state['game_over']:
        st.error("Game over! Your final score is {}".format(st.session_state['score']))
        return

    # Actualizar la posición de la cabeza de la serpiente
    head = st.session_state['snake'][-1][:]
    if st.session_state['direction'] == 'UP':
        head[0] = (head[0] - 1) % st.session_state['board_size']
    elif st.session_state['direction'] == 'DOWN':
        head[0] = (head[0] + 1) % st.session_state['board_size']
    elif st.session_state['direction'] == 'LEFT':
        head[1] = (head[1] - 1) % st.session_state['board_size']
    elif st.session_state['direction'] == 'RIGHT':
        head[1] = (head[1] + 1) % st.session_state['board_size']

    # Agregar nueva posición de la cabeza
    st.session_state['snake'].append(head)

    # Comprobar colisión con la comida
    if head == st.session_state['food']:
        st.session_state['score'] += 1
        st.session_state['food'] = [
            np.random.randint(0, st.session_state['board_size']),
            np.random.randint(0, st.session_state['board_size']),
            ]  # Nueva comida
    else:
        # Si no se come comida, eliminar el último segmento
        st.session_state['snake'].pop(0)

    # Comprobar colisión de la serpiente consigo misma
    if head in st.session_state['snake'][:-1]:
        st.session_state['game_over'] = True


# Función principal del juego Snake
def snake_game():
    st.title("Snake Game")

    # Inicializar el estado del juego si no está ya inicializado
    if 'snake' not in st.session_state:
        initialize_game_state()

    # Mostrar tablero
    render_board()

    # Botones para controlar la dirección
    with st.columns(3) as cols:
        if cols[0].button("⬅️ Left"):
            st.session_state['direction'] = 'LEFT'
        if cols[1].button("⬇️ Down"):
            st.session_state['direction'] = 'DOWN'
        if cols[2].button("➡️ Right"):
            st.session_state['direction'] = 'RIGHT'

    if st.button("⬆️ Up"):
        st.session_state['direction'] = 'UP'

    # Actualizar el estado del juego
    update_game_state()

    # Botón para reiniciar el juego
    if st.session_state['game_over']:
        if st.button("Play Again"):
            initialize_game_state()


# Pantalla principal de la aplicación
def main():
    st.title("Lxcas de la PAC")
    st.warning("Anda a acostarte... o juega Snake.")

    if st.button("Play Snake Game"):
        snake_game()


# Ejecutar la aplicación
if __name__ == "__main__":
    main()