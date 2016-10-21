from HorizonQuiz.models import Question, AccuracyQuestion
from HorizonQuiz.my_unit.model_unit import Region
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
    lst_areas = []
    lst_pos = []
    lst_sizes = []
    lst_urls = []
    for a in Region.objects.all():
        lst_areas.append(a.get_collection_of_area_as_strings())
        lst_pos.append(a.position())
        lst_sizes.append(a.sizes())
        lst_urls.append(a.url)
    return JsonResponse({
        'bg-image': 'some-url',
        'region-images': lst_urls,
        'region-poses': lst_pos,
        'region-areas': lst_areas,
        'region_sizes': lst_sizes
    })
