from HorizonQuiz.models import Question, AccuracyQuestion
from django.http import JsonResponse
import random


def index(request):
    if 'session_status' not in request.session or request.session['session_status'] != 'we_get_question':
        data = random.choice(Question.objects.all())
        request.session['session_status'] = 'we_get_question'
        request.session['true_answer'] = data.true_answer
        return JsonResponse(data.serialize())

    # if request.session['session_status'] == 'we_get_question':
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
    if 'session_status' in request.session and request.session['session_status'] == 'get_accuracy_question':
        del request.session['session_status']
        del request.session['quest_id']
        return JsonResponse({'oops': 'we don\'t know your answer! F5 for new question'})
    else:
        data = random.choice(AccuracyQuestion.objects.all())
        request.session['session_status'] = 'get_accuracy_question'
        request.session['quest_id'] = data.id
        return JsonResponse(data.serialize())


def check_accuracy_answer(request, digit_of_answer):
    if 'session_status' in request.session and request.session['session_status'] == 'get_accuracy_question':
        delta = AccuracyQuestion.objects.get(pk=request.session['quest_id']).check_delta(digit_of_answer)

        if 'score' not in request.session:
            request.session['score'] = 0
        elif delta == 0:
            request.session['score'] += 1

        res = JsonResponse({
            'answer': delta,
            'score': request.session['score']
        })
        del request.session['session_status']
        del request.session['quest_id']
        return res
    return JsonResponse({'correct': 'please, get question by url:'})
