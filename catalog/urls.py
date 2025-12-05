from django.urls import path
from . import views
from catalog import views
from catalog.views import AnimeCreateView, AnimeSelectionView, add_character, add_role_to_crewmember, add_crew_to_anime, add_character
# used to distiguish app url paths from each other

urlpatterns = [
    path('', views.index, name='index'),
    path('anime_list/', views.AnimeListView.as_view(), name='anime_list'),
    # crew-list needs to be crew_list for consistency
    path('crew/', views.CrewMemberListView.as_view(), name='crew-list'),
    path('crewmember/<int:pk>/', views.CrewMemberDetailView.as_view(), name='crew_member_detail'),
    path("search/", views.search, name="search"),
    path('anime_detail/<int:pk>/', views.AnimeDetailView.as_view(), name='anime_detail'),
    path('rating_form/<int:pk>/', views.add_rating, name="add_rating"),
    path('anime/create/', views.AnimeCreateView.as_view(), name='anime_create'),
    path('anime_selection_list/', views.AnimeSelectionView.as_view(), name='anime_selection_list'),
    path('anime/<int:anime_id>/add-crew/', views.add_crew_to_anime, name='add_crew_to_anime'),
    path('anime/<int:anime_id>/crewmember/<int:crew_member_id>/add-role/', views.add_role_to_crewmember, name='add_role_to_crewmember'),
    path('anime/<int:anime_id>/crewmember/<int:crew_member_id>/add-character/', views.add_character, name='add_character'),
    path('anime/<int:anime_id>/anime_crew_list/', views.anime_crew_list, name='anime_crew_list'),
    path('diary/', views.diary, name='diary'),
    path('set-timezone/', views.set_user_timezone, name='set-timezone'),
    path('user_profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('edit_profile/<str:username>/', views.edit_profile, name='edit_profile'),
]