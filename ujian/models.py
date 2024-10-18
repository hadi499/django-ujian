from django.db import models

class Ujian(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="time in second")
    required_score_to_pass = models.FloatField()
    def __str__(self):
        return self.name

class Pertanyaan(models.Model):
    ujian = models.ForeignKey(Ujian, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.title
