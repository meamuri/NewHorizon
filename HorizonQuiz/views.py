from HorizonQuiz.models import Question, AccuracyQuestion
from HorizonQuiz.my_unit.model_unit import *
from .my_unit import views_unit
from django.http import JsonResponse
from HorizonQuiz.my_unit import game_logic
import uuid


def get_enum_question(request):
    return views_unit.user_want_question(request, views_unit.WE_GET_ENUM_QUESTION, Question)


def get_accuracy_question(request):
    return views_unit.user_want_question(request, views_unit.WE_GET_ACCURACY_QUESTION, AccuracyQuestion)


def get_enum_answer(request, user_answer):
    return views_unit.user_want_take_answer(request, views_unit.WE_GET_ENUM_QUESTION, int(user_answer))


def get_accuracy_answer(request, digit_of_answer):
    return views_unit.user_want_take_answer(request, views_unit.WE_GET_ACCURACY_QUESTION, int(digit_of_answer))


def attack_area(request, id_area):
    key = request.session.session_key  # получаем ключ игрока, который делает ход
    current_game = game_logic.game_ids[key]  # ищем его игру по этому ключу

    # возможно, он делает ход не в свой шаг
    # чтобы это проверить, ищем в словаре whose_step айди игрока, чей ход. Ищем по ключу игры
    if key != game_logic.whose_step_in_game[current_game]:
        return JsonResponse({'error': 'step is not your!'})

    # Если игрок делает ход в свой ход, проверяем, что атакуемая область нейтральна или
    # занята врагом (не является занятой им же)
    if game_logic.maps[current_game][id_area] == key:
        return JsonResponse({'error': 'is your area!'})

    # Если все хорошо, получаем вопрос
    return get_enum_question(request)


def get_play_map(request, width, height):
    lst_areas = []
    lst_pos = []
    lst_sizes = []
    lst_urls = []

    views_unit.fill_regions_info(2, lst_areas, lst_pos, lst_sizes, lst_urls, width, height)
    views_unit.fill_regions_info(1, lst_areas, lst_pos, lst_sizes, lst_urls, width, height)
    views_unit.fill_regions_info(3, lst_areas, lst_pos, lst_sizes, lst_urls, width, height)

    return JsonResponse({
        'bg-image': Map.objects.get(pk=1).url,
        'region-images': lst_urls,
        'region-poses': lst_pos,
        'region-areas': lst_areas,
        'region_sizes': lst_sizes
    })


def init_game(request, width=1, height=1):
    request.session['session_status'] = views_unit.PLAYER_STARTS_GAME
    game_map = get_play_map(request, int(width), int(height))
    key = request.session.session_key

    # если он единственный, ожидающий игру, добавляем его в очередь
    if len(game_logic.players) == 0:
        game_logic.players.append(key)
        return game_map

    # если есть игроки, создаем игру
    enemy = game_logic.players[0]  # за врага принимаем первого в очереди
    game_logic.queue_of_gamers = game_logic.players[1:]  # и удаляем его из очереди

    game_id = uuid.uuid1()  # случайную уникальную комбинацию принимаем за игровой id
    game_logic.whose_step_in_game[game_id] = key  # игра начинается с того игрока, который только пришел
    # его соперник, возможно, уже отчаялся ждать и отложил устройство

    game_logic.game_ids[key] = game_id  # id сессии нового игрока присваиваем словарю игровых сессий
    game_logic.game_ids[enemy] = game_id  # id сессии его врага присваиваем словарю игровых сессий
    game_logic.game_round[game_id] = 0

    current_map = []
    views_unit.fill_game_map(current_map, key, enemy)
    game_logic.maps[game_id] = current_map

    return game_map
