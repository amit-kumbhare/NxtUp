from .services import recent_submissions, all_submissions, rating_maxrating
from .models import user,submission,question,UserDifficultyStats,UserTopicStats, sheet_question, notes, star, UserSkillTag
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import F
from .skill_map import skill_map

# CHECK IF NEW SUBMISSIONS WERE MADE
@login_required
def checking_new_submissions(request):
    """Checks if a new submissions by user was added to DB."""
    check = submission.objects.get()
    return True

#--------------------------------------------------------------------------------------

@login_required
def update_ach(request):
    """Updates user acheivements like rating (max also), and his rank"""
    ach = rating_maxrating(request)
    if not ach: # Now redirect to error page
        return redirect("error")
    # Now update the user instance
    request.user.rating = ach["Rating"]
    request.user.MaxRating = ach["MaxRating"]
    request.user.rank = ach["rank"]
    request.user.save()
    return JsonResponse({"ok": True})

@login_required
def user_solve_count(request):
    """Returns the number of questions solved by the user"""
    num = submission.objects.filter(solver = request.user, verdict="OK").values_list('problem__problem_id', flat=True)
    request.user.solved_count = len(set(num))
    # Now save the current updates in the request.user
    request.user.save()
    return True

@login_required
def add_past_submissions(request):
    """
    Creates submission object, showing questions solved by user."""
    new_data = all_submissions(request)
    # here Reverse to process oldest submission first
    new_data = list(reversed(new_data))

    for i in new_data:

        # Now update the count of question rating and tags for user

        # Get or create the question
        prob, _ = question.objects.get_or_create(
            problem_id=f"{i['id']}{i['index']}",
            defaults={
                'title': i["name"],
                'rating': i["rating"],
                'tags': i["tags"]
            }
        )

        # Check if submission already exists
        existing_sub = submission.objects.filter(
            solver=request.user,
            problem=prob
        ).first()

        if existing_sub:
            # If existing submission is NOT OK and current is OK, update it!
            if existing_sub.verdict != "OK" and i["verdict"] == "OK":
                existing_sub.verdict = "OK"
                existing_sub.timestamp = i["Timestamp"]
                existing_sub.save()
        else:
            # If no submission exists, create new one
            submission.objects.create(
                solver=request.user,
                problem=prob,
                verdict=i["verdict"],
                timestamp=i["Timestamp"]
            )


    return JsonResponse({"ok": True})

@login_required
def add_recent_submissions(request):
    """
    Creates submission object, showing questions solved by user."""
    new_data = recent_submissions(request)
    # abb Reverse to process oldest submission first
    # First wrong subs, then right subs -> Correct Subs are counted for only once (in solved list)
    new_data = list(reversed(new_data))
    # Here i skill_map.skill_map to get those recent submissions analysed and shown in recommendations
    skill_map(new_data)

    for i in new_data:
        # Get or create the question
        prob, _ = question.objects.get_or_create(
            problem_id=f"{i['id']}{i['index']}",
            defaults={
                'title': i["name"],
                'rating': i["rating"],
                'tags': i["tags"]
            }
        )

        # Check if submission already exists
        existing_sub = submission.objects.filter(
            solver=request.user,
            problem=prob
        ).first()

        if existing_sub:
            # If existing submission is NOT OK and current is OK, update it!
            if existing_sub.verdict != "OK" and i["verdict"] == "OK":
                existing_sub.verdict = "OK"
                existing_sub.timestamp = i["Timestamp"]
                existing_sub.save()
        else:
            # If no submission exists, create new one
            submission.objects.create(
                solver=request.user,
                problem=prob,
                verdict=i["verdict"],
                timestamp=i["Timestamp"]
            )
    return JsonResponse({"ok": True})

@login_required
def create_user_ach(request):
    """Gets all submission data and creates fresh user statistics"""
    # Get all OK submissions with full problem data
    all_subs = (
        submission.objects.filter(solver__handle=request.user.handle, verdict="OK")
        .select_related('problem')
        .order_by('problem__problem_id')
    )

    # Deduplicate submissions (only keep first OK per problem)
    seen_problem_ids = set()
    unique_subs = []
    for sub in all_subs:
        if sub.problem.problem_id not in seen_problem_ids:
            seen_problem_ids.add(sub.problem.problem_id)
            unique_subs.append(sub)

    # Initialize counters
    solved = {"easy": 0, "medium": 0, "hard": 0}

    # NEEDS REVIEW TODO
    tag_mapping = {
        "graph theory": "graphs",
        "dynamic programming": "dp",
        "greedy": "greedy",
        "binary search": "binary_search",
        "data structures": "data_structures",
        "math": "math",
        "strings": "strings",
        "dfs and similar": "dfs",
        "shortest paths": "shortest_paths",
        "trees": "trees",
        "two pointers": "two_pointer",
        "sliding window": "sliding_window",
        "implementation": "implementation",
        "dsu": "dsu",
        "bitmasks": "bitmasks"
    }

    tag = {field: 0 for field in tag_mapping.values()}

    # Calculate stats
    for sub in unique_subs:
        # Difficulty count
        if sub.problem.rating <= 1200:
            solved["easy"] += 1
        elif sub.problem.rating <= 1900:
            solved["medium"] += 1
        else:
            solved["hard"] += 1

        # Topic count
        for problem_tag in sub.problem.tags:
            normalized_tag = problem_tag.lower()
            if normalized_tag in tag_mapping:
                model_field = tag_mapping[normalized_tag]
                tag[model_field] += 1

    # Update UserDifficultyStats obj
    diff, _ = UserDifficultyStats.objects.get_or_create(user=request.user)
    diff.easy = solved["easy"]
    diff.medium = solved["medium"]
    diff.hard = solved["hard"]
    diff.save()

    # Update UserTopicStats obj
    topics, _ = UserTopicStats.objects.get_or_create(user=request.user)
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

    # Update user's solved_count
    request.user.solved_count = len(unique_subs)
    request.user.save()

    return JsonResponse({"status": "ok", "solved_count": len(unique_subs)})
                
    

# Update user ach
@login_required
def update_user_ach(request):
    """Updates them with the latest submission data fetched (ones from recent_submissions)"""
    subs = (
        submission.objects.filter(solver__handle=request.user.handle, verdict="OK")
        .select_related('problem')
        .order_by('problem__problem_id')
        .values('problem__problem_id')             
    )

    seen_problem_ids = set()
    subs = []
    for sub in all_subs:
        if sub.problem.problem_id not in seen_problem_ids:
            seen_problem_ids.add(sub.problem.problem_id)
            subs.append(sub)


    # Fetch full objects after dedup
    unique_problem_ids = [s['problem__problem_id'] for s in subs]
    all_subs = submission.objects.filter(
        solver__handle=request.user.handle,
        verdict="OK",
        problem__problem_id__in=unique_problem_ids
    ).select_related('problem')

    seen_problem_ids = set()
    subs = []
    for sub in all_subs:
        if sub.problem.problem_id not in seen_problem_ids:
            seen_problem_ids.add(sub.problem.problem_id)
            subs.append(sub)


    solved = {"easy": 0, "medium": 0, "hard": 0}
    tag = {
        "graphs": 0, "dp": 0, "greedy": 0,
        "binary search": 0, "data structures": 0,
        "math": 0, "strings": 0, "dfs and similar": 0,
        "shortest paths": 0, "trees": 0, "two pointer": 0,
        "sliding window": 0, "implementation": 0,
        "dsu": 0, "bitmasks": 0
    }

    for sub in subs:
        if sub.problem.rating < 1200:
            solved["easy"] += 1
        elif sub.problem.rating < 1900:
            solved["medium"] += 1
        else:
            solved["hard"] += 1

        for i in sub.problem.tags:
            if i in tag:
                tag[i] += 1

    # Update UserDifficultyStats
    diff = request.user.difficulty
    diff.easy   = solved["easy"]
    diff.medium = solved["medium"]
    diff.hard   = solved["hard"]
    diff.save()

    # Update UserTopicStats
    topics = request.user.topic_wise
    topics.graphs          = tag["graphs"]
    topics.dp              = tag["dp"]
    topics.greedy          = tag["greedy"]
    topics.binary_search   = tag["binary search"]
    topics.data_structures = tag["data structures"]
    topics.math            = tag["math"]
    topics.strings         = tag["strings"]
    topics.dfs             = tag["dfs and similar"]
    topics.shortest_paths  = tag["shortest paths"]
    topics.trees           = tag["trees"]
    topics.two_pointer     = tag["two pointer"]
    topics.sliding_window  = tag["sliding window"]
    topics.implementation  = tag["implementation"]
    topics.dsu             = tag["dsu"]
    topics.bitmasks        = tag["bitmasks"]
    topics.save()

    request.user.save()
    return JsonResponse({"status": "ok"})


def update_user_data(request):
    """
    Creates submission object, showing questions solved by user."""
    new_data = recent_submissions(request) 
    for i in new_data:
        sub = submission(
            solver = request.get("user"),
            problem = question.objects.get_or_create(
                problem_id = f"{i['id']}{i['index']}",
                defaults={
                    'problem_id' : f"{i['id']}{i['index']}",
                    'title' : i["name"],
                    'rating' : i["rating"],
                    'tags' : i["tags"]
                    
                })[0],
            verdict = i["verdict"],
            timestamp = i["Timestamp"]
        )
        sub.save()
    return "Synced !"

def update_user_field(request):
    pass

def create_questions(request):
    """
    For creating question instances from json data
    """
    with open(f'sheet/sheet_problems/a2oj_problems.json') as f:
        data = json.load(f) # Loads all json question data
    new_ques = []
    for i in data:
        new_ques = sheet_question(
            contestId = i["contestId"],
            index = i["index"],
            problem_id = f"{i["contestId"]}{i["index"]}",
            title = i["title"],
            rating = i["rating"],
            tags = i["tags"]
        )
        new_ques.save()
    return redirect("profile")

def create_questions_2(request):
    """
    For creating question instances from json data
    """
    with open(f'sheet/sheet_problems/a2oj_problems.json') as f:
        data = json.load(f) # Loads all json question data
    new_ques = []
    for i in data:
        new_ques = question(
            contestId = i["contestId"],
            index = i["index"],
            problem_id = f"{i["contestId"]}{i["index"]}",
            title = i["title"],
            rating = i["rating"],
            tags = i["tags"]
        )
        new_ques.save()
    return redirect("profile")

def update_user_statistics(request):
    # Here add data to user stats
    pass
    
@login_required
def create_note(request):
    """Creates an obj of notes from user (on sheet_problems), takes in user, note and problem_id"""
    data = json.loads(request.body)
    if request.method == "POST":
        # content = request # HERE GET THE CONTENT
        problem_instance = sheet_question.objects.get(problem_id = data.get("id"))
        new_note, created = notes.objects.update_or_create(
            user = request.user,
            problem = problem_instance, # This should be an instance of the object of sheet_problem
            defaults= {"text": data.get("note")}
        )
        return JsonResponse({"status": "ok", "update":not created})

    return JsonResponse({"status": "fail"})

        
@login_required
def create_star(request):
    """Creates obj of star from user (on sheet_problems), takes in user and problem_id"""
    data = json.loads(request.body)
    if request.method == "POST":
        # content = request # HERE GET THE CONTENT
        problem_instance = sheet_question.objects.get(problem_id = data.get("id"))
        new_star = star.objects.get_or_create(
            user = request.user,
            problem = problem_instance
        )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "fail"})
        




