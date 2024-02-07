from django.urls import path 
from bestow import views 

urlpatterns = [
    # User Profiles
    path('api/profile/<username>', views.ProfileViewSet.as_view(), name="profile"),

    #User Database
    path('api/user/generate', views.UserPostViewSet.as_view(), name="user-post"),

    # Filtering 
    path('api/filter/generate', views.FilterPostViewSet.as_view(), name="filter-post"),
    path('api/filter/response/<email>/', views.FilterGetViewSet.as_view(), name="filter-get"),
]
