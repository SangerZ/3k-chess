from ability import AbilityResult

class Board:
    def __init__(self):
        print("[Board] Initializing board...")
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'Shu'
        self.game_over = False
        self.populate_board()

    def populate_board(self):
        print("[Board] Populating board with pieces...")
        from piece import Piece
        self.grid[7][4] = Piece('Liu Bei', 'Shu', 'LB', self.king_moves, self.rally_ability, 'king')
        self.grid[7][3] = Piece('Zhuge Liang', 'Shu', 'ZL', self.queen_moves, self.swap_ability, 'queen')
        self.grid[7][1] = Piece('Zhao Yun', 'Shu', 'ZY', self.knight_moves, self.charge_ability, 'knight')
        self.grid[0][4] = Piece('Cao Cao', 'Wei', 'CC', self.king_moves, self.rally_ability, 'king')
        self.grid[0][3] = Piece('Sima Yi', 'Wei', 'SY', self.queen_moves, self.swap_ability, 'queen')
        self.grid[0][1] = Piece('Zhang Liao', 'Wei', 'ZL', self.knight_moves, self.charge_ability, 'knight')

        # Pawns for Shu (row 6)
        for col in range(8):
            self.grid[6][col] = Piece(f'Shu Pawn {col+1}', 'Shu', 'sp', self.pawn_moves, None, 'pawn')

        # Pawns for Wei (row 1)
        for col in range(8):
            self.grid[1][col] = Piece(f'Wei Pawn {col+1}', 'Wei', 'wp', self.pawn_moves, None, 'pawn')

    def display(self):
        for row in self.grid:
            print(' '.join(p.symbol if p else '.' for p in row))
        print()

    def move(self, start, end):
        print(f"[Board] move() called: {start} -> {end}")
        sx, sy = start
        ex, ey = end
        piece = self.grid[sx][sy]

        if not piece:
            print("[Board] No piece at start.")
            return False

        if piece.faction != self.turn:
            print("[Board] Not your turn.")
            return False

        valid_moves = piece.movement_fn(start, self.grid)

        if end not in valid_moves:
            print("[Board] Invalid move.")
            return False

        target = self.grid[ex][ey]
        if target and target.faction == piece.faction:
            print("[Board] Can't capture your own piece.")
            return False
        # Print capture message
        if target:
            print(f"[Board] {piece.name} captured {target.name} at {end}!")

        # Use piece_type for king capture check
        if target and getattr(target, "piece_type", None) == "king":
            print(f"[Board] Game Over! {target.name} (King) has been captured!")
            self.game_over = True

        self.grid[ex][ey] = piece
        self.grid[sx][sy] = None
        piece.has_moved = True  # <-- Mark as moved
        print(f"[Board] {piece.name} moved to {end}")
        return True

    def pawn_moves(self, pos, grid):
        x, y = pos
        moves = []
        piece = grid[x][y]
        if not piece:
            return moves
        direction = -1 if piece.faction == 'Shu' else 1  # Shu moves up, Wei moves down
        nx = x + direction
        # One square forward
        if 0 <= nx < 8 and grid[nx][y] is None:
            moves.append((nx, y))
            # Two squares forward if not moved yet and both squares are empty
            nx2 = x + 2 * direction
            if not piece.has_moved and 0 <= nx2 < 8 and grid[nx2][y] is None:
                moves.append((nx2, y))
        # Diagonal captures
        for dy in [-1, 1]:
            ny = y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and grid[nx][ny] and grid[nx][ny].faction != piece.faction:
                moves.append((nx, ny))
        return moves

    def king_moves(self, pos, grid):
        x, y = pos
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    moves.append((nx, ny))
        return moves

    def queen_moves(self, pos, grid):
        return self.rook_moves(pos, grid) + self.bishop_moves(pos, grid)

    def rook_moves(self, pos, grid):
        x, y = pos
        moves = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                moves.append((nx, ny))
                if grid[nx][ny]:
                    break
        return moves

    def bishop_moves(self, pos, grid):
        x, y = pos
        moves = []
        for dx, dy in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                moves.append((nx, ny))
                if grid[nx][ny]:
                    break
        return moves

    def knight_moves(self, pos, grid):
        x, y = pos
        candidates = [
            (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
            (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)
        ]
        return [(nx, ny) for nx, ny in candidates if 0 <= nx < 8 and 0 <= ny < 8]

    def rally_ability(self, board, pos):
        print(f"[Ability] Rally activated at {pos}")
        row, col = pos
        faction = self.grid[row][col].faction
        for c in range(8):
            piece = self.grid[row][c]
            if piece and piece.faction == faction:
                piece.extra_moves = 1
                print(f"[Ability] {piece.name} at ({row},{c}) gets extra move.")
        return AbilityResult.END_TURN

    def swap_ability(self, board, pos):
        print(f"[Ability] Swap activated at {pos}")
        row, col = pos
        faction = self.grid[row][col].faction
        for r in range(8):
            if r != row:
                piece = self.grid[r][col]
                if piece and piece.faction == faction:
                    self.grid[row][col], self.grid[r][col] = self.grid[r][col], self.grid[row][col]
                    print(f"[Ability] Swapped with {piece.name} at ({r},{col})")
                    break
        # End the turn immediately after using swap, just like rally
        return AbilityResult.END_TURN

    def charge_ability(self, board, pos):
        print(f"[Ability] Charge activated at {pos}")
        row, col = pos
        piece = self.grid[row][col]
        piece.extra_moves = 2
        print(f"[Ability] {piece.name} at ({row},{col}) can move twice this turn.")
        return AbilityResult.ALLOW_EXTRA_MOVES