players = []         # players keys
enemies = dict()     # player_key ---> player_id (his enemy)
game_ids = dict()    # player_key ---> game_id
game_turn = dict()   # player_key ---> TURN_OF_GAME[k]
game_round = dict()  # game_id ---> step of game
maps = dict()        # game_id ---> regions
whose_step = dict()  # game_id ---> player_key
players_id = dict()  # player_key ---> player_id

TURN_OF_GAME = {
    'can_make_move': 0,
    'attack_area': 1,
    'check_round': 2,
    'finished': 3,
}


class GameMap:
    regions = []
    capitals = [0, 0]  # индексы тех регионов, которые являются столицами


class Game:
    players_parties = dict()  # стороны конфликта, 1 и 2
    round = 0
    game_turn = dict()
    game_round = 0

    def __init__(self, player_key, his_enemy):
        self.player_who_come_later = player_key
        self.player_who_wait_games = his_enemy
        self.players_parties[player_key] = 1
        self.players_parties[his_enemy] = 2
        self.whose_step = player_key
        self.game_map = GameMap()
        self.game_turn[self.round] = TURN_OF_GAME['round_start']
