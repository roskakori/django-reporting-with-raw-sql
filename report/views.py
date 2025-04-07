# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
from django.shortcuts import render

from core.models import Issue


def issue_list(request):
    issues = Issue.objects.values("assignee", "id", "labels", "title", "state")
    return render(request, "report/issue_list.html", {"issues": issues})
