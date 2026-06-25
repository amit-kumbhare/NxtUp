from .services import recent_submissions, all_submissions, rating_maxrating
from .models import user,submission,question,UserDifficultyStats,UserTopicStats, sheet_question, notes, star, UserSkillTag
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
from django.shortcuts import render
import heapq
from django.db.models import Q
import operator
from functools import reduce

# getting the all tags with the lowest tags (excluding those which user hasen't touched yet)

@login_required
def testing(request):
    pass
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

@login_required
def weakest_tags(request):
    """returns a list of three weakest solved tags, with their score"""
    skills= UserSkillTag.objects.get(user = request.user)
    tag_solve_count  = UserTopicStats.objects.get(user=request.user)
    skills_json = serializers.serialize('json', [skills])
    data = json.loads(skills_json)[0]["fields"]
    data.pop("user",None)
    all_tags = {k:v for k,v in data.items() }
    all_solved_tags = {}
    for k, v in all_tags.items():
        solved = getattr(tag_solve_count, k)
        if solved > 0: # Atleast one solved in that tag
            all_solved_tags[k] = v

    lowest_three = heapq.nsmallest(3, all_solved_tags.items(), key= lambda x:x[1])
    # compare this to the users solve count per tag, to ensure insolved tags aren't considered weak
    result = [k for k,v in lowest_three]
    return result

# TODO read more about this Q providing features like OR and AND in queryset

@login_required
def subs_weak_tags(request):
    """Gets me the most recent submissions of those weak tags"""
    weak_tags = weakest_tags(request)
    tag_filter = Q() 
    for tag in weak_tags:
        tag_filter |= Q(problem__tags__icontains=tag)
    
    submissions = (
        submission.objects
        .filter(solver=request.user)
        # .filter(tag_filter)
        .select_related('problem')
        .order_by('-timestamp')
        .values('problem__contestId', 'problem__index')
        .distinct()[:20]
    )
    data = list(submissions)
    return JsonResponse({"submissions":data})

# Worst Case
@login_required
def maxmin_tags(request):
    """If no embeddings were returned in first query, fall back to metadata filtering."""
    pass

# LOGICAL Issue TODO
# If no questions were found in vector db, it wouldn't return any embeddings







