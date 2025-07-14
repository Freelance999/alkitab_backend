from django.db import models

class Home(models.Model):
    title = models.CharField(("title"), max_length=255)
    text = models.TextField(("text"))
    phone = models.IntegerField(("phone"), null=True, blank=True)
    email = models.EmailField(("email"), null=True, blank=True)

    def __str__(self) -> str:
        return self.title
