from django.http import JsonResponse
from HorizonQuiz.my_unit import views_unit, logic
from HorizonQuiz import views
import uuid


def player_start_game(request, width=1, height=1, map_id=1):
    """
    Контроллер, отвечающий инициализацию новой игры, подбор соперников
    и получение карты регионов
    :param request: запрос на сервер с устройства пользователя
    :param width: ширина экрана устройства пользователя
    :param height: высота экрана устройства пользователя
    :param map_id: идентификатор карты, на которой будет игра
    :return: JSON, содержащий ошибку или информацию о карте в случае корректности запроса
    """
    if request.session.session_key:
        return JsonResponse({'error:': 'you are start game'})

    request.session.save()
    request.session['situation'] = logic.SITUATION_FOR_PLAYER['start_game']
    player_key = request.session.session_key
    game_map = views_unit.get_play_map(player_key, int(map_id), int(width), int(height))
    if len(logic.players) == 0:
        logic.players.append(player_key)
        return game_map

    enemy = logic.players[0]  # за врага принимаем первого в очереди
    logic.players = logic.players[1:]  # и удаляем его из очереди

    game_id = uuid.uuid1()  # случайную уникальную комбинацию принимаем за игровой id
    init_game(player_key, enemy, game_id, int(map_id))  # инициализация карты, соперников, стадии игры
    return game_map


def player_want_search_opponent(request, opp_id):
    if not request.session.session_key:
        request.session.save()
    else:
        return JsonResponse({'error:': 'you are start game'})


def init_game(player_key, his_enemy, game_id, map_id):
    """
    Функция инициализирует игру, когда в очереди найдены
    два соперника.
    :param player_key: игрок, который только подключился
    :param his_enemy: игрок, который давно ждал оппонента
    :param game_id: идентификатор, присвоенный новой игре
    :param map_id: идентификатор карты, на которой будет происходить игра
    :return: NONE
    """
    logic.game_ids[player_key] = game_id
    logic.game_ids[his_enemy] = game_id
    logic.enemies[player_key] = his_enemy
    logic.enemies[his_enemy] = player_key

    current_map = views_unit.get_game_map_from_model(map_id)  # распределяем локации на карте
    the_game = logic.Game(player_key=player_key, his_enemy=his_enemy)
    the_game.game_map.set_regions(current_map)

    the_game.game_map.set_capitals()
    logic.games[game_id] = the_game


def game_center(request, num=1):
    player_key = request.session.session_key
    if player_key not in logic.game_ids:
        return JsonResponse({'error': 'the game is not initialized!'})

    game_id = logic.game_ids[player_key]
    the_game = logic.games[game_id]
    if not the_game.is_your_step(player_key=player_key):
        return JsonResponse({'error': 'not your step!!'})

    val = int(num)
    if the_game.game_turn == logic.TURN_OF_GAME['check']:
        request.session['url_answer'] = val
        res = fight_result(request=request, current_game=the_game, player_key=player_key)
        return JsonResponse(res)

    if the_game.is_area_him(this_player_key=player_key, checked_area=request.session['value']):
        return JsonResponse({'error': 'is your area!'})

    if request.session['situation'] == logic.SITUATION_FOR_PLAYER['start_game']:
        request.session['url_area'] = val
        area_condition = the_game.get_area_state(val)
        if area_condition == logic.AREA_CONDITION['neutral']:
            request.session['count'] = 1
            request.session['situation'] = logic.SITUATION_FOR_PLAYER['attack_neutral']
        elif area_condition == logic.AREA_CONDITION['of_enemy']:
            request.session['count'] = 1
            request.session['situation'] = logic.SITUATION_FOR_PLAYER['attack_enemy']
        else:
            request.session['count'] = 3
            request.session['situation'] = logic.SITUATION_FOR_PLAYER['attack_capital']

    return attack_area(request, current_game=the_game)


def attack_area(request, current_game):
    current_game.game_turn = logic.TURN_OF_GAME['check']

    if request.session['situation'] == logic.SITUATION_FOR_PLAYER['attack_neutral'] or request.session['count'] != 1:
        return views.get_enum_question(request)

    return views.get_accuracy_question(request)


def fight_result(request, current_game, player_key):
    user_answer = request.session['url_answer']
    if (request.session['situation'] == logic.SITUATION_FOR_PLAYER['attack_capital'] or request.session['situation']
            == logic.SITUATION_FOR_PLAYER['attack_enemy']) and request.session['count'] == 0:
        res = views.get_accuracy_answer(request, user_answer)
    else:
        res = views.get_enum_answer(request, user_answer)

    if 'error' in res:
        return res

    request.session['count'] -= 1
    if res['its_true_answer?']:
        current_game.change_map(player_who_win=player_key, area_id=request.session['url_area'])
    else:
        pass

    current_game.switch_whose_step(key_of_player_whose_step_now=player_key)
    current_game.change_turn(it_was_fight=False)

    return res
