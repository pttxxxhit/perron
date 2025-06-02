import random
import streamlit as st


# Inicialización del estado de la aplicación
if 'snake' not in st.session_state:
    st.session_state.snake = [[5, 5]]  # Posición inicial de la serpiente
if 'food' not in st.session_state:
    st.session_state.food = [random.randint(0, 9), random.randint(0, 9)]  # Comida inicial
if 'direction' not in st.session_state:
    st.session_state.direction = 'RIGHT'  # Dirección inicial
if 'score' not in st.session_state:
    st.session_state.score = 0  # Puntaje
if 'screen' not in st.session_state:
    st.session_state.screen = 'main'  # Pantalla inicial: 'main' o 'game'

GRID_SIZE = 10


def move_snake():
    """Mueve la serpiente en la dirección actual."""
    head = st.session_state.snake[0]  # Cabeza de la serpiente
    new_head = head.copy()

    if st.session_state.direction == 'UP':
        new_head[1] -= 1
    elif st.session_state.direction == 'DOWN':
        new_head[1] += 1
    elif st.session_state.direction == 'LEFT':
        new_head[0] -= 1
    elif st.session_state.direction == 'RIGHT':
        new_head[0] += 1

    # Asegurar que la serpiente no salga de los límites
    if (
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= GRID_SIZE or new_head[1] >= GRID_SIZE
    ):
        st.session_state.snake = [[5, 5]]  # Reiniciar
        st.session_state.score = 0
        st.warning("Chocaste contra un muro. Juego reiniciado.")
        return False

    # Verificar si la serpiente se muerde a sí misma
    if new_head in st.session_state.snake:
        st.session_state.snake = [[5, 5]]  # Reiniciar
        st.session_state.score = 0
        st.warning("Te mordiste. Juego reiniciado.")
        return False

    # Mover la serpiente
    st.session_state.snake = [new_head] + st.session_state.snake[:-1]

    # Verificar si la serpiente come comida
    if new_head == st.session_state.food:
        st.session_state.snake.append(st.session_state.snake[-1])  # Crece
        st.session_state.food = [
            random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1)
            ]  # Nueva posición de comida
        st.session_state.score += 1

    return True


def draw_grid():
    """Dibuja el tablero del juego."""
    grid = [["⬜"] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Dibuja la serpiente
    for segment in st.session_state.snake:
        grid[segment[1]][segment[0]] = "🟩"

    # Dibuja la comida
    food = st.session_state.food
    grid[food[1]][food[0]] = "🍎"

    # Renderizar la cuadrícula
    st.write("")
    for row in grid:
        st.write("".join(row))


def snake_game():
    """Pantalla del juego Snake."""
    st.title("🐍 Snake Game")
    st.sidebar.title("Controles")

    st.sidebar.write("Usa los botones para mover la serpiente:")
    if st.sidebar.button("⬆️ Up"):
        st.session_state.direction = "UP"
    if st.sidebar.button("⬅️ Left"):
        st.session_state.direction = "LEFT"
    if st.sidebar.button("⬇️ Down"):
        st.session_state.direction = "DOWN"
    if st.sidebar.button("➡️ Right"):
        st.session_state.direction = "RIGHT"

    st.write(f"**Puntaje:** {st.session_state.score}")

    # Avance del juego
    success = move_snake()

    if success:
        draw_grid()
    else:
        st.error("El juego terminó. Presiona cualquier botón para reiniciar.")

    # Botón para volver al menú principal
    if st.button("Volver al menú principal"):
        st.session_state.screen = 'main'


def main():
    """Pantalla principal de la aplicación."""
    st.title("Lxcas de la PAC")
    st.warning("despabila o juega.")

    # Botón para ir al juego
    if st.button("Play Snake Game"):
        st.session_state.screen = 'game'  # Cambiar a la pantalla del juego


# Controlador de pantalla
if __name__ == "__main__":
    # Cambiar entre pantalla principal y juego
    if st.session_state.screen == 'main':
        main()
    elif st.session_state.screen == 'game':
        snake_game()
