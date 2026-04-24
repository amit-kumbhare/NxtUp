from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import requests
from django.http import JsonResponse
import json



# Create your views here.

def index(request):
    return render(request, "sheet/login.html")

def login(request):
    pass

def logout(request):
    pass

def profile(request):
    return render(request, "sheet/profile.html")

# correct codeforces URL -> https://codeforces.com/problemset/problem/4/A
# TODO -> Also add activated section context when updating frontend

# ONE TIME ONLY TOUR OF NXTUP
def tour(request):
    return render(request, "sheet/tour.html")


####################################################################################
# BLIND ORDER
####################################################################################


def blind_order(request):
    with open('sheet/sheet_problems/1300.json') as f:
        data = json.load(f)
    return render(request, "sheet/blind_order.html",{
        'problems_json': json.dumps(data)
    })

####################################################################################

# TODO Implement a rating sort on your own.
# TODO Also update new topic_wise.html file name in navigation
# bars on every page
def topic_wise(request):
    return render(request, "sheet/topic_wise.html")

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
    handle = request.GET.get("handle", "amit.k_52")

    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=200"

    try:
        res = requests.get(url)
        data = res.json()

        if data["status"] != "OK":
            return -1
        
        submissions = data["result"]
        result = []
        for i in submissions:
            result.append({
                "name":i['problem']['name'],
                "tags":i['problem']['tags'],
                # Special check for unrated gym problems
                "rating":i['problem'].get('rating',0),
                "id": i["problem"]["contestId"],
                "index": i["problem"]["index"],
                "verdict":i['verdict']
            })

        return result
    except Exception as e:
        return -1

tags = ["implementation", "math", "brute-force","greedy","binary-search",
        "two-pointer", "dp","dfs/bfs","dsu", "number-theory","segment-trees",
        "dp-on-trees","shortest-paths"]



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

def notes(request):
    return render(request, "sheet/notes.html")

def fetching(request):
    handle = "amit.k_52"



def get_submissions(request):
    handle = request.GET.get("handle", "amit.k_52")

    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000"

    try:
        res = requests.get(url)
        data = res.json()

        if data["status"] != "OK":
            return JsonResponse({"error": "Invalid handle"}, status=400)
        
        submissions = data["result"]

        # Optional: simplify response
        result = [
            {
                "name": sub["problem"]["name"],
                "verdict": sub.get("verdict", "UNKNOWN")
            }
            for sub in submissions
        ]
        return render(request, "sheet/codeforcesapi.html",{
            "content":result
        })

        # return JsonResponse({"submissions": result})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





