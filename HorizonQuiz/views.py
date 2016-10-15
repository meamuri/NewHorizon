from HorizonQuiz.models import Question, AccuracyQuestion
from django.http import JsonResponse
import random


def check_score(request, value):
    if 'score' not in request.session:
        request.session['score'] = 0
    if value == 0:
        request.session['score'] += 1


def clear_and_return(request, what_you_want_return):
    del request.session['session_status']
    del request.session['correct_answer']
    return JsonResponse({'correct': what_you_want_return})


def index(request):
    if 'session_status' not in request.session or request.session['session_status'] != 'we_get_question':
        data = random.choice(Question.objects.all())
        request.session['session_status'] = 'we_get_question'
        request.session['correct_answer'] = data.true_answer
        return JsonResponse(data.serialize())
    return clear_and_return(request, -1)


def get_answer(request, user_answer):
    if 'session_status' not in request.session:
        return JsonResponse({'correct': 'not in session'})

    if request.session['session_status'] != 'we_get_question':
        return clear_and_return(request, 'not in time')

    check_score(request, request.session['correct_answer'] - int(user_answer))
    res = JsonResponse({
        'correct': request.session['correct_answer'],
        'score': request.session['score']
    })

    del request.session['session_status']
    del request.session['correct_answer']
    return res


def get_accuracy_question(request):
    if 'session_status' not in request.session or request.session['session_status'] != 'get_accuracy_question':
        data = random.choice(AccuracyQuestion.objects.all())
        request.session['session_status'] = 'get_accuracy_question'
        request.session['correct_answer'] = data.true_answer
        return JsonResponse(data.serialize())
    return clear_and_return(request, 'we don\'t know your answer! F5 for new question')


def check_accuracy_answer(request, digit_of_answer):
    if 'session_status' not in request.session:
        return JsonResponse({'delta': 'not in session'})
    if request.session['session_status'] != 'get_accuracy_question':
        return clear_and_return(request, 'not in time')

    delta = abs(request.session['correct_answer'] - int(digit_of_answer))

    check_score(request, delta)

    res = JsonResponse({
        'delta': delta,
        'score': request.session['score']
    })
    del request.session['session_status']
    del request.session['correct_answer']
    return res
