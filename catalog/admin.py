from django.contrib import admin
from .models import Genre, Anime, Rating, CrewMember, CrewRole, Character, TrendingNews, UserProfile

admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(TrendingNews)
admin.site.register(UserProfile)

@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name')

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'display_genres')
    search_fields = ('title', 'summary')
    list_filter = ('type', 'genre')

    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'type', 'genre', 'anime_image')
        }),
    )

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    display_genres.short_description = "Genres"