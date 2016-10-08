from HorizonQuiz.models import Question
from django.http import JsonResponse
import random


def index(request):
    data = random.choice(Question.objects.all()).serialize()
    return JsonResponse(data)  # HttpResponse(str(data), content_type="application/json; charset=utf-8")


def get_answer(request, question_id):
    try:
        quest_by_id = Question.objects.get(pk=question_id)
    except (KeyError, Question.DoesNotExist):
        return JsonResponse({'correct': -1})  # str(-1), content_type="application/json; charset=utf-8")
    else:
        return JsonResponse({'correct': quest_by_id.true_answer})
