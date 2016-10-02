from HorizonQuiz.models import Question
from django.http import HttpResponse
import random


def index(request):
    data = random.choice(Question.objects.all()).to_json()
    return HttpResponse(str(data), content_type="application/json; charset=utf-8")


def get_answer(request, question_id):
    try:
        quest_by_id = Question.objects.get(pk=question_id)
    except (KeyError, Question.DoesNotExist):
        return HttpResponse(str(-1), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse(str(quest_by_id.true_answer), content_type="application/json; charset=utf-8")
