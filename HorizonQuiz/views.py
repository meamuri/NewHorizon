from HorizonQuiz.models import Question, AccuracyQuestion
from .my_unit import views_unit
from django.http import JsonResponse


def get_question(request):
    return views_unit.user_want_question(request, views_unit.WE_GET_QUESTION, Question)


def get_accuracy_question(request):
    return views_unit.user_want_question(request, views_unit.WE_GET_ACCURACY_QUESTION, AccuracyQuestion)


def get_answer(request, user_answer):
    return views_unit.user_want_take_answer(request, views_unit.WE_GET_QUESTION, int(user_answer))


def get_accuracy_answer(request, digit_of_answer):
    return views_unit.user_want_take_answer(request, views_unit.WE_GET_ACCURACY_QUESTION, int(digit_of_answer))


def get_play_map(reqeust, width=1, height=1):
    return JsonResponse({

    })
