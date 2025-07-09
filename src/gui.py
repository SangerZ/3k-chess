import pygame
import sys

class GameGUI:
    def __init__(self, screen, board):
        print("[GUI] Initializing GUI...")
        self.screen = screen
        self.board = board
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def draw_board(self):
        # Draw the chessboard squares
        self.screen.fill((255, 255, 255))
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * 100, row * 100, 100, 100)
                color = (200, 200, 200) if (row + col) % 2 == 0 else (100, 100, 100)
                pygame.draw.rect(self.screen, color, rect)
                piece = self.board.grid[row][col]
                if piece:
                    # Draw the piece symbol
                    text = self.font.render(str(piece.symbol), True, (0, 0, 0))
                    self.screen.blit(text, (col * 100 + 30, row * 100 + 30))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[GUI] Quit event detected.")
                pygame.quit()
                sys.exit()
        self.draw_board()
        pygame.display.flip()

    def get_player_input(self, current_turn):
        selected = None
        print(f"[GUI] Awaiting input for {current_turn}...")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("[GUI] Quit event detected.")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // 100, x // 100
                    print(f"[GUI] Mouse click at ({row}, {col}), button {event.button}")
                    if event.button == 1:  # Left click for move
                        if selected is None:
                            if self.board.grid[row][col] and self.board.grid[row][col].faction == current_turn:
                                selected = (row, col)
                                print(f"[GUI] Selected piece at {selected}")
                        else:
                            print(f"[GUI] Move from {selected} to {(row, col)}")
                            return ('move', selected, (row, col))
                    elif event.button == 3:  # Right click for ability
                        if self.board.grid[row][col] and self.board.grid[row][col].faction == current_turn:
                            print(f"[GUI] Ability activation at ({row}, {col})")
                            return ('ability', (row, col))
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

    def update_board(self):
        print("[GUI] Board updated.")
        self.draw_board()
        pygame.display.flip()

    def display_winner(self, winner):
        print(f"[GUI] {winner} wins!")