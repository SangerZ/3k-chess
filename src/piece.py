class Piece:
    def __init__(self, name, faction, symbol, movement_fn, ability_fn=None, piece_type=None):
        self.name = name
        self.faction = faction
        self.symbol = symbol
        self.movement_fn = movement_fn
        self.ability = ability_fn
        self.piece_type = piece_type
        self.has_used_ability = False
        self.extra_moves = 0
        self.has_moved = False

    def reset_ability(self):
        self.has_used_ability = False
        self.extra_moves = 0

    def can_use_ability(self):
        return self.ability is not None and not self.has_used_ability

    def use_ability(self, board, *args):
        if self.ability:
            return self.ability(board, *args)
        return None