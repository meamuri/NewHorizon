from HorizonQuiz.models import Question, AccuracyQuestion
from .my_unit import views_unit
from django.http import JsonResponse
from HorizonQuiz.my_unit import game_logic, map_model
import uuid


def get_enum_question(request):
    return views_unit.user_want_question(request, views_unit.WE_GET_ENUM_QUESTION, Question)


def get_accuracy_question(request):
    return views_unit.user_want_question(request, views_unit.WE_GET_ACCURACY_QUESTION, AccuracyQuestion)


def get_enum_answer(request, user_answer):
    return views_unit.user_want_take_answer(request, views_unit.WE_GET_ENUM_QUESTION, int(user_answer))


def get_accuracy_answer(request, digit_of_answer):
    return views_unit.user_want_take_answer(request, views_unit.WE_GET_ACCURACY_QUESTION, int(digit_of_answer))


def player_start_game(request, width=1, height=1, map_id=1):
    """
    Инициализация игры пользователем.
    Если он единственный игрок в очереди, он получает карту и ожидает
    Если уже кто-то ждет игры, пользователи объединяются в игровую комнату
    :param request: Запрос клиента
    :param width:   Ширина экрана устройства пользователя
    :param height:  Высота экрана устройства пользователя
    :param map_id:  id игрового поля
    :return:        Json, содержащий информацию об игровом поле
    """
    regions = map_model.get_regions_as_list(int(map_id), int(width), int(height))
    game_map = JsonResponse(regions)

    if not request.session.session_key:
        request.session.create()

    player_key = request.session.session_key
    if len(game_logic.players) == 0:  # or game_logic.players[0] == player_key:
        # если новый игрок единственный, кто ожидающий игру, добавляем его в очередь
        game_logic.players.append(player_key)
        return game_map

    enemy = game_logic.players[0]  # за врага принимаем первого в очереди
    game_logic.queue_of_gamers = game_logic.players[1:]  # и удаляем его из очереди

    game_id = uuid.uuid1()  # случайную уникальную комбинацию принимаем за игровой id
    init_game(player_key, enemy, game_id, int(map_id))  # инициализация карты, соперников, стадии игры

    return game_map


def init_game(player_key, his_enemy, game_id, map_id):
    game_logic.enemies[player_key] = his_enemy
    game_logic.enemies[his_enemy] = player_key

    game_logic.game_ids[player_key] = game_id  # id сессии нового игрока присваиваем словарю игровых сессий
    game_logic.game_ids[his_enemy] = game_id  # id сессии его врага присваиваем словарю игровых сессий

    game_logic.maps[game_id] = map_model.get_regions_as_list(map_id, player_key, his_enemy)
    game_logic.games[game_id] = game_logic.Game(player_who_comes_now=player_key,
                                                player_who_has_waited_some_times=his_enemy)


def game_center(request, num=1):
    player_key = request.session.session_key
    if player_key not in game_logic.game_ids:
        return JsonResponse({'error': 'the game is not initialized!'})

    current_game = game_logic.game_ids[player_key]  # ищем игру по id сессии
    enemy_of_player = game_logic.enemies[player_key]

    # if game_logic.game_turn[player_key] == game_logic.TURN_OF_GAME['check_fight_result'] or game_logic.game_turn[
    #     player_key] == game_logic.TURN_OF_GAME['check_accuracy']:
    #     round_up_or_resume(current_game)
    #     res = fight_result(request, int(num), player_key, enemy_of_player, current_game)
    #     return JsonResponse(res)
    #
    # # возможно, игрок player_key делает ход не в свой шаг
    # # чтобы это проверить, ищем в словаре whose_step айди игрока, чей ход. Ищем по ключу игры
    # if player_key != game_logic.whose_step[current_game]:
    #     return JsonResponse({'error': 'step is not your!'})
    #
    # return attack_area(request, int(num), player_key, enemy_of_player, current_game)


def attack_area(request, id_area, player_key, his_enemy, current_game):
    # Если игрок делает ход в свой ход, проверяем, что атакуемая область нейтральна или
    # занята врагом (не является занятой им же)
    if game_logic.maps[current_game][id_area] == player_key:
        return JsonResponse({'error': 'is your area!'})

    request.session['area_id'] = id_area
    if game_logic.maps[current_game][id_area] == -1:  # область нейтраьная
        game_logic.game_turn[player_key] = game_logic.TURN_OF_GAME['attack_neutral_area']
        game_logic.game_turn[his_enemy] = game_logic.TURN_OF_GAME['attack_neutral_area']
        return get_enum_question(request)

    game_logic.game_turn[player_key] = game_logic.TURN_OF_GAME['attack_enemy_area']
    game_logic.game_turn[his_enemy] = game_logic.TURN_OF_GAME['enemy_attack_me!!!']
    return get_enum_question(request)


def fight_result(request, user_answer, player_key, his_enemy, current_game):
    if game_logic.game_turn[player_key] == game_logic.TURN_OF_GAME['check_fight_result']:
        res_obj = get_enum_answer(request, user_answer)
    else:
        res_obj = get_accuracy_answer(request, user_answer)

    if 'error' in res_obj:
        return res_obj

    if res_obj['its_true_answer?']:
        curr_map = game_logic.maps[current_game]
        curr_map[request.session['area_id']] = player_key

    game_logic.whose_step[current_game] = his_enemy
    game_logic.game_turn[player_key] = game_logic.TURN_OF_GAME['wait_his_opponent']
    game_logic.game_turn[his_enemy] = game_logic.TURN_OF_GAME['can_make_move']
    return res_obj


def check_pair(request):
    return JsonResponse({'enemy': request.session.session_key in game_logic.game_ids})
