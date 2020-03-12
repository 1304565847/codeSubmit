from django.db import models

class Img(models.Model):
    imgMD5 = models.TextField()
    url = models.TextField()

    class Meta:
        db_table = "img"
        ordering = ['-id']