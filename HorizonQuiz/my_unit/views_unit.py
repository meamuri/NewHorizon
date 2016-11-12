from django.http import JsonResponse
from HorizonQuiz.my_unit import game_logic
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
        clear_session(request)
        return JsonResponse({'correct': 'error', 'what happens': 'not in time'})


def clear_session(request):
    del request.session['session_status']
    del request.session['correct_answer']


def user_want_question(request, session_text, q_type):
    data = random.choice(q_type.objects.all())
    request.session['session_status'] = session_text
    request.session['correct_answer'] = data.true_answer
    return JsonResponse(data.serialize())


def user_want_take_answer(request, session_text, value):
    obj = check_session_status(request, session_text)
    if obj is not None:
        return JsonResponse({'error': 'error'})
    correct = request.session['correct_answer']
    clear_session(request)
    return {
        'correct': correct,
        'its_true_answer?': abs(correct - value) == 0,
    }


def fill_regions_info(num, areas, poses, sizes, urls, types, width=1, height=1):
    for a in Region.objects.all():
        if a.map_id == num:
            areas.append(a.get_collection_of_area_as_strings(width, height))
            poses.append(a.position(width, height))
            sizes.append(a.sizes())
            urls.append(a.reg_type.url)
            if a.is_capital_area:
                types.append(game_logic.WHOSE_AREA['capital_of_first'])
            else:
                types.append(game_logic.WHOSE_AREA['empty'])
    types[-1] = game_logic.WHOSE_AREA['capital_of_second']


def fill_game_map(curr_map, map_id, player, his_enemy):
    for obj in Region.objects.all():
        if obj.map_id == map_id:
            curr_map.append(obj)
            curr_map[-1].owner_id = -1
    curr_map[0].is_capital_area = curr_map[-1].is_capital_area = True
    curr_map[0].owner_id = player
    curr_map[-1].owner_id = his_enemy
