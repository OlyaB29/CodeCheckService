from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm, FileForm
from .models import File, Log
# from . import tasks
from django.core.mail import EmailMessage
from django.conf import settings


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "check_app/sign_up.html"


class FileCreateView(generic.CreateView):
    form_class = FileForm
    success_url = reverse_lazy("check_app:files")
    template_name = "check_app/home.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class FileUpdateView(generic.UpdateView):
    model = File
    form_class = FileForm
    success_url = reverse_lazy("check_app:files")
    template_name = "check_app/update-file.html"

    def form_valid(self, form):
        form.instance.is_new = True
        return super().form_valid(form)


class FileListView(generic.ListView):
    model = File
    template_name = "check_app/files.html"

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)


class FileDeleteView(generic.DeleteView):
    model = File
    success_url = reverse_lazy("check_app:files")


class LogListView(generic.ListView):
    model = Log
    template_name = "check_app/logs.html"

    def get_queryset(self):
        file = File.objects.get(pk=self.kwargs["file_id"])
        return Log.objects.filter(file=file)