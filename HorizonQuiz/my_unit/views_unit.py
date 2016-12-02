from django.http import JsonResponse
from HorizonQuiz.my_unit.map_model import Region
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


