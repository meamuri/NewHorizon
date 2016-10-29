from HorizonQuiz.models import Question, AccuracyQuestion
from HorizonQuiz.my_unit.model_unit import Region
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


def get_play_map(reqeust, width=1, height=1):
    lst_areas = []
    lst_pos = []
    lst_sizes = []
    lst_urls = []
    for a in Region.objects.all():
        lst_areas.append(a.get_collection_of_area_as_strings())
        lst_pos.append(a.position(int(width), int(height)))
        lst_sizes.append(a.sizes(int(width), int(height)))
        lst_urls.append(a.url)

    return JsonResponse({
        'bg-image': 'some-url',
        'region-images': lst_urls,
        'region-poses': lst_pos,
        'region-areas': lst_areas,
        'region_sizes': lst_sizes
    })


def init_game(request):
    key = request.session.session_key

    # если он единственный, ожидающий игру, добавляем его в очередь
    if len(game_logic.players) == 0:
        game_logic.players.append(key)
        return JsonResponse(dict())

    # если есть игроки, создаем игру
    enemy = game_logic.players[0]  # за врага принимаем первого в очереди
    game_logic.queue_of_gamers = game_logic.players[1:]  # и удаляем его из очереди

    game_id = uuid.uuid1()  # случайную уникальную комбинацию принимаем за игровой id
    game_logic.game_ids[key] = game_id  # id сессии нового игрока присваиваем словарю игровых сессий
    game_logic.game_ids[enemy] = game_id  # id сессии его врага присваиваем словарю игровых сессий

    game_logic.maps[game_id] = dict()
    return JsonResponse(dict())
