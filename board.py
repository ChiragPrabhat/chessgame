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

        # Initialize the PieceManager
        self.piece_manager = PieceManager(self.cell_size)

        # Initialize starting positions for pieces
        self.setup_pieces()

    def setup_pieces(self):
        """Set up initial piece positions on the board."""
        for i in range(8):
            self.board[1][i] = ('pawn', 'black')  # Black pawns
            self.board[6][i] = ('pawn', 'white')  # White pawns

        # Setup other pieces
        self.board[0][0] = self.board[0][7] = ('rook', 'black')
        self.board[0][1] = self.board[0][6] = ('knight', 'black')
        self.board[0][2] = self.board[0][5] = ('bishop', 'black')
        self.board[0][3] = ('queen', 'black')
        self.board[0][4] = ('king', 'black')

        # Add white pieces setup similarly
        self.board[7][0] = self.board[7][7] = ('rook', 'white')
        self.board[7][1] = self.board[7][6] = ('knight', 'white')
        self.board[7][2] = self.board[7][5] = ('bishop', 'white')
        self.board[7][3] = ('queen', 'white')
        self.board[7][4] = ('king', 'white')

    def draw_board(self):
        """Draw the chessboard and the pieces."""
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.screen, color, 
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

                # Draw pieces on the board
                piece = self.board[row][col]
                if piece:
                    piece_type, piece_color = piece
                    self.piece_manager.draw_piece(self.screen, piece_type, piece_color, col, row)

    def run(self):
        """Main game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill the screen with white color
            self.screen.fill(self.WHITE)

            # Draw the chess board
            self.draw_board()

            # Update the display
            pygame.display.update()

# Create a ChessBoard instance and run the game
if __name__ == "__main__":
    chess_board = ChessBoard(640, 640)
    chess_board.run()
