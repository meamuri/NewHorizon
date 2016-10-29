from HorizonQuiz.models import Question, AccuracyQuestion
from HorizonQuiz.my_unit.model_unit import Region, Map
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


def get_play_map(request, width, height):
    lst_areas = []
    lst_pos = []
    lst_sizes = []
    lst_urls = []
    for a in Region.objects.all():
        if a.map_id == 1:
            lst_areas.append(a.get_collection_of_area_as_strings())
            lst_pos.append(a.position(width, height))
            lst_sizes.append(a.sizes(width, height))
            lst_urls.append(a.url)

    return JsonResponse({
        'bg-image': Map.objects.get(pk=1).url,
        'region-images': lst_urls,
        'region-poses': lst_pos,
        'region-areas': lst_areas,
        'region_sizes': lst_sizes
    })


def init_game(request, width=1, height=1):
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
    game_logic.game_ids[key] = game_id  # id сессии нового игрока присваиваем словарю игровых сессий
    game_logic.game_ids[enemy] = game_id  # id сессии его врага присваиваем словарю игровых сессий

    current_map = []
    for obj in Region.objects.all():
        if obj.map_id == 1:
            current_map.append(obj)
            current_map[-1].owner_id = -1
    current_map[0].is_capital_area = current_map[-1].is_capital_area = True
    current_map[0].owner_id = key
    current_map[-1].owner_id = enemy

    game_logic.maps[game_id] = current_map
    return game_map
