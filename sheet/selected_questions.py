from .models import user,submission,question,UserDifficultyStats,UserTopicStats, sheet_question, notes, star, UserSkillTag
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
import heapq
from django.db.models import Q
from functools import reduce
import chromadb
from collections import defaultdict
import numpy as np
import os
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
        .filter(tag_filter)
        .select_related('problem')
        .order_by('-timestamp')
        .values('problem__contestId', 'problem__index', 'problem__tags','problem__rating')
        .distinct()[:20]
    )
    data = list(submissions)
    return {"tags" : weak_tags, "submissions":data}

# Worst Case
@login_required
def maxmin_tags(request):
    """If no embeddings were returned in first query, fall back to metadata filtering."""
    pass

# LOGICAL Issue TODO
# If no questions were found in vector db, it wouldn't return any embeddings


# # On the recent subms extracted
# @login_required
# def query_on_subs2(request):
#     subs = subs_weak_tags(request) # Gets latest submissions from weak tags
#     weak_tags = subs.get("tags",[]) # Weak tags list
#     sub_ids = subs.get("submissions")
#     query_ids = defaultdict(list)
#     avg_rating = defaultdict(int)

#     for sb in sub_ids:
#         contestId = sb.get('problem__contestId')
#         index = sb.get('problem__index')
#         rating = sb.get('problem__rating')
#         for tag in sb.get('problem__tags'):
#             if tag in weak_tags:
#                 query_ids[tag].append(f"{contestId}/{index}")
#                 avg_rating[tag] += rating

#     for k,v in avg_rating.items():
#         avg_rating[k] = round(avg_rating[k] // max(len(query_ids[k]),1) ,-2)# Average of those  question rating 
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     db_path = os.path.join(script_dir, "chroma_db")
    
#     client = chromadb.PersistentClient(path=db_path)
    
#     # 2. Safely load your hard-earned collection
#     collection = client.get_collection(name="db_questions_v7")
#     centroid_to_query = {}
#     testing = []
#     sample = collection.get(limit=5, include=["metadatas"])
#     for m in sample["metadatas"]:
#         testing.append(repr(m["tags"]))  # repr shows exact characters
#         testing.append(repr(k))  # repr shows exact characters

#     recommend = []
#     for k, v in centroid_to_query.items():
#         if not v:
#             continue
#         matching = collection.get(
#             where={"tags": {"$contains": f'"{k}"'}},
#             include=[]
#         )
#         n = min(15, len(matching["ids"]))
#         if n == 0:
#             continue
#         raw_matches = collection.query(
#             query_embeddings=[v],
#             n_results=n,
#             where={"tags": {"$like": f'%"{k}"%'}},
#             include=["metadatas"]
#         )
#         for metadata in raw_matches["metadatas"][0]:
#             if metadata:
#                 recommend.append(metadata)
#         # sample_tag = raw_matches['metadatas'][0][0]['tags'] if raw_matches['metadatas'][0] else "none"
#         # recommend.append({
#         #     "k": k,
#         #     "sample_tag": sample_tag,
#         #     "contains_check": f'"{k}"' in sample_tag,
#         # })

#     # # And now i query the db from those embeddings
#     # target_embeds = embeds_from_subs
#     # return JsonResponse({"data":query_ids, "data2":avg_rating, "collections": centroid_to_query, "len" : len(centroid_to_query), "from_db": recommend, "testing":sample})
#     return JsonResponse({
#         "len": len(centroid_to_query),
#         "from_db": recommend
#     })
#     # embed_debug = {}
#     # for k,v in query_ids.items():
#     #     res = collection.get(ids=v, include=["embeddings"])
#     #     embeds = res["embeddings"]
#     #     embed_debug[k] = len(embeds) if embeds is not None else 0
#     # return JsonResponse({"embed_debug": embed_debug})
    

# TASK LIST
"""
1. Migrate for solved_ids set
2. get embeddings for all those subs (tagwise) from vectordb
   make a collective embedding for one tag at a time
3. now get 15 questions which are similar to those tag, rating and not solved yet"""

@login_required
def query_on_subs(request):
    """Returns json resp of metadata of 50 vector embeddings {"title","rating","core_math_logic","index","contestId","tags"}"""
    subs = subs_weak_tags(request)
    weak_tags = subs.get("tags", [])
    sub_ids = subs.get("submissions")
    query_ids = defaultdict(list)
    avg_rating = defaultdict(int)

    for sb in sub_ids:
        contestId = sb.get('problem__contestId')
        index = sb.get('problem__index')
        rating = sb.get('problem__rating')
        for tag in sb.get('problem__tags'):
            if tag in weak_tags:
                query_ids[tag].append(f"{contestId}/{index}")
                avg_rating[tag] += rating

    for k, v in avg_rating.items(): # Avg rating - > range of questions = -100 to +200
        avg_rating[k] = round(avg_rating[k] // max(len(query_ids[k]), 1), -2)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "chroma_db")
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name="db_questions_v7")

    centroid_to_query = {} # Average vec of all embeddings from one weak tag -> now used to fetch other vec embeds 
    for k, v in query_ids.items():
        results = collection.get(ids=v, include=["embeddings"])
        embeds = results["embeddings"]
        if embeds is None or len(embeds) == 0:
            continue
        centroid = np.mean(np.array(embeds), axis=0).tolist() # point to rem -> axis = 0 (row average), axis = 1 (columns avg)
        centroid_to_query[k] = centroid

    recommend = []
    for k, v in centroid_to_query.items():
        avg = avg_rating[k]
        raw_matches = collection.query(
            query_embeddings=[v],
            n_results=50,
            # where={"tags": {"$contains": f'"{k}"'}},
            where={
                "$and": [
                    {"rating": {"$gte": avg - 100}},
                    {"rating": {"$lte": avg + 200}}
                ]
            },
            include=["metadatas"]
        )
        return JsonResponse({
            "raw_metadatas": raw_matches["metadatas"][0]
        })
    
@login_required
def saved_state_of_ques(request):
    """A Saved state of 50 selected questions, for sending all data to frontend faster"""
    data = query_on_subs(request)
    json_data = data.content.decode('utf-8') # utf-8 is decoding format (standard)
    resp = json.loads(json_data)
    data = resp.get("raw_metadatas")
    return JsonResponse({"status":"ok"})
    
    
# While the data fwd ed to prompt would be cut down significantly, maintain a separate state of those
# 50 questions so we can instantly send selected question's data to frontend.
@login_required
def prompt_data(request):
    """Strips data for prompt ["id", "tags", "rating", "core_math_logic"]"""
    data = query_on_subs(request)
    json_data = data.content.decode('utf-8') # utf-8 is decoding format (standard)
    resp = json.loads(json_data)
    data = resp.get("raw_metadatas")
    count = 1
    res = []
    for i in data:
        res.append({
            "id": count,
            "tags": i["tags"],
            "rating": i["rating"],
            "core_math_logic": i["core_math_logic"]
        })
        count += 1
    return res


@login_required
def getting_recommendations(request):
    pass
