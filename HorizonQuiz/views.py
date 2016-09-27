from django.http import JsonResponse


def index(request):
    return JsonResponse({
        'image': "some url",
        'text': "what's up?",
        'answers': [
            "ans1",
            "ans2",
            "ans3",
            "ans4"
        ]
    })

# Create your views here.
