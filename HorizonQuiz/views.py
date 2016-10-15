from HorizonQuiz.models import Question, AccuracyQuestion
from django.http import JsonResponse
import random


def index(request):
    if 'session_status' not in request.session or request.session['session_status'] != 'we_get_question':
        data = random.choice(Question.objects.all())
        request.session['session_status'] = 'we_get_question'
        request.session['true_answer'] = data.true_answer
        return JsonResponse(data.serialize())

    # request.session['session_status'] == 'we_get_question':
    del request.session['session_status']
    del request.session['true_answer']
    return JsonResponse({'correct': -1})


def get_answer(request, user_answer):
    if 'session_status' not in request.session:
        return JsonResponse({'correct': 'not in session'})

    if request.session['session_status'] != 'we_get_question':
        del request.session['session_status']
        del request.session['true_answer']
        return JsonResponse({
            'correct': 'not in time',
            'status is': request.session['session_status']
        })

    if 'score' not in request.session:
        request.session['score'] = 0
    if request.session['true_answer'] == int(user_answer):
        request.session['score'] += 1

    res = JsonResponse({
        'correct': request.session['true_answer'],
        'score': request.session['score']
    })

    del request.session['session_status']
    del request.session['true_answer']
    return res


def get_accuracy_question(request):
    if 'session_status' not in request.session or request.session['session_status'] != 'get_accuracy_question':
        data = random.choice(AccuracyQuestion.objects.all())
        request.session['session_status'] = 'get_accuracy_question'
        request.session['true_answer'] = data.true_answer
        return JsonResponse(data.serialize())

    del request.session['session_status']
    del request.session['true_answer']
    return JsonResponse({'oops': 'we don\'t know your answer! F5 for new question'})


def check_accuracy_answer(request, digit_of_answer):
    if 'session_status' not in request.session:
        return JsonResponse({'correct': 'not in session'})

    if request.session['session_status'] != 'get_accuracy_question':
        del request.session['session_status']
        del request.session['true_answer']
        return JsonResponse({
            'correct': 'not in time',
            'status is': request.session['session_status']
        })

    if 'score' not in request.session:
        request.session['score'] = 0

    delta = abs(request.session['true_answer'] - int(digit_of_answer))
    if delta == 0:
        request.session['score'] += 1

    res = JsonResponse({
        'correct': delta,
        'score': request.session['score']
    })

    del request.session['session_status']
    del request.session['true_answer']
    return res
