from HorizonQuiz.models import Question
from django.http import HttpResponse
import random


def index(request):
    return random.choice(Question.objects.all()).to_json()


def get_answer(request, question_id):
    return HttpResponse(str(Question.objects.get(pk=question_id).true_answer))
