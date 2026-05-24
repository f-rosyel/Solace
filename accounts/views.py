from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm, CustomAuthenticationForm
from albums.models import Album, Collaborator


class RegisterView(CreateView):
    form_class   = RegisterForm
    template_name = 'registration/register.html'
    success_url   = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(self.request, 'Account created! Please sign in.')
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx  = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['owned_albums']  = Album.objects.filter(owner=user).order_by('-updated_at')
        ctx['photo_count']   = user.photos.count()
        ctx['collab_count']  = Collaborator.objects.filter(user=user).exclude(album__owner=user).count()
        return ctx