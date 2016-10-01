from HorizonQuiz.models import Question
from django.http import HttpResponse
import random


def index(request):
    json_string = random.choice(Question.objects.all()).to_json()
    return HttpResponse(json_string)


def get_answer(request, question_id):
    try:
        obj = Question.objects.get(pk=question_id)
    except (KeyError, Question.DoesNotExist):
        return HttpResponse(str(-1))
    else:
        return HttpResponse(str(obj.true_answer))
