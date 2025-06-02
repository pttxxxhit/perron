import streamlit as st
import numpy as np

# Inicialización del estado del juego
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((6, 7), dtype=int)  # Tablero de 6 filas x 7 columnas
if 'current_player' not in st.session_state:
    st.session_state.current_player = 1  # El primer jugador comienza
if 'winner' not in st.session_state:
    st.session_state.winner = None  # No hay ganador al inicio


def reset_game():
    """Reinicia el tablero y el estado del juego."""
    st.session_state.board = np.zeros((6, 7), dtype=int)
    st.session_state.current_player = 1
    st.session_state.winner = None


def drop_piece(column):
    """Coloca una ficha en la columna seleccionada."""
    if st.session_state.winner is not None:
        return  # No permitir jugar después de ganar

    board = st.session_state.board
    for row in range(5, -1, -1):  # Comenzar desde abajo hacia arriba
        if board[row, column] == 0:  # Encontrar la primera fila vacía
            board[row, column] = st.session_state.current_player
            if check_winner(row, column):  # Comprobar si este movimiento ganó el juego
                st.session_state.winner = st.session_state.current_player
            else:
                # Cambiar turno
                st.session_state.current_player = 3 - st.session_state.current_player  # Alternar entre 1 y 2
            break


def check_winner(row, col):
    """Verifica si hay un ganador después de colocar una ficha."""
    board = st.session_state.board
    player = st.session_state.current_player

    # Verificar direcciones: horizontal, vertical, diagonales
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1  # Contar la ficha actual
        # Verificar hacia adelante
        r, c = row + dr, col + dc
        while 0 <= r < 6 and 0 <= c < 7 and board[r, c] == player:
            count += 1
            r += dr
            c += dc
        # Verificar hacia atrás
        r, c = row - dr, col - dc
        while 0 <= r < 6 and 0 <= c < 7 and board[r, c] == player:
            count += 1
            r -= dr
            c -= dc
        # Comprobar si se encontraron 4 en línea
        if count >= 4:
            return True
    return False


def draw_board():
    """Dibujar el tablero del juego en Streamlit."""
    board = st.session_state.board
    board_text = ""

    # Representar el tablero como texto
    for row in board:
        for cell in row:
            if cell == 0:
                board_text += "⚪"  # Casilla vacía
            elif cell == 1:
                board_text += "🔴"  # Jugador 1
            elif cell == 2:
                board_text += "🟡"  # Jugador 2
        board_text += "\n"
    st.text(board_text)


def connect_four_screen():
    """Pantalla del juego Connect Four."""
    st.title("🔴🟡 Conecta 4")

    # Mostrar el turno actual o el ganador
    if st.session_state.winner is not None:
        st.success(f"🎉 ¡El jugador {st.session_state.winner} ha ganado!")
    else:
        st.write(f"Turno actual: {'🔴' if st.session_state.current_player == 1 else '🟡'}")

    # Dibujar el tablero
    draw_board()

    # Botones para seleccionar la columna
    columns = st.columns(7)
    for col in range(7):
        with columns[col]:
            if st.button(f"Columna {col + 1}", key=f"col{col}"):
                drop_piece(col)

    # Botón para reiniciar el juego
    if st.button("Reiniciar juego"):
        reset_game()

    # Botón para volver al menú principal
    if st.button("Volver al menú principal"):
        st.session_state.screen = 'main'


def main_screen():
    """Pantalla principal donde se selecciona el juego."""
    st.title("🎮 Centro de Juegos - Lxcas de la PAC")
    st.warning("Elige un juego para jugar.")

    # Botones para seleccionar game
    if st.button("Conecta 4"):
        st.session_state.screen = 'connect_four'
    elif st.button("Tic Tac Toe"):
        st.session_state.screen = 'tic_tac_toe'


# Controlador de pantallas
if __name__ == "__main__":
    if 'screen' not in st.session_state:
        st.session_state.screen = 'main'  # Pantalla inicial ('main', 'connect_four' o 'tic_tac_toe')

    if st.session_state.screen == 'main':
        main_screen()
    elif st.session_state.screen == 'connect_four':
        connect_four_screen()
    elif st.session_state.screen == 'tic_tac_toe':
        st.write("⚠️ Tic Tac Toe no está implementado. Por favor, juega Conecta 4.")  # Placeholder
