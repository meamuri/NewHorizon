from HorizonQuiz.models import Question
import random


def index(request):
    return random.choice(Question.objects.all()).to_json()

# Create your views here.
