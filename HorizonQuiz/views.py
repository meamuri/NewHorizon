from HorizonQuiz.models import Question, AccuracyQuestion
from .my_unit import views_unit
from django.http import JsonResponse
from HorizonQuiz.my_unit import game_logic, map_model
import uuid
from push_notifications.models import APNSDevice, GCMDevice


def get_enum_question(request):
    res = views_unit.user_want_question(request, views_unit.WE_GET_ENUM_QUESTION, Question)
    return JsonResponse(res)


def get_accuracy_question(request):
    res = views_unit.user_want_question(request, views_unit.WE_GET_ACCURACY_QUESTION, AccuracyQuestion)
    return JsonResponse(res)


def get_enum_answer(request, user_answer):
    res = views_unit.user_want_take_answer(request, views_unit.WE_GET_ENUM_QUESTION, int(user_answer))
    return JsonResponse(res)


def get_accuracy_answer(request, digit_of_answer):
    res = views_unit.user_want_take_answer(request, views_unit.WE_GET_ACCURACY_QUESTION, int(digit_of_answer))
    return JsonResponse(res)


def clear_all_of_user(key):
    del game_logic.enemies[key]
    del game_logic.game_ids[key]


def drop_old_session(request):
    key = request.session.session_key
    if game_logic.game_ids.get(key) is None:
        return False

    del game_logic.games[game_logic.game_ids[key]]
    enemy = game_logic.enemies[key]
    clear_all_of_user(key)
    clear_all_of_user(enemy)
    return True


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

    if request.session.session_key:
        drop_old_session(request)

    regions = map_model.get_play_map_as_dict(int(map_id), int(width), int(height))
    game_map = JsonResponse(regions)

    request.session.save()
    player_key = request.session.session_key
    if len(game_logic.players) == 0:  # or game_logic.players[0] == player_key:
        # если новый игрок единственный, кто ожидающий игру, добавляем его в очередь
        game_logic.players.append(player_key)
        return game_map

    if game_logic.players[0] == player_key:
        return game_map

    enemy = game_logic.players[0]  # за врага принимаем первого в очереди
    game_logic.players = game_logic.players[1:]  # и удаляем его из очереди

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

    current_game_id = game_logic.game_ids[player_key]  # ищем игру по id сессии
    the_game = game_logic.games[current_game_id]
    if the_game.status_for_player[player_key] == game_logic.TURN_STATUS['player_wait_step']:
        return JsonResponse({'error': 'not your step!'})

    enemy_of_player = game_logic.enemies[player_key]
    num = int(num)  # из url параметр пришел строкой. Получаем число

    one = the_game.status_for_player[player_key] == game_logic.TURN_STATUS['check_enum_quest']
    if one or the_game.status_for_player[player_key] == game_logic.TURN_STATUS['check_accuracy_question']:
        res = fight_result(request=request,
                           user_answer=num,
                           player_key=player_key,
                           his_enemy=enemy_of_player,
                           the_game=the_game)
        return JsonResponse(res)

    if the_game.status_for_player[player_key] == game_logic.TURN_STATUS['player_can_attack']:
        check = game_logic.init_round(the_game=the_game, area_id=num, player_key=player_key, his_enemy=enemy_of_player)
        if 'error' in check:
            return JsonResponse(check)

    return attack_area(request=request,
                       player_key=player_key,
                       the_game=the_game)


def attack_area(request, player_key, the_game):
    if the_game.round_state[player_key] == game_logic.TURN_STATUS['get_me_enum_question']:
        the_game.status_for_player[player_key] = game_logic.TURN_STATUS['check_enum_quest']
        return get_enum_question(request)
    else:
        the_game.status_for_player[player_key] = game_logic.TURN_STATUS['check_accuracy_question']
        return get_accuracy_question(request)


def fight_result(request, user_answer, player_key, his_enemy, the_game):
    if the_game.status_for_player[player_key] == game_logic.TURN_STATUS['check_enum_quest']:
        what_we_want = views_unit.WE_GET_ENUM_QUESTION
    else:
        what_we_want = views_unit.WE_GET_ACCURACY_QUESTION
    res_obj = views_unit.user_want_take_answer(request, what_we_want, int(user_answer))

    if 'error' in res_obj:
        return res_obj

    answer = 'taken_'+str(res_obj['its_true_answer?']).lower()+'_answer'
    the_game.round_state[player_key] = game_logic.TURN_STATUS[answer]

    def answer_of_enemy(x):
        return the_game.round_state[his_enemy] == game_logic.TURN_STATUS['taken_' + x + '_answer']

    fight_for_neutral = the_game.game_status['what_was_attacked'] == game_logic.TURN_STATUS['attacked_neutral_area']
    if fight_for_neutral or answer_of_enemy('true') or answer_of_enemy('false'):
        the_game.resume_part_of_round()  # resume step -> должна уметь делать игра!

    return res_obj


def get_curr_map(request):
    key = request.session.session_key
    the_game = game_logic.games[game_logic.game_ids[key]]
    return JsonResponse({
        'you_are': the_game.key_to_player_id(key),
        'map': the_game.regions,
    })


def check_pair(request):
    return JsonResponse({'enemy': request.session.session_key in game_logic.game_ids})
