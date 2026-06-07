from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import requests
from django.http import JsonResponse
from .services import verify_handle, rating_maxrating
from .essentials import add_past_submissions,update_ach, user_solve_count
from django.db.models import Count,Max
import json
import datetime
import time
from .models import submission, user, sheet_question, star, notes

def index(request):
    return render(request, "sheet/login.html")

@require_POST
def login_user(request):
    data = json.loads(request.body)
    if request.method == "POST":

        email = data.get("email","").strip()
        password = data.get("password","")
        remember = data.get("remember", False)

        # authenticate() returns an user instance is it exists, none otherwise
        user_verify = authenticate(request, username = email, password = password)

        # Check if authentication successful
        if user_verify is not None:
            # Creates a session for user, which redirects and sends context
            login(request, user_verify)
            if not remember:
                request.session.set_expiry(0) # Would be logged out later
            # This is the success case -> Now login the user to blind_order
            return JsonResponse({"ok" : True, "redirect": reverse("blind_order")})
            # return render(request, "sheet/blind_order.html")
        else:
            return JsonResponse({"ok": False, "error":"Invalid Credentials"})
    else:
        return JsonResponse({"ok":False, "error": "Invalid email or password."})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# TODO -> add # message inside login page to show errors

def register(request):
    return render(request, "sheet/register.html")


@require_POST
def register_check(request):
    data = json.loads(request.body)
    if request.method == "POST":
        email = data.get('email').strip()
        exists = user.objects.filter(email = email).first()

        if not exists : # Success case for new registration
            return JsonResponse({"ok": True})
        else:
            return JsonResponse({"ok":False, "error": "Email is already registered"})
        
    else:
        # Instead we should try to raise an error here
        return JsonResponse({"ok":False})

@require_POST
def handle_check(request):
    data = json.loads(request.body)
    if request.method == "POST":
        handle = data.get("handle").strip()
        exists = verify_handle(handle)

        if not exists:
            # Failure case INVALID HANDLE
            return JsonResponse({"ok":False})
        else:
            # Success Case
            return JsonResponse({"ok":True})
    else:
        return JsonResponse({"ok":False})


@require_POST
def create_user(request):
    data = json.loads(request.body)

    # First if any existing 
    if request.method == "POST":

        fname = data.get('fname')
        lname = data.get('lname')
        email = data.get('email')
    
        password = data.get('password')
        handle = data.get('handle')

        age = data.get('age')
        country = data.get('Country')
        role = data.get('role')
        bio = data.get('bio')

        new_user = user.objects.create_user(
            handle = data.get('handle'),
            username=handle, # Abstract User class requirements
            password=password, # Automatically hashed by Django
            first_name = fname,
            last_name = lname,
            email = email,

            age = age,
            country = country,
            current_role = role,
            bio = bio
        )
        new_user.save()

        login(request,new_user)

        print(request.user.is_authenticated)
        print(request.user.username)
        print(request.session.session_key)

        return JsonResponse({"ok":True})
    else:
        return JsonResponse({"ok":False})

def forgot_password(request):
    pass # TODO

def error_occured(request):
    return render(request,"sheet/error.html")

def control(request):
    return render(request, "sheet/control.html")

@login_required
def profile(request):
    # Currently update rating when visiting the profile, later shift it to half hourly updation
    # update_ach(request)
    return render(request, "sheet/profile.html")

@login_required
def profile_data(request):
    submission_data = year_submission(request)
    user_solve_count(request)
    # profile_stats = 
    # Now add user data like solved count and tags info
    user_object = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        # "handle": getattr(request.user, 'handle', ''),
        "handle": request.user.handle,
        "country": getattr(request.user, 'country', ''),
        "age": getattr(request.user, 'age', ''),
        "current_role": getattr(request.user, 'current_role', ''),
        "bio": getattr(request.user, 'bio', ''),
        "rating":getattr(request.user,'rating',''),
        "maxrating":getattr(request.user, 'MaxRating',''),
        "solved_count":getattr(request.user,'solved_count',''),
        "rank":getattr(request.user, 'rank','')
    }

    # Graph data
    diff = request.user.difficulty # Fetches UserDifficultyStats
    pie_data = {
        "easy" : diff.easy,
        "medium" : diff.medium,
        "hard" : diff.hard
    }
    topics = request.user.topic_wise # Fetches UserTopicStats
    topic = {
        "graphs" : topics.graphs,
        "dp" : topics.dp,
        "greedy" : topics.greedy,
        "binary_search" : topics.binary_search,
        "data_structures" : topics.data_structures,
        "math" : topics.math,
        "strings" : topics.strings,
        "dfs" : topics.dfs,
        "shortest_paths" : topics.shortest_paths,
        "trees" : topics.trees,
        "two_pointer" : topics.two_pointer,
        "sliding_window" : topics.sliding_window,
        "implementation" : topics.implementation,
        "dsu" : topics.dsu,
        "bitmasks" : topics.bitmasks
    }


    return JsonResponse({"user": user_object, "data": submission_data, "pie":pie_data, "graph":topic})



@login_required
def year_submission(request):
    """Gets all submission from a user within the past 364 Days."""
    user_data = request.user
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()

    all_submissions = submission.objects.filter(solver__handle = user_data.handle, timestamp__range =[start_date,end_date], verdict="OK" )
    submission_data = all_submissions.values('timestamp').annotate(count=Count('id'), rating= Max('problem__rating'))

    # Now converting dates to strings because JSON can't serialise date in Django (basically trying to make them strings to send places)
    formatted_data = []
    for item in submission_data:
        formatted_data.append({
            "timestamp": item['timestamp'].strftime('%Y-%m-%d'),
            "count" : item['count'],
            "rating": item['rating']
        })
    return formatted_data

@login_required
def graph_data(request):
    """Updates user's statistics data for the first time (on all 10k submissions)"""
    # subs = submission.objects.filter(solver__handle = request.user.handle,verdict="OK").distinct("problem__problem_id")
    subs = (
        submission.objects.filter(solver__handle=request.user.handle, verdict="OK")
        .select_related('problem') # Fetches entire problem table, reducing 10k query to 1
        .order_by('problem__problem_id') # SQL ORDER BY
    )

    # Now look for duplicates 
    seen_problem_ids = set()

    new_subs = []

    for sub in subs:
        if sub.problem.problem_id not in seen_problem_ids:
            seen_problem_ids.add(sub.problem.problem_id)
            new_subs.append(sub)
    solved = {"easy":0, "medium":0, "hard":0}

    tag = {"graphs":0, 
                  "dp": 0,
                  "greedy":0,
                  "binary_search":0,
                  "data_structures":0,
                  "math":0,
                  "strings":0,
                  "dfs":0,
                  "shortest_paths":0,
                  "trees":0,
                  "two_pointer":0,
                  "sliding_window":0,
                  "implementation":0,
                  "dsu":0,
                  "bitmasks":0
                  }
    
    for sub in subs:
        # Now get sub's rating 
        if sub.problem.rating <= 1200:
            solved["easy"] += 1
        elif sub.problem.rating <= 1900:
            solved["medium"] += 1
        else:
            solved["hard"] += 1
        
        for i in sub.problem.tags:
            if i in tag:
                tag[i] += 1
    
    # Now update the new data with user stats

    diff = request.user.difficulty # Object of UserDifficultyStats
    diff.easy = solved["easy"]
    diff.medium = solved["medium"]
    diff.hard = solved["hard"]

    diff.save()

    topics = request.user.topic_wise # Object of UserTopicStats
    topics.graphs = tag["graphs"]
    topics.dp = tag["dp"]
    topics.greedy = tag["greedy"]
    topics.binary_search = tag["binary_search"]
    topics.data_structures = tag["data_structures"]
    topics.math = tag["math"]
    topics.strings = tag["strings"]
    topics.dfs = tag["dfs"]
    topics.shortest_paths = tag["shortest_paths"]
    topics.trees = tag["trees"]
    topics.two_pointer = tag["two_pointer"]
    topics.sliding_window = tag["sliding_window"]
    topics.implementation = tag["implementation"]
    topics.dsu = tag["dsu"]
    topics.bitmasks = tag["bitmasks"]
    
    topics.save()

    request.user.save()

    return redirect("profile")



def profile_edit(request):
    return render(request, "sheet/profile_edit.html")

# correct codeforces URL -> https://codeforces.com/problemset/problem/4/A
# TODO -> Also add activated section context when updating frontend

# ONE TIME ONLY TOUR OF NXTUP
def tour(request):
    return render(request, "sheet/tour.html")

# def user_data(request):
#     json_data = get_user_data(request)
#     return render(request, "sheet/codeforcesapi.html",{
#         "userdata":json_data
#     })

        



####################################################################################
# BLIND ORDER
####################################################################################

@login_required # This decorator only allows blind_order to run if loggedin
def questions_data(request):
    user_handle = request.user.handle

    # Firstly fetch sheet_problems
    sheet_problems = list(sheet_question.objects.values())
    # This is list of all problem_ids
    problem_id = [f"{p["contestId"]}{p["index"]}" for p in sheet_problems]

    # Fetch all star from users 
    star_problems = star.objects.filter(
        user = request.user
        ).values_list(
            "problem__problem_id",flat=True)
    # Make a list of all problem id having a star from user
    star_list = [str(p) for p in star_problems]

    # Fetch all user notes
    notes_list = dict(notes.objects.filter(
        user = request.user
    ).values_list("problem__problem_id","text"))
    
    solved_ids = list(
        submission.objects.filter(
            solver__handle = user_handle,
            problem__problem_id__in = problem_id,
            verdict = "OK"
        )
        .values_list('problem__problem_id', flat=True)
        .distinct()
    )
    return JsonResponse({"problems": sheet_problems, "solved_problem_list": solved_ids, "starred": star_list, "notes": notes_list}, json_dumps_params={"default": str})


@login_required
def blind_order(request):
    return render(request, "sheet/blind_order.html")
####################################################################################
# TOPIC WISE
####################################################################################

# TODO Implement a rating sort on your own.
# bars on every page

@login_required
def topic_wise(request):
    with open('sheet/sheet_problems/a2oj_problems.json') as f:
        data = json.load(f)
    return render(request, "sheet/topic_wise.html",{
        'problems_json': json.dumps(data)
    })

@login_required
def user_notes(request):
    pass

@login_required
def user_stars(request):
    pass


####################################################################################
# RECOMMENDATIONS
####################################################################################

# Context for recommendations
'''
No. of submissions analysed 
last synced hours


Success per tag -> currently hard coded : 
skill-pct strong = Green 
skill-pct mid = yellow
skill-pct weak = red
'''
from collections import defaultdict

'''
Submission Fetched JSON Example
{
"name" : "Fair Coin",
"tags" : ["Implementation", "constructive Algorithm"],
"rating" : 1400,
"id" : 658,
"index" : A,
"verdict" : OK
}
'''


def recent_submissions(request):
    pass


tags = ["implementation", "math", "brute-force","greedy","binary-search",
        "two-pointer", "dp","dfs/bfs","dsu", "number-theory","segment-trees",
        "dp-on-trees","shortest-paths"]


@login_required
def topic_analysis(request):
    """Generates an accuracy percentage table, showing strong
       weak topics of the user.
       Formula => (ACs/total_submission) per topic"""
    data = recent_submissions(request)
    topic_stats = defaultdict(lambda : {"total":0 ,"OK":0})

    for prob in data:
        tags = prob["tags"]
        for tag in tags:
            topic_stats[tag]["total"] += 1 # This counts every submission
            if prob["verdict"] == "OK":
                topic_stats[tag]["OK"] += 1 # No. of ACs
    result = []
    for tag, stats in topic_stats.items():
        accuracy = int((stats["OK"]/stats["total"]) * 100)
        result.append({
            "Tag":tag,
            "Submissions":stats["total"],
            "Accuracy" : accuracy
        })
    result.sort(key = lambda x : x["Accuracy"])
    return result

def weak_topic_analysis(request):
    pass

def recommendations(request):
    tags_accuracy = topic_analysis(request)
    return render(request, "sheet/recommendations.html",{
        "no_of_submissions_analysed" : 200,
        "last_synced": 2,
        "tags_accuracy" : tags_accuracy
    })

####################################################################################
# TESTING AREA

def print_date(request):
    data = recent_submissions(request)
    return render(request, "sheet/codeforcesapi.html",{
        "submissions":data
    })

####################################################################################











