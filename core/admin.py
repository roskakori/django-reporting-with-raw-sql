# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
from django.contrib import admin

from core.models import Issue, Label


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "state", "assignee__username")
    list_filter = ("state", "assignee")
    ordering = ["title", "id"]
    search_fields = ("description", "title")


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    ordering = ["title"]
