from django.http import JsonResponse
from HorizonQuiz.my_unit.model_unit import Region
import random

WE_GET_ENUM_QUESTION = 'we_get_enum_question'
WE_GET_ACCURACY_QUESTION = 'we_get_accuracy_question'
PLAYER_STARTS_GAME = 'player_starts_game'


def check_and_inc_score(request, value):
    if 'score' not in request.session:
        request.session['score'] = 0
    if value == 0:
        request.session['score'] += 1


def check_session_status(request, session_text):
    if 'session_status' not in request.session:
        return JsonResponse({'correct': 'error', 'what happens': 'not in session'})
    if request.session['session_status'] != session_text:
        return clear_and_answer(request, {'correct': 'error', 'what happens': 'not in time'})


def clear_and_answer(request, what_you_want_return):
    del request.session['session_status']
    del request.session['correct_answer']
    return JsonResponse(what_you_want_return)


def user_want_question(request, session_text, q_type):
    data = random.choice(q_type.objects.all())
    request.session['session_status'] = session_text
    request.session['correct_answer'] = data.true_answer
    return JsonResponse(data.serialize())


def user_want_take_answer(request, session_text, value):
    obj = check_session_status(request, session_text)
    if obj is not None:
        return JsonResponse({'error': 'error'})
    delta = request.session['correct_answer'] - value
    check_and_inc_score(request, delta)
    return clear_and_answer(request, {'correct': request.session['correct_answer']})


def fill_regions_info(num, areas, poses, sizes, urls, width=1, height=1):
    for a in Region.objects.all():
        if a.map_id == num:
            areas.append(a.get_collection_of_area_as_strings())
            poses.append(a.position(width, height))
            sizes.append(a.sizes(width, height))
            urls.append(a.reg_type.url)


def fill_game_map(curr_map, player, his_enemy):
    for obj in Region.objects.all():
        if obj.map_id == 1:
            curr_map.append(obj)
            curr_map[-1].owner_id = -1
    curr_map[0].is_capital_area = curr_map[-1].is_capital_area = True
    curr_map[0].owner_id = player
    curr_map[-1].owner_id = his_enemy
