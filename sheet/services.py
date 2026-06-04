import requests
from django.shortcuts import render
import datetime
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Functions which call API 

def verify_handle(handle):
    """ Used in register page to verify existance of codeforces handle. """
    url = f"https://codeforces.com/api/user.info?handles={handle}&checkHistoricHandles=true"

    try:
        res = requests.get(url)
        data = res.json()

        if data["status"] != "OK":
            return False

        user_data = data["result"][0]
        return user_data
    except Exception as e:
        return redirect("error")

# def get_user_data(request):
#     url = f"https://codeforces.com/api/user.info?handles={handle}&checkHistoricHandles=true"
#     try:
#         res = requests.get(url)
#         data = res.json()

def rating_maxrating(request):
    """Fetches Rating, Max Rating and Rank of user."""
    user_rating = {
            "MaxRating": 0,
            "Rating": 0,
            "rank":"Unranked" # Initialized to blank for unranked or unrated users.
        }
    handle = request.user.handle

    url = f"https://codeforces.com/api/user.info?handles={handle}"

    try:
        res = requests.get(url) # here its requestS
        data = res.json()

        if data["status"] != "OK":
            return user_rating
        data = data['result'][0] # result of data sends a list, get its first item
        

        # Safe API field access
        # user_rating["MaxRating"] = data["maxRating"]
        user_rating["MaxRating"] = data.get("maxRating",0)
        # user_rating["Rating"] = data["rating"]
        user_rating["Rating"] = data.get("rating",0)
        # user_rating["rank"] = data["rank"]
        user_rating["rank"] = data.get("rank","unranked")

        return user_rating
    except Exception as e:
        return user_rating


def recent_submissions(request):
    """
    Fetches the latest 200 submissions from user's profile
    OUTPUT -> Result = ["name","tags","rating","id","index","verdict","Timestamp"]
    """
    handle = request.user.handle

    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=200"

    try:
        res = requests.get(url)
        data = res.json()

        if data["status"] != "OK":
            return redirect('error')
        
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
                "verdict":i['verdict'],
                "Timestamp": datetime.datetime.fromtimestamp(i['creationTimeSeconds']).strftime('%Y-%m-%d')
            })
        
        return result
    except Exception as e:
        return -1

@login_required
def all_submissions(request):
    """
    Will run only once during account creation.
    Fetches all submissions from user's profile 
    OUTPUT -> Result = ["name","tags","rating","id","index","verdict","Timestamp"]
    """
    handle = request.user.handle

    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=10000"

    try:
        res = requests.get(url)
        data = res.json()

        if data["status"] != "OK":
            return redirect('error')
        
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
                "verdict":i['verdict'],
                "Timestamp": datetime.datetime.fromtimestamp(i['creationTimeSeconds']).strftime('%Y-%m-%d')
            })
        
        return result
    
    # Here after making the result use something like bulk create to make 
    # those obj instances for them
    except Exception as e:
        return -1




# BUILD LATER DURING PROFILE EDIT PHASE

# def update_user_data(request):

#     handle = request.GET.get("handle")
#     url = f"https://codeforces.com/api/user.info?handles={handle}"

#     try:
#         res = requests.get(url)
#         data = res.json()
#         if data["status"] != "OK":
#             return "ERROR"

#         user_data = {
#             "firstName":data["result"]["firstName"],
#             "lastName":data["result"]["lastName"],
#             "handle":data["result"]["handle"],
#             "country":f"{data["result"]["city"]}, {data["result"]["country"]}",
#             "profile_pic":data["result"]["titlePhoto"]
#         }
#         return user_data
 
#     except Exception as e:
#         return "NO JSON CONTENT WAS FETCHED"
