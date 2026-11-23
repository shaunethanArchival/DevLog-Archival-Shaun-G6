from django import forms
from django.utils import timezone

from .models import Category, Project, WorkSession


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Category name cannot be blank.")
        if Category.objects.filter(user=self.user, name__iexact=name).exists():
            raise forms.ValidationError("You already have a category with this name.")
        return name


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "status", "categories"]
        widgets = {"categories": forms.CheckboxSelectMultiple, "description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["categories"].queryset = Category.objects.filter(user=user)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Project name cannot be blank.")
        qs = Project.objects.filter(user=self.user, name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("You already have a project with this name.")
        return name


class WorkSessionForm(forms.ModelForm):
    class Meta:
        model = WorkSession
        fields = ["project", "session_date", "duration_minutes", "notes"]
        widgets = {
            "session_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }
        labels = {"duration_minutes": "Duration (minutes)"}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(user=user)
        self.user = user

    def _post_clean(self):
        self.instance.user = self.user   # lets model.clean() verify project ownership
        super()._post_clean()

    def clean_duration_minutes(self):
        d = self.cleaned_data["duration_minutes"]
        if d is None or d < 1:
            raise forms.ValidationError("Duration must be a positive whole number of minutes.")
        return d

    def clean_session_date(self):
        d = self.cleaned_data["session_date"]
        if d > timezone.localdate():
            raise forms.ValidationError("Session date cannot be in the future.")
        return d
