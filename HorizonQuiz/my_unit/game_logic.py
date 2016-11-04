players = []         # players id
game_ids = dict()    # player_id ---> game_id
game_round = dict()  # game_id ---> step of game
game_turn = dict()   # game_id ---> TURN_OF_GAME[i]
maps = dict()        #
whose_step_in_game = dict()

TURN_OF_GAME = ('started', 'wait_question', 'want_check_answer', 'finished')
