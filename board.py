import pygame
from pygame.locals import *
import sys
from pieces import PieceManager


pygame.init()

class ChessBoard:
    def __init__(self, width, height):
        # Set up the display
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.cell_size = width // 8  # Assuming an 8x8 grid

        # Define colors
        self.WHITE = (115, 149, 82)
        self.BLACK = (235, 236, 208)

        # Track the board state: 2D array for piece positions (None for empty squares)
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'  # Start with white's turn


        # Initialize the PieceManager
        self.piece_manager = PieceManager(self.cell_size)

        # Initialize starting positions for pieces
        self.setup_pieces()

        # Track selected piece and position
        self.selected_piece = None
        self.selected_position = None

    def setup_pieces(self):
        """Set up initial piece positions on the board."""
        for i in range(8):
            self.board[1][i] = ('pawn', 'black')  # Black pawns
            self.board[6][i] = ('pawn', 'white')  # White pawns

        # Setup other pieces for black
        self.board[0][0] = self.board[0][7] = ('rook', 'black')
        self.board[0][1] = self.board[0][6] = ('knight', 'black')
        self.board[0][2] = self.board[0][5] = ('bishop', 'black')
        self.board[0][3] = ('queen', 'black')
        self.board[0][4] = ('king', 'black')

        # Setup other pieces for white
        self.board[7][0] = self.board[7][7] = ('rook', 'white')
        self.board[7][1] = self.board[7][6] = ('knight', 'white')
        self.board[7][2] = self.board[7][5] = ('bishop', 'white')
        self.board[7][3] = ('queen', 'white')
        self.board[7][4] = ('king', 'white')


    def highlight_moves(self, piece, row, col):
        """Calculate valid moves for the selected piece."""
        piece_type, piece_color = piece
        moves = []

        # Pawn movement logic
        if piece_type == 'pawn':
            direction = -1 if piece_color == 'white' else 1  # White moves up, black moves down
            start_row = 6 if piece_color == 'white' else 1
            new_row = row + direction

            # Move forward one square
            if 0 <= new_row < 8 and self.board[new_row][col] is None:
                moves.append((new_row, col))

            # Move forward two squares from starting position
            if row == start_row and self.board[new_row][col] is None:
                new_row_two = row + 2 * direction
                if 0 <= new_row_two < 8 and self.board[new_row_two][col] is None:
                    moves.append((new_row_two, col))

            # Capture diagonally
            for dx in [-1, 1]:
                if 0 <= new_row < 8 and 0 <= col + dx < 8:
                    target = self.board[new_row][col + dx]
                    if target and target[1] != piece_color:
                        moves.append((new_row, col + dx))

        # Knight movement logic
        elif piece_type == 'knight':
            knight_moves = [
                (2, 1), (2, -1), (-2, 1), (-2, -1),  # Two squares horizontally
                (1, 2), (1, -2), (-1, 2), (-1, -2)   # Two squares vertically
            ]
            for dx, dy in knight_moves:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board[new_row][new_col] is None or self.board[new_row][new_col][1] != piece_color:
                        moves.append((new_row, new_col))


        # Rook movement logic
        elif piece_type == 'rook':
            for d in [-1, 1]:  # Check both directions
                for step in range(1, 8):  # Move up to 7 squares
                    new_row = row + d * step
                    if 0 <= new_row < 8:
                        if self.board[new_row][col] is None:
                            moves.append((new_row, col))  # Empty square
                        else:
                            if self.board[new_row][col][1] != piece_color:
                                moves.append((new_row, col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

            for d in [-1, 1]:  # Check left and right
                for step in range(1, 8):  # Move up to 7 squares
                    new_col = col + d * step
                    if 0 <= new_col < 8:
                        if self.board[row][new_col] is None:
                            moves.append((row, new_col))  # Empty square
                        else:
                            if self.board[row][new_col][1] != piece_color:
                                moves.append((row, new_col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

        # Bishop movement logic
        elif piece_type == 'bishop':
            for d in [-1, 1]:  # Check diagonals
                for step in range(1, 8):
                    new_row = row + d * step
                    new_col = col + d * step
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] is None:
                            moves.append((new_row, new_col))  # Empty square
                        else:
                            if self.board[new_row][new_col][1] != piece_color:
                                moves.append((new_row, new_col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

            for d in [-1, 1]:  # Check the other diagonal
                for step in range(1, 8):
                    new_row = row + d * step
                    new_col = col - d * step
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] is None:
                            moves.append((new_row, new_col))  # Empty square
                        else:
                            if self.board[new_row][new_col][1] != piece_color:
                                moves.append((new_row, new_col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

        # Queen movement logic (combines rook and bishop)
        elif piece_type == 'queen':
            # Use rook logic
            for d in [-1, 1]:  # Check vertical
                for step in range(1, 8):
                    new_row = row + d * step
                    if 0 <= new_row < 8:
                        if self.board[new_row][col] is None:
                            moves.append((new_row, col))  # Empty square
                        else:
                            if self.board[new_row][col][1] != piece_color:
                                moves.append((new_row, col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

            for d in [-1, 1]:  # Check horizontal
                for step in range(1, 8):
                    new_col = col + d * step
                    if 0 <= new_col < 8:
                        if self.board[row][new_col] is None:
                            moves.append((row, new_col))  # Empty square
                        else:
                            if self.board[row][new_col][1] != piece_color:
                                moves.append((row, new_col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

            # Use bishop logic
            for d in [-1, 1]:  # Check diagonal
                for step in range(1, 8):
                    new_row = row + d * step
                    new_col = col + d * step
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] is None:
                            moves.append((new_row, new_col))  # Empty square
                        else:
                            if self.board[new_row][new_col][1] != piece_color:
                                moves.append((new_row, new_col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

            for d in [-1, 1]:  # Check the other diagonal
                for step in range(1, 8):
                    new_row = row + d * step
                    new_col = col - d * step
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] is None:
                            moves.append((new_row, new_col))  # Empty square
                        else:
                            if self.board[new_row][new_col][1] != piece_color:
                                moves.append((new_row, new_col))  # Capture
                            break  # Blocked by another piece
                    else:
                        break  # Out of bounds

        # King movement logic
        elif piece_type == 'king':
            king_moves = [
                (1, 0), (-1, 0), (0, 1), (0, -1),
                (1, 1), (1, -1), (-1, 1), (-1, -1)
            ]
            for dx, dy in king_moves:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board[new_row][new_col] is None or self.board[new_row][new_col][1] != piece_color:
                        moves.append((new_row, new_col))

        return moves


    def draw_board(self):
        """Draw the chessboard and the pieces."""
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.screen, color, 
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

                # Highlight the square if it's a valid move
                if self.selected_position and (row, col) in self.highlight_moves(self.selected_piece, *self.selected_position):
                    pygame.draw.rect(self.screen, (0, 255, 0, 128),
                                     (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

                # Draw pieces on the board
                piece = self.board[row][col]
                if piece:
                    piece_type, piece_color = piece
                    self.piece_manager.draw_piece(self.screen, piece_type, piece_color, col, row)

    def run(self):
        """Main game loop."""
        selected_piece = None
        selected_row = None
        selected_col = None
        current_turn = 'white'  # White starts first

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // self.cell_size
                    row = mouse_y // self.cell_size

                    piece = self.board[row][col]

                    # If a piece is already selected
                    if selected_piece is not None:
                        if (row, col) in self.highlight_moves(selected_piece, selected_row, selected_col):  # Move piece
                            # Move the piece
                            self.board[row][col] = selected_piece  # Place the piece in the new position
                            self.board[selected_row][selected_col] = None  # Remove it from the old position
                            selected_piece = None  # Deselect piece

                            # Switch turn
                            current_turn = 'black' if current_turn == 'white' else 'white'
                        else:
                            # Deselect the piece if the click is not a valid move
                            selected_piece = None  # Deselecting if it's not a valid move

                    # If no piece is selected, try to select a piece
                    else:
                        if piece and piece[1] == current_turn:  # Check if it's the current player's piece
                            selected_piece = piece
                            selected_row, selected_col = row, col

            # Fill the screen with white color
            self.screen.fill(self.WHITE)

            # Draw the chess board
            self.draw_board()

            # Highlight valid moves if a piece is selected
            if selected_piece:
                moves = self.highlight_moves(selected_piece, selected_row, selected_col)
                for move in moves:
                    pygame.draw.rect(self.screen, (0, 255, 0), (move[1] * self.cell_size, move[0] * self.cell_size, self.cell_size, self.cell_size), 3)

            # Update the display
            pygame.display.update()



# Create a ChessBoard instance and run the game
if __name__ == "__main__":
    chess_board = ChessBoard(640, 640)
    chess_board.run()
