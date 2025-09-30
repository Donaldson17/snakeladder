## 🎮 `game.py`

import random
import uuid

# snakes and ladders map
JUMPS = {
    16: 6, 46: 25, 49: 11, 62: 19, 64: 60, 74: 53,
    89: 68, 92: 88, 95: 75, 99: 80,   # snakes
    2: 38, 7: 14, 8: 31, 15: 26, 21: 42, 28: 84,
    36: 44, 51: 67, 71: 91, 78: 98, 87: 94  # ladders
}

class Game:
    def __init__(self, max_players=2, target=100):
        self.id = str(uuid.uuid4())
        self.max_players = max_players
        self.target = target
        self.players = []  # list of dicts
        self.turn = 0
        self.winner = None
        self.started = False

    def add_player(self, name):
        if len(self.players) >= self.max_players:
            return None
        player = {"id": str(uuid.uuid4()), "name": name, "position": 0}
        self.players.append(player)
        if len(self.players) == self.max_players:
            self.started = True
        return player

    def roll(self, player_id):
        if not self.started or self.winner:
            return None, "Game not ready or already finished"

        current_player = self.players[self.turn]
        if current_player["id"] != player_id:
            return None, "Not your turn"

        dice = random.randint(1, 6)
        new_pos = current_player["position"] + dice

        if new_pos > self.target:
            new_pos = current_player["position"]  # overshoot, no move

        # snakes or ladders
        new_pos = JUMPS.get(new_pos, new_pos)
        current_player["position"] = new_pos

        result = {
            "player": current_player["name"],
            "roll": dice,
            "new_position": new_pos
        }

        # check winner
        if new_pos == self.target:
            self.winner = current_player
            result["winner"] = current_player["name"]

        # next turn
        self.turn = (self.turn + 1) % len(self.players)
        return result, None

    def state(self):
        return {
            "id": self.id,
            "players": self.players,
            "turn": self.turn,
            "winner": self.winner,
            "started": self.started
        }
