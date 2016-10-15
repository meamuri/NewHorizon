from HorizonQuiz.models import Question, AccuracyQuestion
from .my_unit import views_unit


def get_question(request):
    return views_unit.user_want_question(request, 'we_get_question', Question)


def get_accuracy_question(request):
    return views_unit.user_want_question(request, 'get_accuracy_question', AccuracyQuestion)


def get_answer(request, user_answer):
    views_unit.check_session_status(request, 'we_get_question')
    delta = request.session['correct_answer'] - int(user_answer)
    views_unit.check_and_inc_score(request, delta)
    return views_unit.clear_and_answer(request, {'correct': request.session['correct_answer']})


def get_accuracy_answer(request, digit_of_answer):
    views_unit.check_session_status(request, 'get_accuracy_question')
    delta = abs(request.session['correct_answer'] - int(digit_of_answer))
    views_unit.check_and_inc_score(request, delta)
    return views_unit.clear_and_answer(request, {'delta': delta})
