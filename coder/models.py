from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    endTime = models.DateTimeField()

    class Meta:
        db_table = "question"
        ordering = ['-id']
    
    def __str__(self):
        return self.title

class VerCode(models.Model):

    id = models.IntegerField(primary_key=True)
    email = models.EmailField()
    code = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        db_table = "VerCode"
    
    def __str__(self):
        return f"{self.email}-{self.code}"

class Answer(models.Model):

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(null=True)
    content = models.TextField()

    class Meta:
        db_table = "Answer"
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.user.username}-{self.question.title}"