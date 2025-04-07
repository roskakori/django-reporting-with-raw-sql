# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
import pytest
from django.contrib.auth.models import User
from django.db.models import Count, Q

from core.management.commands.make_demo import make_demo_issues, make_demo_users
from core.models import IssueState


@pytest.mark.django_db
def test_can_compute_done_issue_count_per_user():
    make_demo_users()
    make_demo_issues()
    done_issue_count_per_user = (
        User.objects.annotate(done_issue_count=Count("issues", filter=Q(issues__state=IssueState.DONE)))
        .values("username", "done_issue_count")
        .filter(done_issue_count__gt=0)
    )
    assert done_issue_count_per_user.exists()
