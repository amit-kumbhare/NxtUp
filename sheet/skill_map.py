from .services import recent_submissions, all_submissions, rating_maxrating
from .models import user,submission,question,UserDifficultyStats,UserTopicStats, sheet_question, notes, star, UserSkillTag
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
from django.shortcuts import render
"""
{"ok": true, "data": "[{\"model\": \"sheet.userskilltag\", \"pk\": 9, \"fields\": {\"user\": 6, \"dp\": 803, \"graphs\": 800, \"greedy\": 800, \"binary_search\": 800, \"data_structures\": 800, \"math\": 787, \"strings\": 803, \"dfs\": 800, \"shortest_paths\": 800, \"trees\": 813, \"two_pointer\": 800, \"sliding_window\": 800, \"implementation\": 800, \"dsu\": 795}}]\n"}"""
# Run by 
@login_required
def get_user_skillmap(request):
    """Activated via recent_submissions CRON Job, it gets me user skillmap updated on the last"""
    # prob_list = new_data
    # skill_map(request, prob_list)
    skills = UserSkillTag.objects.get(user = request.user)
    skills_json = serializers.serialize('json', [skills])
    return JsonResponse({"data":skills_json})

@login_required
def testing(request):
    # return JsonResponse({"CODE TESTING ZONE"})
    skills = UserSkillTag.objects.get(user = request.user)
    skills_json = serializers.serialize('json', [skills])
    return JsonResponse({"ok": True, "data":skills_json})


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
    TAG_MAP = {
        "two pointers":   "two_pointer",
        "binary search":  "binary_search",
        "data structures":"data_structures",
        "shortest paths": "shortest_paths",
        "sliding window": "sliding_window",
        "dfs and similar":"dfs",
        "graphs":         "graphs",
        "dp":             "dp",
        "greedy":         "greedy",
        "math":           "math",
        "strings":        "strings",
        "trees":          "trees",
        "dsu":            "dsu",
        "bitmasks":       "bitmasks",
        "implementation": "implementation",
    }
    octs = { # Octs for outcomes
        "AC" : 1,
        "WA" : -0.5,
        "TLE": -0.25
    }
    topics, created = UserSkillTag.objects.get_or_create(user = request.user)
    tag_name = TAG_MAP.get(skill)
    if tag_name is None:
        return
    curr_skill = getattr(topics, tag_name, 800)
    val =  octs[outcome] * (1 + (rating - curr_skill)/100)
    new_val = curr_skill + val
    setattr(topics, tag_name, new_val)
    topics.save()



# OUTPUT -> New_data Entries = {"name","tags","rating","id","index","verdict","Timestamp"}
@login_required
def skill_map(request, new_data):
    """calculates a rating point for every tag. Updates with every recent_submissions API Call"""
    recent_problems = new_data
    for subs in recent_problems:
        all_tags = subs["tags"]
        verdict = subs["verdict"]
        if verdict == "OK": verdict = "AC"
        elif verdict in ["TIME_LIMIT_EXCEEDED","MEMORY_LIMIT_EXCEEDED"]: verdict = "TLE"
        else: verdict = "WA"
        for tag in all_tags:
            delta(request,subs["rating"], tag, verdict)
    return {"status":"ok"}


# penalty_factor = max(-200, (problem_rating - current_user_tag_skill))