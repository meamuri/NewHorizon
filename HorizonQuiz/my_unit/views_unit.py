from django.http import JsonResponse
import random


def check_and_inc_score(request, value):
    if 'score' not in request.session:
        request.session['score'] = 0
    if value == 0:
        request.session['score'] += 1


def check_session_status(request, session_text):
    if 'session_status' not in request.session:
        return JsonResponse({'correct': 'not in session'})
    if request.session['session_status'] != session_text:
        return clear_and_answer(request, {'error': 'not in time'})


def clear_and_answer(request, what_you_want_return):
    res = JsonResponse(what_you_want_return)
    del request.session['session_status']
    del request.session['correct_answer']
    return res


def user_want_question(request, session_text, q_type):
    data = random.choice(q_type.objects.all())
    request.session['session_status'] = session_text
    request.session['correct_answer'] = data.true_answer
    return JsonResponse(data.serialize())
