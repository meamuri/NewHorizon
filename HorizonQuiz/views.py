from HorizonQuiz.models import Question
from django.http import HttpResponse
import random


def index(request):
    data = random.choice(Question.objects.all()).to_json()
    return HttpResponse(str(data), content_type="application/json; charset=utf-8")


def get_answer(request, question_id):
    try:
        obj = Question.objects.get(pk=question_id)
    except (KeyError, Question.DoesNotExist):
        return HttpResponse(str(-1))
    else:
        return HttpResponse(str(obj.true_answer))
