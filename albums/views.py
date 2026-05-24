from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q
import cloudinary.uploader

from .models import Album, Photo, Collaborator
from .forms import AlbumForm, PhotoUploadForm, PhotoEditForm


class AlbumAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        if album.owner == self.request.user:
            return True
        return album.album_collaborators.filter(user=self.request.user, role='admin').exists()


class AlbumContributorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        if album.owner == self.request.user:
            return True
        return album.album_collaborators.filter(
            user=self.request.user, role__in=['admin', 'contributor']
        ).exists()


class HomeView(ListView):
    model           = Album
    template_name   = 'albums/album_list.html'
    context_object_name = 'albums'
    paginate_by     = 12

    def get_queryset(self):
        qs = Album.objects.filter(visibility='public').order_by('-updated_at')
        q  = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'albums/album_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['owned_albums']  = Album.objects.filter(owner=self.request.user).order_by('-updated_at')
        ctx['collab_albums'] = self.request.user.collab_albums.exclude(owner=self.request.user).order_by('-updated_at')
        return ctx


class AlbumDetailView(DetailView):
    model         = Album
    template_name = 'albums/album_detail.html'

    def get_object(self):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        user  = self.request.user
        if album.visibility == 'private':
            if not user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(self.request.get_full_path())
            if album.owner != user and not album.album_collaborators.filter(user=user).exists():
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied
        return album

    def get_context_data(self, **kwargs):
        ctx   = super().get_context_data(**kwargs)
        album = self.object
        user  = self.request.user
        is_owner       = user.is_authenticated and album.owner == user
        is_admin       = user.is_authenticated and album.album_collaborators.filter(user=user, role='admin').exists()
        is_contributor = user.is_authenticated and album.album_collaborators.filter(user=user, role__in=['admin', 'contributor']).exists()
        ctx['photos']        = album.photos.all()
        ctx['collaborators'] = album.album_collaborators.select_related('user')
        ctx['can_edit']      = is_owner or is_admin
        ctx['can_contribute'] = is_owner or is_contributor
        return ctx


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model       = Album
    form_class  = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f'Album "{form.instance.title}" created!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class AlbumUpdateView(AlbumAdminMixin, UpdateView):
    model       = Album
    form_class  = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Album updated.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class AlbumDeleteView(AlbumAdminMixin, DeleteView):
    model         = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url   = reverse_lazy('albums:dashboard')

    def form_valid(self, form):
        album = self.get_object()
        for photo in album.photos.all():
            try:
                cloudinary.uploader.destroy(photo.image.public_id)
            except Exception:
                pass
        messages.success(self.request, f'Album "{album.title}" deleted.')
        return super().form_valid(form)


class PhotoUploadView(AlbumContributorMixin, CreateView):
    model       = Photo
    form_class  = PhotoUploadForm
    template_name = 'albums/album_detail.html'

    def form_valid(self, form):
        album   = get_object_or_404(Album, pk=self.kwargs['pk'])
        files   = self.request.FILES.getlist('image')
        caption = self.request.POST.get('caption', '')
        for file in files:
            Photo.objects.create(album=album, uploaded_by=self.request.user, image=file, caption=caption)
        messages.success(self.request, f'{len(files)} photo(s) uploaded!')
        return redirect(reverse('albums:album_detail', kwargs={'pk': self.kwargs['pk']}))

    def form_invalid(self, form):
        messages.error(self.request, 'Upload failed. Please try again.')
        return redirect(reverse('albums:album_detail', kwargs={'pk': self.kwargs['pk']}))

    def get_success_url(self):
        return reverse('albums:album_detail', kwargs={'pk': self.kwargs['pk']})


class PhotoDetailView(DetailView):
    model         = Photo
    template_name = 'albums/photo_detail.html'

    def get_context_data(self, **kwargs):
        ctx   = super().get_context_data(**kwargs)
        photo = self.object
        album = photo.album
        user  = self.request.user
        photos_qs = list(album.photos.order_by('uploaded_at'))
        idx       = photos_qs.index(photo)
        ctx['prev_photo'] = photos_qs[idx - 1] if idx > 0 else None
        ctx['next_photo'] = photos_qs[idx + 1] if idx < len(photos_qs) - 1 else None
        is_owner = user.is_authenticated and album.owner == user
        is_admin = user.is_authenticated and album.album_collaborators.filter(user=user, role='admin').exists()
        ctx['can_edit'] = is_owner or is_admin
        return ctx


class PhotoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model       = Photo
    form_class  = PhotoEditForm
    template_name = 'albums/photo_form.html'

    def test_func(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        album = photo.album
        if album.owner == self.request.user:
            return True
        return album.album_collaborators.filter(
            user=self.request.user, role__in=['admin', 'contributor']
        ).exists()

    def form_valid(self, form):
        messages.success(self.request, 'Caption updated.')
        return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model         = Photo
    template_name = 'albums/photo_confirm_delete.html'

    def test_func(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        album = photo.album
        if album.owner == self.request.user:
            return True
        return album.album_collaborators.filter(
            user=self.request.user, role__in=['admin', 'contributor']
        ).exists()

    def get_success_url(self):
        return reverse('albums:album_detail', kwargs={'pk': self.object.album.pk})

    def form_valid(self, form):
        photo = self.get_object()
        try:
            cloudinary.uploader.destroy(photo.image.public_id)
        except Exception:
            pass
        messages.success(self.request, 'Photo deleted.')
        return super().form_valid(form)


class CollaboratorAddView(AlbumAdminMixin, View):
    def post(self, request, pk):
        album    = get_object_or_404(Album, pk=pk)
        username = request.POST.get('username', '').strip()
        role     = request.POST.get('role', 'viewer')
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=username)
            if user == album.owner:
                messages.warning(request, 'That user is already the owner.')
            else:
                Collaborator.objects.update_or_create(album=album, user=user, defaults={'role': role})
                messages.success(request, f'{username} added as {role}.')
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found.')
        return redirect(reverse('albums:album_detail', kwargs={'pk': pk}))


class CollaboratorRemoveView(AlbumAdminMixin, View):
    def post(self, request, pk, collab_pk):
        collab = get_object_or_404(Collaborator, pk=collab_pk, album__pk=pk)
        collab.delete()
        messages.success(request, 'Collaborator removed.')
        return redirect(reverse('albums:album_detail', kwargs={'pk': pk}))


class SetCoverView(AlbumAdminMixin, View):
    def test_func(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        album = photo.album
        if album.owner == self.request.user:
            return True
        return album.album_collaborators.filter(user=self.request.user, role='admin').exists()

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        album = photo.album
        album.cover_photo = photo
        album.save()
        messages.success(request, 'Cover photo updated.')
        return redirect(reverse('albums:album_detail', kwargs={'pk': album.pk}))