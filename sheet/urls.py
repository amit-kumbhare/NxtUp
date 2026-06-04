from django.urls import path
from . import views
from . import services
from . import essentials

urlpatterns = [

    # CONTROL PANEL
    path("control", views.control, name="control"),

    # Initialization
    path("", views.index, name="index"),
    # Alt path
    # path("accounts/login/", views.index, name="login"),
    path("login/",views.index, name="login"),
    # path("login", views.login, name="login"),
    path("login/api/", views.login_user, name = "check_login"),
    path("register", views.register, name="register"),
    path("user/register", views.register_check, name="register_user"),
    path('create/user', views.create_user, name="create_user"),
    path("verify", views.handle_check, name="handle_check"),
    path("logout", views.logout_user, name="logout"),
    path("tour", views.tour, name= "tour"),
    path('profile', views.profile, name="profile"),
    path('user_profile_data', views.profile_data, name='profile_data'),
    path("profile_edit", views.profile_edit, name= "profile_edit"),

    # Blindorder and Topic Wise Sheets  Questions

    # NOTE => Try to add those questions in session storage for smoother experience
    path("fetch_sheet_questions", views.questions_data, name="fetch_sheet_questions"),

    # Problems Sheets
    path("sheet/blind_order", views.blind_order, name="blind_order"),
    path("sheet/topic_wise", views.topic_wise, name="topic_wise"),

    # Recommendations
    path("sheet/recommendations", views.recommendations, name="recommendations"),

    # Notes
    path("sheet/notes", views.notes, name="notes"),

    #api
    path("add_past_submissions", essentials.add_past_submissions, name="add_past_submissions"),
    path("recent_submissions", services.recent_submissions, name="recent_submissions"),
    path("get_rating", essentials.update_ach, name="get_rating"),

    # DB
    path("calc_stats", essentials.create_user_ach, name="calc_stats"),
    path("update_data", views.graph_data, name="update_data"),
    path("create_questions", essentials.create_questions, name="create_questions"),

    # Control Panel 
    # Fetch Submission of a user
    path("error",views.error_occured, name="error")
    
]