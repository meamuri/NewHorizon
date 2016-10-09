from HorizonQuiz.models import Question
from django.http import JsonResponse
import random


def index(request):
    if request.session.get('QuestionIssued', False):
        quest_by_id = Question.objects.get(pk=request.session['quest_id'])
        del request.session['QuestionIssued']
        del request.session['quest_id']
        return JsonResponse({
            'correct': quest_by_id.true_answer
        })
    else:
        data = random.choice(Question.objects.all()).serialize()
        request.session['QuestionIssued'] = True
        request.session['quest_id'] = data['id']
        return JsonResponse(data)  # HttpResponse(str(data), content_type="application/json; charset=utf-8")


def get_answer(request, question_id):
    try:
        quest_by_id = Question.objects.get(pk=question_id)
    except (KeyError, Question.DoesNotExist):
        return JsonResponse({'correct': -1})  # str(-1), content_type="application/json; charset=utf-8")
    else:
        return JsonResponse({'correct': quest_by_id.true_answer})
