from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Album(models.Model):
    VISIBILITY_CHOICES = [
        ('public',   'Public'),
        ('unlisted', 'Unlisted'),
        ('private',  'Private'),
    ]
    owner        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_albums')
    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    visibility   = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    cover_photo  = models.ForeignKey('Photo', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    collaborators = models.ManyToManyField(User, through='Collaborator', related_name='collab_albums', blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('albums:album_detail', kwargs={'pk': self.pk})

    @property
    def photo_count(self): return self.photos.count()

    @property
    def cover_url(self):
        if self.cover_photo:
            return self.cover_photo.image.url
        first = self.photos.first()
        return first.image.url if first else None


class Photo(models.Model):
    album       = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image       = CloudinaryField()
    caption     = models.CharField(max_length=300, blank=True)
    taken_at    = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.caption or f"Photo {self.pk}"
    def get_absolute_url(self): return reverse('albums:photo_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['uploaded_at']


class Collaborator(models.Model):
    ROLE_CHOICES = [
        ('viewer',      'Viewer'),
        ('contributor', 'Contributor'),
        ('admin',       'Admin'),
    ]
    album    = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_collaborators')
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations')
    role     = models.CharField(max_length=15, choices=ROLE_CHOICES, default='viewer')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('album', 'user')