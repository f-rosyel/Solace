from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('',                                        views.HomeView.as_view(),              name='home'),
    path('',                                        views.HomeView.as_view(),              name='album-list'),
    path('dashboard/',                              views.DashboardView.as_view(),         name='dashboard'),
    path('albums/create/',                          views.AlbumCreateView.as_view(),       name='album_create'),
    path('albums/create/',                          views.AlbumCreateView.as_view(),       name='album-create'),
    path('albums/<int:pk>/',                        views.AlbumDetailView.as_view(),       name='album_detail'),
    path('albums/<int:pk>/',                        views.AlbumDetailView.as_view(),       name='album-detail'),
    path('albums/<int:pk>/edit/',                   views.AlbumUpdateView.as_view(),       name='album_edit'),
    path('albums/<int:pk>/delete/',                 views.AlbumDeleteView.as_view(),       name='album_delete'),
    path('albums/<int:pk>/delete/',                 views.AlbumDeleteView.as_view(),       name='album-delete'),
    path('albums/<int:pk>/upload/',                 views.PhotoUploadView.as_view(),       name='photo_upload'),
    path('albums/<int:pk>/collaborators/add/',      views.CollaboratorAddView.as_view(),   name='collab_add'),
    path('albums/<int:pk>/collaborators/<int:collab_pk>/remove/', views.CollaboratorRemoveView.as_view(), name='collab_remove'),
    path('photos/<int:pk>/',                        views.PhotoDetailView.as_view(),       name='photo_detail'),
    path('photos/<int:pk>/edit/',                   views.PhotoEditView.as_view(),         name='photo_edit'),
    path('photos/<int:pk>/delete/',                 views.PhotoDeleteView.as_view(),       name='photo_delete'),
    path('photos/<int:pk>/set-cover/',              views.SetCoverView.as_view(),          name='set_cover'),
    path('albums/<int:album_pk>/photos/<int:pk>/',         views.PhotoDetailView.as_view(), name='photo-detail'),
    path('albums/<int:album_pk>/photos/<int:pk>/delete/',  views.PhotoDeleteView.as_view(), name='photo-delete'),
]