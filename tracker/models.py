from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["user", "name"], name="unique_category_per_user")]

    def __str__(self):
        return self.name


class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        ON_HOLD = "On Hold", "On Hold"
        COMPLETED = "Completed", "Completed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    categories = models.ManyToManyField(Category, blank=True, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["user", "name"], name="unique_project_per_user")]

    def __str__(self):
        return self.name

    @property
    def total_minutes(self):
        return self.sessions.aggregate(t=models.Sum("duration_minutes"))["t"] or 0


class WorkSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="work_sessions")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sessions")
    session_date = models.DateField(default=timezone.localdate)
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    notes = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-session_date", "-created_at"]

    def clean(self):
        if self.project_id and self.user_id and self.project.user_id != self.user_id:
            raise ValidationError({"project": "You can only log sessions for your own projects."})
        if self.session_date and self.session_date > timezone.localdate():
            raise ValidationError({"session_date": "Session date cannot be in the future."})

    def __str__(self):
        return f"{self.project.name} - {self.session_date} ({self.duration_minutes} min)"
