from django.contrib import admin

# Register your models here.
from .models import user, notes, question, submission, UserDifficultyStats, UserTopicStats, sheet_question

admin.site.register(user)
admin.site.register(notes)
admin.site.register(question)
admin.site.register(sheet_question)
admin.site.register(submission)
admin.site.register(UserTopicStats)
admin.site.register(UserDifficultyStats)
