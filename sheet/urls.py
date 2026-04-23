
from django.urls import path

from . import views

urlpatterns = [

    # Initialization
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("tour", views.tour, name= "tour"),

    # Problems Sheets
    path("sheet/blind_order", views.blind_order, name="blind_order"),
    path("sheet/topic_wise", views.topic_wise, name="topic_wise"),

    # Recommendations
    path("sheet/recommendations", views.recommendations, name="topic_wise"),

    # Notes
    path("sheet/notes", views.notes, name="notes"),

    #api
    path("codeforces", views.get_submissions, name="submissions"),
    path("recent", views.recent_submissions, name="recent_submissions")
    
]