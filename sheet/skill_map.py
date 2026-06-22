from .services import recent_submissions, all_submissions, rating_maxrating
from .models import user,submission,question,UserDifficultyStats,UserTopicStats, sheet_question, notes, star, UserSkillTag
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
from django.shortcuts import render

@login_required
def testing(request):
    prob_list = recent_submissions(request)
    skill_map(prob_list)
    skills, _ = UserSkillTag.objects.get()
    skills_json = serializers.serialize('json', skills)
    return render(request, "sheet/temp.html",{
        "submissions" : skills_json
    })


# CHECK IF NEW SUBMISSIONS WERE MADE
@login_required
def checking_new_submissions(request):
    """Checks if a new submissions by user was added to DB."""
    check = submission.objects.get()
    return True

# USER SKILL MAP 
@login_required
def delta(request, rating, skill, outcome):
    """[RUN ONLY][Not for incr] Calculates and updates delta for tag skill (GIVEN) for every submission"""
    octs = {
        "AC" : 1,
        "WA" : -0.5,
        "TLE": -0.25
    }
    topics, _ = UserSkillTag.objects.get_or_create(user=request.user)
    val =  octs[outcome] * (1 + (rating - topics[skill])/100)
    setattr(UserTopicStats, skill, val)
    return {"status":"ok"}


# OUTPUT -> New_data Entries = ["name","tags","rating","id","index","verdict","Timestamp"]
@login_required
def skill_map(request, new_data):
    """calculates a rating point for every tag. Updates with every recent_submissions API Call"""
    recent_problems = new_data
    for subs in recent_problems:
        all_tags = subs[1]
        verdict = subs[5]
        if verdict == "OK": verdict = "AC"
        elif verdict in ["TIME_LIMIT_EXCEEDED","MEMORY_LIMIT_EXCEEDED"]: verdict = "TLE"
        else: verdict = "WA"
        for tag in all_tags:
            delta(subs[2], tag, verdict)
    return {"status":"ok"}


# penalty_factor = max(-200, (problem_rating - current_user_tag_skill))