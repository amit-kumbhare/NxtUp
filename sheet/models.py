from django.db import models

# Create your models here.

class notes(models.Model):
    problem_id = models.CharField(max_length=10)
    text = models.TextField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"Note for {self.problem_id}"


class question(models.Model):
    problem_id = models.CharField(max_length=10)
    title = models.TextField(max_length=100)
    rating = models.IntegerField()
    problem_link = models.URLField()
    solution_link = models.URLField(blank=True)
    # tags = models.Choices() #  Check is this allows multiple choices
    star = models.BooleanField(default=False)
    notes = models.ForeignKey( notes ,on_delete=models.CASCADE, null=True, blank=True)

    question_category = [
    ("<1300","<1300"),
    ("<1500","<1500"),
    ("<1700","<1700")
    ]
    category = models.CharField(max_length=7, choices=question_category, default="Unrated")

class user(models.Model):
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=20)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    handle = models.CharField(max_length=20)
    age = models.IntegerField() # Search how to add limit to it
    country = models.CharField(max_length=15)
    current_role = models.TextField(max_length=50)
    bio = models.TextField(max_length= 150)

    



