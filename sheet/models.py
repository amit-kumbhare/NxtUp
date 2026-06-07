from enum import unique
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class user(AbstractUser): 
    # standard Fields
    profile_pic = models.URLField(null=True, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    handle = models.CharField(max_length=20, unique=True, blank=False, null = False)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], null=True, blank=True)
    country = models.CharField(max_length=15, null=True, blank=True)
    current_role = models.TextField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length= 150, null=True, blank=True)
    last_sync = models.DateTimeField(auto_now_add=True)

    # Profile Data
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)],default=0)
    MaxRating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)], default=0)
    rank = models.TextField(max_length=50, default="Unranked")

    # User Stats
    solved_count = models.IntegerField(default=0)
    
    # Other profile Data
    leetcode_handle = models.CharField(max_length=20, unique=True, blank=True,null=True)
    github_handle = models.CharField(max_length=20, unique=True, blank=True,null=True)

    # Goals and Target
    target_rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(3500)],default=1500)
    target_rank = models.TextField(max_length=50,default="Expert")
    target_problems = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(15)],default=1)
    target_contest = models.TextField(max_length=25,default="At least 2/Month")
    
class question(models.Model):
    contestId = models.CharField(max_length=10)
    index = models.CharField(max_length=10)
    problem_id = models.CharField(max_length=10, unique=True)
    title = models.TextField(max_length=100)
    rating = models.IntegerField()
    tags = models.JSONField(default=list,blank=True)

class sheet_question(models.Model):
    contestId = models.CharField(max_length=10)
    index = models.CharField(max_length=10)
    problem_id = models.CharField(max_length=10, unique=True)
    title = models.TextField(max_length=100)
    rating = models.IntegerField()
    tags = models.JSONField(default=list,blank=True)

class UserTopicStats(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='topic_wise')
    
    graphs          = models.IntegerField(default=0)
    dp              = models.IntegerField(default=0)
    greedy          = models.IntegerField(default=0)
    binary_search   = models.IntegerField(default=0)
    data_structures = models.IntegerField(default=0)
    math            = models.IntegerField(default=0)
    strings         = models.IntegerField(default=0)
    dfs             = models.IntegerField(default=0)
    shortest_paths  = models.IntegerField(default=0)
    trees           = models.IntegerField(default=0)
    two_pointer     = models.IntegerField(default=0)
    sliding_window  = models.IntegerField(default=0)
    implementation  = models.IntegerField(default=0)
    dsu             = models.IntegerField(default=0)
    bitmasks        = models.IntegerField(default=0)

class UserDifficultyStats(models.Model):
    user   = models.OneToOneField(user, on_delete=models.CASCADE, related_name='difficulty')
    easy   = models.IntegerField(default=0)
    medium = models.IntegerField(default=0)
    hard   = models.IntegerField(default=0)

class submission(models.Model):
    solver = models.ForeignKey(user, on_delete=models.CASCADE)
    problem = models.ForeignKey(question, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=50)
    timestamp = models.DateField()

    class Meta:
        unique_together = ('solver','problem')

class star(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE )
    problem = models.ForeignKey(sheet_question, on_delete=models.CASCADE)

class notes(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="notes")
    problem = models.ForeignKey(sheet_question, on_delete=models.CASCADE, null=True, blank=True)  # Link to actual problem
    text = models.TextField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"Note for {self.problem_id or self.problem} by {self.user}"

@receiver(post_save,sender=user)
def create_user_stats(sender,instance, created, **kwargs):
    if created:
        UserTopicStats.objects.create(user=instance)
        UserDifficultyStats.objects.create(user=instance)


    



