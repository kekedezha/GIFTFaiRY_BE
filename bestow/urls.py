from django.urls import path 
from bestow import views 

urlpatterns = [
    # User Profiles
    path('api/profile/<username>', views.ProfileViewSet.as_view(), name="profile"),

    # Filtering 
    path('api/filter/generate', views.FilterPostViewSet.as_view(), name="filter-post"),
    path('api/filter/response/', views.FilterGetViewSet.as_view()),
]