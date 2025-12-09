from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import date

BAD_WORDS = ["ugly", "stupid", "shit", "fuck","gay","fucking","arse","asshole","bitch","bullshit","cock","cunt","dick","dick-head","dumb-ass","faggot","fucked","fucker","fucking","goddammit","horseshit","jack-ass","jackass","motherfucker","nigga","nigra","pigfucker","slut","wanker"]


CrewChoices= [
    ('Director','Director'),
    ('Voice Actor','Voice Actor'),
    ('Writer', 'Writer')
]

class CrewMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def description(self):
        roles_str = [str(role) for role in self.crew_roles.all()]
        character_str = [str(character) for character in self.characters.all()]

        description_lines = []
        if roles_str:
            description_lines.append("\n".join(roles_str))
        if character_str:
            description_lines.append("\n".join(character_str))
        return "\n".join(description_lines)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('crew_member_detail', args=[str(self.id)])

# copy these genres
GenreChoices = [
    ('Adventure','Adventure'),
    ('Action','Action'),
    ('Fantasy', 'Fantasy'),
    ('SciFi', 'SciFi'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Mystery','Mystery'),
    ('Supernatural','Supernatural'),
    ('Romance','Romance'),
    ('Slice of Life','Slice of Life'),
    ('Sports', 'Sports')
]

class Genre(models.Model):
  name = models.CharField(max_length=200, choices=GenreChoices)

  def __str__(self):
    return self.name


AnimeChoices = [('Movie','Movie'), ('Show','Show')]

class Anime(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000,)
    type = models.CharField(max_length=100, choices=AnimeChoices,default='Show')
    production_studio = models.CharField(max_length=100)
    anime_image = models.ImageField(upload_to='images/', null=True, blank=True)
    genre = models.ManyToManyField(Genre, )
    trailer_url = models.URLField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.title
    # anime rating average
    # def average_rating(self):

    def get_absolute_url(self):
        return reverse('anime_detail', args=[str(self.id)])

class Character(models.Model):
    LanguageChoices = [
        ('English','English'),
        ('Japanese','Japanese')
    ]
    crew_member = models.ForeignKey(CrewMember, on_delete=models.CASCADE, related_name='characters')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)
    language = models.CharField(choices=LanguageChoices, max_length=10, default='English')

    class Meta:
        unique_together = ('crew_member', 'anime', 'character_name', 'language')
        ordering = ['character_name']

    def __str__(self):
        return f"{self.crew_member.first_name} {self.crew_member.last_name} voiced {self.character_name} in the {self.language} version of {self.anime.title}."

class CrewRole(models.Model):
    RoleChoices = [
        ('Director','Director'),
        ('Voice Actor','Voice Actor'),
        ('Writer', 'Writer')
    ]
    crew_member = models.ForeignKey(CrewMember, on_delete=models.CASCADE, related_name='crew_roles')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    role = models.CharField(choices=RoleChoices, max_length=20, default='Voice Actor')

    def __str__(self):
        return f"{self.crew_member.first_name} {self.crew_member.last_name} worked as a {self.role} in {self.anime.title}."

class RatingChoices(models.IntegerChoices):
    ONE = 1, '1 star'
    TWO = 2, '2 stars'
    THREE = 3, '3 stars'
    FOUR = 4, '4 stars'
    FIVE = 5, '5 stars'



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add extra fields later like avatar, bio, etc.
    AVATAR_CHOICES = (
        ('avatar1.jpg', 'Avatar 1'),
        ('avatar2.jpg', 'Avatar 2'),
        ('avatar3.jpg', 'Avatar 3'),
        ('avatar4.jpg', 'Avatar 4'),
        ('avatar5.jpg', 'Avatar 5'),
        ('avatar6.jpg', 'Avatar 6'),
        ('avatar7.jpg', 'Avatar 7'),
        ('avatar8.jpg', 'Avatar 8'),
        ('avatar9.jpg', 'Avatar 9'),
        ('avatar10.jpg', 'Avatar 10'),
        ('avatar11.jpg', 'Avatar 11'),
        ('avatar12.jpg', 'Avatar 12'),
    )
    avatar = models.CharField(max_length=100, choices=AVATAR_CHOICES, default='avatar1.jpg')
    bio = models.TextField(max_length=500, default='Learn a little about me...')
    favorite_anime = models.ManyToManyField(Anime, blank=True)
    def __str__(self):
        return self.user.username

class Rating(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField(
        choices=RatingChoices.choices,
        default=RatingChoices.FIVE,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.CharField(max_length=500,default='',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Replace each bad word with asterisks
        for word in BAD_WORDS:
            self.comment = self.comment.replace(word, "*" * len(word))
            self.comment = self.comment.replace(word.capitalize(), "*" * len(word))
            self.comment = self.comment.replace(word.upper(), "*" * len(word))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id}'s {self.get_rating_display()} rating for {self.anime_id}"

    def get_absolute_url(self):
        return reverse('catalog:rating_detail', args=[str(self.id)])

class TrendingNews(models.Model):
    anime_title = models.CharField(max_length=100)
    news_title = models.CharField(max_length=200)
    news_author = models.CharField(max_length=100)
    news_link = models.URLField()

    def get_absolute_url(self):
        return reverse('catalog:news_detail', args=[str(self.id)])

    def __str__(self):
        return self.anime_title
