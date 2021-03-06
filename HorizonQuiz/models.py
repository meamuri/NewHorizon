from django.db import models


class Question(models.Model):
    image_url = models.CharField(max_length=256)
    question_text = models.CharField(max_length=256)
    answer_1 = models.CharField(max_length=128)
    answer_2 = models.CharField(max_length=128)
    answer_3 = models.CharField(max_length=128)
    answer_4 = models.CharField(max_length=128)
    true_answer = models.IntegerField(default=1)

    def __str__(self):
        return 'id - ' + str(self.id) + '; ' + self.question_text + ' [' + str(self.true_answer) + ']'

    def serialize(self):
        return dict(id=self.id, image=self.image_url, text=self.question_text, answers=[
            self.answer_1,
            self.answer_2,
            self.answer_3,
            self.answer_4,
        ])


class AccuracyQuestion(models.Model):
    image_url = models.CharField(max_length=256)
    question_text = models.CharField(max_length=256)
    true_answer = models.IntegerField(default=1)

    def __str__(self):
        return 'id - ' + str(self.id) + '; ' + self.question_text + ' [' + str(self.true_answer) + ']'

    def serialize(self):
        return dict(id=self.id, image=self.image_url, text=self.question_text)

    def check_delta(self, num):
        return abs(self.true_answer - int(num))
