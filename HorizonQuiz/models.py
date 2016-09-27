from django.db import models
from django.http import JsonResponse


class Question(models.Model):
    image_url = models.CharField(max_length=256)
    question_text = models.CharField(max_length=256)
    answer_1 = models.CharField(max_length=128)
    answer_2 = models.CharField(max_length=128)
    answer_3 = models.CharField(max_length=128)
    answer_4 = models.CharField(max_length=128)

    def __str__(self):
        return self.question_text

    def to_json(self):
        return JsonResponse({
            'image': self.image_url,
            'text': self.question_text,
            'answers': [
                self.answer_1,
                self.answer_2,
                self.answer_3,
                self.answer_4
            ]
        })
