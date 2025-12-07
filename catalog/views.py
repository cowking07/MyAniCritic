from django.views import generic
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone as django_timezone
from .models import Genre, CrewMember, Anime, Rating, TrendingNews, CrewRole, Character, UserProfile
from .forms import AnimeForm, CharacterForm, CrewRoleForm, CrewMemberForm, UserProfileForm, UserForm
from catalog.forms import RatingForm
import json

@csrf_exempt
def set_user_timezone(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tzname = data.get("timezone")
            if tzname:
                # This activates the timezone for the current session/user context
                django_timezone.activate(tzname)
                # This also stores it in the session for subsequent requests
                request.session['django_timezone'] = tzname
                return JsonResponse({'status': 'ok', 'timezone': tzname})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid request'}, status=405)

def search(request):
    query = (request.GET.get("q") or "").strip()
    anime_results = Anime.objects.none()
    crew_results = CrewMember.objects.none()
    if query:
        # --- Anime search ---
        anime_results = (
            Anime.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(production_studio__icontains=query) |
                Q(genre__name__icontains=query)       # ManyToMany to Genre(name)
            )
            .distinct()
            .order_by("title")
        )
        # --- Crew search ---
        crew_results = (
            CrewMember.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(crew_roles__role__icontains=query) |        # from CrewRole.role
                Q(crew_roles__anime__title__icontains=query) | # anime they worked on
                Q(characters__character_name__icontains=query) # characters voiced
            )
            .distinct()
            .order_by("last_name", "first_name")
        )

    return render(
        request,
        "catalog/search_results.html",
        {
            "query": query,
            "anime_results": anime_results,
            "crew_results": crew_results,
            "total": anime_results.count() + crew_results.count() if query else 0,
        }
    )

def index(request):
    news = TrendingNews.objects.all()
    anime = Anime.objects.all()
    existing_anime = []
    for article in news:
        for ani in anime:
            if ani.title == article.anime_title:
                existing_anime.append(article.anime_title)

    context = {
        'news': news,
        'anime': anime,
        'existing_anime': existing_anime,
    }
    return render(request, 'catalog/index.html', context)
# login view shouldn't restrict viewing anime reviews


class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'catalog/anime_detail.html'
    context_object_name = 'anime'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = self.object.ratings.all()
        
        return context

class AnimeListView(ListView):
    model = Anime

    # return render(request, 'catalog/anime_list.html', context)

class CrewMemberDetailView(DetailView):
    model = CrewMember
    template_name = 'catalog/crew_member_detail.html'
    context_object_name = 'crew_member'
    # Now the template can say {{ crew_member.name }}, etc.

class CrewMemberListView(ListView):
    model = CrewMember
    template_name = 'catalog/crew-member_list.html'
    context_object_name = 'crew_list'

@login_required
def diary(request):
    user_ratings =Rating.objects.filter(user=request.user).order_by('-id')
    return render(request, 'catalog/diary.html', {'ratings': user_ratings})

# Rating view
# because classed based we use LoginRequiredMixin

@login_required
def add_rating(request, pk):
  if request.user.is_authenticated:
    anime = Anime.objects.get(id=pk)
    user = request.user
    try:
      rating_instance = Rating.objects.get(user=user, anime=anime)
    except Rating.DoesNotExist:
      rating_instance = None
    if request.method == "POST":
      form = RatingForm(request.POST, instance=rating_instance)
      if form.is_valid():
        data = form.save(commit=False)
        data.comment = request.POST["comment"]
        data.rating = request.POST["rating"]
        data.user = request.user
        data.anime = anime
        data.save()
        return redirect("/anime_list/")
    else:
      form = RatingForm(instance=rating_instance)
    context = {"form": form,
               'anime': anime,
               'title': 'Edit Rating' if rating_instance else 'Create Rating'}
    return render(request, 'catalog/rating_form.html', context)
  else:
    return redirect("register:register")
@login_required
def edit_rating(request, pk):
  if request.user.is_authenticated:
    anime = Anime.objects.get(id=pk)
    user = request.user
    try:
      rating_instance = Rating.objects.get(user=user, anime=anime)
    except Rating.DoesNotExist:
      rating_instance = None
    if request.method == "POST":
      form = RatingForm(request.POST, instance=rating_instance)
      if form.is_valid():
        data = form.save(commit=False)
        data.comment = request.POST["comment"]
        data.rating = request.POST["rating"]
        data.user = request.user
        data.anime = anime
        data.save()
        return redirect("/anime_list/")
    else:
      form = RatingForm(instance=rating_instance)
    context = {"form": form,
               'anime': anime,
               'title': 'Edit Rating' if rating_instance else 'Create Rating'}
    return render(request, 'catalog/rating_form.html', context)
  else:
    return redirect("register:register")




"""def edit_review(request, movie_id, review_id):
  if request.user.is_authenticated:
    movie = Movie.objects.get(id=movie_id)
    # review
    review = Review.objects.get(movie=movie, id=review_id)

    # check if the review was done by the logged in user
    if request.user == review.user:
      # grant permission
      if request.method == "POST" or "GET":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
          data = form.save(commit=False)
          if (data.rating > 10) or (data.rating < 0):
            error = "Out of range. Please select rating from 0 to 10."
            return render(request, 'main/editreview.html', {"error": error, "form": form})
          else:

            data.save()
            return redirect("main:detail", movie_id)
        else:
          form = ReviewForm(instance=review)
        return render(request, 'main/editreview.html', {"form": form})
      else:
        return redirect("main:detail", movie_id)
    else:
      return redirect("accounts:login")


# Delete review:
def delete_review(request, movie_id, review_id):
  if request.user.is_authenticated:
    movie = Movie.objects.get(id=movie_id)
    # review
    review = Review.objects.get(movie=movie, id=review_id)

    # check if the review was done by the logged in user
    if request.user == review.user:
      # grant permission to delete
      review.delete()

    return redirect("main:detail", movie_id)
  else:
    return redirect("accounts:login")


"""
class AnimeCreateView(CreateView):
    model = Anime
    fields = ['title', 'summary', 'production_studio', 'type', 'genre', 'anime_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()

        for genre in form.cleaned_data['genre']:
            theGenre = get_object_or_404(Genre, name=genre)
            post.genre.add(theGenre)
            post.save()
        anime = form.save()
        return HttpResponseRedirect(reverse('anime_list'))



class AnimeUpdateView(UpdateView):
    model = Anime
    fields = ['title', 'summary', 'type', 'genre', 'anime_image']

    def form_valid(self, form):
        anime = form.save()
        return HttpResponseRedirect(reverse('anime_list'))

class AnimeSelectionView(ListView):
    model = Anime
    template_name = 'catalog/anime_selection_list.html'
    context_object_name = 'anime_list'
    ordering = ['title']

class CrewCreateView(CreateView):
    model = Anime
    fields = ['first_name', 'last_name']
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('index'))

def add_crew_to_anime(request, anime_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    if request.method == 'POST':
        form = CrewMemberForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            #This is to check if the crew member already exists in the database.
            crewmember_instance, created = CrewMember.objects.update_or_create(
                first_name=first_name,
                last_name=last_name,
            )
            if created:
                messages.success(request, f"Added new crew member: {crewmember_instance.first_name} {crewmember_instance.last_name}")
            else:
                messages.info(request, f"Found existing crew member: {crewmember_instance.first_name} {crewmember_instance.last_name} (No update needed to core info)")

            return redirect('add_role_to_crewmember', anime_id=anime.id, crew_member_id=crewmember_instance.id)
    else:
        form = CrewMemberForm()
    context = {
        'form': form,
        'anime': anime
    }
    return render(request, 'catalog/add_crew_to_anime.html', context)

def add_role_to_crewmember(request, anime_id, crew_member_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    crew_member = get_object_or_404(CrewMember, pk=crew_member_id)

    if request.method == 'POST':
        form = CrewRoleForm(request.POST)
        if form.is_valid():
            crew_role_instance = form.save(commit=False)
            crew_role_instance.anime = anime
            crew_role_instance.crew_member = crew_member
            crew_role_instance.save()

            if "save-exit" in request.POST:
                return redirect("index")
            elif "save-new" in request.POST:
                return redirect("add_crew_to_anime", anime_id=anime_id)
            elif "add-character" in request.POST:
                return redirect("add_character", anime_id=anime_id, crew_member_id=crew_member_id)
    else:
        form = CrewRoleForm()
    context = {
        'form': form,
        'anime': anime,
        'crew_member': crew_member,
    }
    return render(request, 'catalog/add_role_to_crewmember.html', context)

def add_character(request, anime_id, crew_member_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    crew_member = get_object_or_404(CrewMember, pk=crew_member_id)

    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character_instance = form.save(commit=False)
            character_instance.anime = anime
            character_instance.crew_member = crew_member
            character_instance.save()

            if "save-exit" in request.POST:
                return redirect("index")
            elif "save-new" in request.POST:
                return redirect("add_crew_to_anime", anime_id=anime_id)
    else:
        form = CharacterForm()

    context = {
        'form': form,
        'anime': anime,
        'crew_member': crew_member,
    }
    return render(request, 'catalog/add_character.html', context)

def anime_crew_list(request, anime_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    directors = CrewRole.objects.filter(anime=anime, role='Director')
    writers = CrewRole.objects.filter(anime=anime, role='Writer')
    voice_actors = Character.objects.filter(anime=anime).select_related('crew_member').order_by('character_name', 'language')
    context = {
        'anime': anime,
        'directors': directors,
        'writers': writers,
        'voice_actors': voice_actors,
    }
    return render(request, 'catalog/anime_crew_list.html', context)

def user_profile_view(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=target_user)
    recent_reviews = Rating.objects.filter(user=target_user).order_by('-created_at')[:3]
    is_owner = request.user.is_authenticated and request.user == target_user
    context = {
        'target_user': target_user,
        'profile': profile,
        'recent_reviews': recent_reviews,
        'is_owner': is_owner,
    }
    return render(request, 'catalog/user_profile.html', context)

def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        selected_avatar = request.POST.get('avatar')
        if user_form.is_valid() and profile_form.is_valid() and selected_avatar:
            user_form.save()
            profile_instance = profile_form.save(commit=False)
            profile_instance.avatar = selected_avatar
            profile_instance.save()
            profile_form.save_m2m()
            return redirect('user_profile', username=user.username)
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'catalog/edit_profile.html', context)