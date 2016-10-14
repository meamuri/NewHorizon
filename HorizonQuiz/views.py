from HorizonQuiz.models import Question, AccuracyQuestion
from django.http import JsonResponse
import random


def index(request):
    if 'session_status' in request.session and request.session['session_status'] == 'we_know_answer':
        res = JsonResponse({'correct': request.session['true_answer']})
        del request.session['session_status']
        del request.session['true_answer']
        del request.session['quest_id']
        return res
    elif 'session_status' in request.session and request.session['session_status'] == 'we_get_question':
        del request.session['session_status']
        del request.session['true_answer']
        del request.session['quest_id']
        return JsonResponse({'correct': -1})
    else:
        data = random.choice(Question.objects.all())
        request.session['session_status'] = 'we_get_question'
        request.session['true_answer'] = data.true_answer
        request.session['quest_id'] = data.id
        return JsonResponse(data.serialize())


def get_answer(request, user_answer):
    if 'session_status' in request.session and request.session['session_status'] == 'we_get_question':
        if user_answer == request.session['true_answer']:
            request.session['true_answer'] = 'true'
        else:
            request.session['true_answer'] = 'false'
        request.session['session_status'] = 'we_know_answer'
        return JsonResponse({'answer': 'checked'})
    return JsonResponse({'correct': 'not in time'})


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
        res = JsonResponse({
            'answer': AccuracyQuestion.objects.get(pk=request.session['quest_id']).check_delta(digit_of_answer)
        })
        del request.session['session_status']
        del request.session['quest_id']
        return res
    return JsonResponse({'correct': 'please, get question by url:'})
