from django.db import models

# Create your models here.

class notes(models.Model):
    problem_id = models.CharField(max_length=10)
    text = models.TextField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"Note for {self.problem_id}"


class questions(models.Model):
    done = models.BooleanField(default=False)
    problem_id = models.CharField(max_length=10)
    title = models.TextField()
    rating = models.IntegerField()
    problem_link = models.URLField()
    solution_link = models.URLField()
    # tags = models.Choices() #  Check is this allows multiple choices
    star = models.BooleanField(default=False)
    notes = models.ForeignKey( notes ,on_delete=models.CASCADE, null=True, blank=True)




