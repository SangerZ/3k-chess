from board import Board
from gui import GameGUI as GUI
from ability import AbilityResult

class Game:
    def __init__(self, screen):
        print("[Game] Initializing game...")
        self.board = Board()
        self.screen = screen
        self.gui = GUI(self.screen, self.board)

    def start(self):
        print("[Game] Starting game loop...")
        while not self.board.game_over:
            self.gui.update()
            self.process_turn()

    def process_turn(self):
        current_turn = self.board.turn
        print(f"[Game] {current_turn}'s turn begins.")

        while True:
            action = self.gui.get_player_input(current_turn)
            print(f"[Game] Player action: {action}")

            if not action:
                break

            if action[0] == 'move':
                _, start, end = action
                print(f"[Game] Attempting move from {start} to {end}")
                piece = self.board.grid[start[0]][start[1]]
                if piece and piece.faction == current_turn:
                    if self.board.move(start, end):
                        print(f"[Game] Move successful: {piece.name} moved from {start} to {end}")
                        self.gui.update_board()
                        moved_piece = self.board.grid[end[0]][end[1]]
                        # Handle extra moves if granted
                        while getattr(moved_piece, "extra_moves", 0) > 0:
                            print(f"[Game] {moved_piece.name} has {moved_piece.extra_moves} extra move(s) left!")
                            moved_piece.extra_moves -= 1
                            extra_action = self.gui.get_player_input(current_turn)
                            print(f"[Game] Extra move action: {extra_action}")
                            if extra_action and extra_action[0] == 'move':
                                _, extra_start, extra_end = extra_action
                                if extra_start == (end if moved_piece.extra_moves == 1 else extra_start):
                                    if self.board.move(extra_start, extra_end):
                                        print(f"[Game] Extra move successful: {moved_piece.name} moved from {extra_start} to {extra_end}")
                                        self.gui.update_board()
                                        moved_piece = self.board.grid[extra_end[0]][extra_end[1]]
                                        end = extra_end
                                    else:
                                        break
                            else:
                                break
                        if self.board.game_over:
                            print("[Game] Game over detected after move.")
                            self.gui.display_winner(self.board.turn)
                            return
                        break  # End turn after move(s)

            elif action[0] == 'ability':
                            _, pos = action
                            piece = self.board.grid[pos[0]][pos[1]]
                            if piece and piece.ability and not piece.has_used_ability and piece.faction == current_turn:
                                print(f"[Game] {piece.name} ({piece.faction}) activated ability: {piece.ability.__name__} at {pos}")
                                result = piece.ability(self.board, pos)
                                piece.has_used_ability = True
                                self.gui.update_board()
                                if result == AbilityResult.END_TURN:
                                    break
                                elif result == AbilityResult.ALLOW_EXTRA_MOVES:
                                    while getattr(piece, "extra_moves", 0) > 0:
                                        print(f"[Game] {piece.name} has {piece.extra_moves} extra move(s) after ability!")
                                        piece.extra_moves -= 1
                                        extra_action = self.gui.get_player_input(current_turn)
                                        print(f"[Game] Extra move action: {extra_action}")
                                        if extra_action and extra_action[0] == 'move':
                                            _, extra_start, extra_end = extra_action
                                            if extra_start == pos or extra_start == extra_end:
                                                if self.board.move(extra_start, extra_end):
                                                    print(f"[Game] Extra move successful: {piece.name} moved from {extra_start} to {extra_end}")
                                                    self.gui.update_board()
                                                    piece = self.board.grid[extra_end[0]][extra_end[1]]
                                                    pos = extra_end
                                                else:
                                                    break
                                        else:
                                            break
                                    break
                                # Add more result types as needed

        print(f"[Game] {current_turn}'s turn ends. Swapping turn.")
        self.board.turn = 'Wei' if self.board.turn == 'Shu' else 'Shu'