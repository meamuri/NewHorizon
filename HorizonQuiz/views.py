from HorizonQuiz.models import Question
from django.http import HttpResponse
import random


def index(request):
    json_string = random.choice(Question.objects.all()).to_json()
    return HttpResponse(json_string)


def get_answer(request, question_id):
    return HttpResponse(str(Question.objects.get(pk=question_id).true_answer))
