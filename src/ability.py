
from enum import Enum, auto

class AbilityResult(Enum):
    END_TURN = auto()
    ALLOW_EXTRA_MOVES = auto()
    CONTINUE = auto()

def rally_ability(board, pos):
    print(f"[Ability] Rally activated at {pos}")
    row, col = pos
    faction = board.grid[row][col].faction
    for c in range(8):
        piece = board.grid[row][c]
        if piece and piece.faction == faction:
            piece.extra_moves = 1
            print(f"[Ability] {piece.name} at ({row},{c}) gets extra move.")
    return AbilityResult.END_TURN

def swap_ability(board, pos):
    print(f"[Ability] Swap activated at {pos}")
    row, col = pos
    faction = board.grid[row][col].faction
    for r in range(8):
        if r != row:
            piece = board.grid[r][col]
            if piece and piece.faction == faction:
                board.grid[row][col], board.grid[r][col] = board.grid[r][col], board.grid[row][col]
                print(f"[Ability] Swapped with {piece.name} at ({r},{col})")
                break
    return AbilityResult.END_TURN

def charge_ability(board, pos):
    print(f"[Ability] Charge activated at {pos}")
    row, col = pos
    piece = board.grid[row][col]
    piece.extra_moves = 2
    print(f"[Ability] {piece.name} at ({row},{col}) can move twice this turn.")
    return AbilityResult.ALLOW_EXTRA_MOVES