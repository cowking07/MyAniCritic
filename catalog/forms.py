from django import forms
from .models import Rating, Anime, CrewMember, CrewRole, Character


class RatingForm(forms.ModelForm):

  class Meta:
    model = Rating
    fields = {"comment", "rating"}
    labels = {
      'comment': '',
      'rating': '',
    }
    # reference git uses widget

class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = ['title', 'summary', 'type', 'genre', 'production_studio', 'anime_image']

class CrewRoleForm(forms.ModelForm):
    class Meta:
        model = CrewRole
        fields = ['role']

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['character_name', 'language']

class CrewMemberForm(forms.ModelForm):
    class Meta:
        model = CrewMember
        fields = ['first_name', 'last_name']
