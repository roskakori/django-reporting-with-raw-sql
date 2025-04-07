# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Issue, IssueState, Label
from report.reports import output_info

DEFAULT_ISSUE_COUNT = 10

DEMO_FIRST_NAMES = [
    "Alice",
    "Bob",
    "Claire",
    "Daniel",
    "Emily",
    "Felix",
    "Gina",
    "Henry",
    "Isabel",
    "James",
    "Kylie",
    "Lucas",
    "Mila",
    "Noah",
]

DEMO_LAST_NAMES = [
    "Adams",
    "Brown",
    "Clark",
    "Davis",
    "Evans",
    "Fisher",
    "Green",
    "Hall",
    "Ivy",
    "Jones",
    "King",
    "Lee",
    "Miller",
    "Nelson",
]
assert len(DEMO_FIRST_NAMES) == len(DEMO_LAST_NAMES)
DEMO_USERNAMES = [first_name.lower() for first_name in DEMO_FIRST_NAMES]
DEFAULT_USER_COUNT = len(DEMO_FIRST_NAMES)

ISSUE_TITLE_ACTIONS = ["Add", "Change", "Improve", "Optimize"]
ISSUE_TITLE_NAMES = ["cart", "login", "product", "purchase", "search", "settings", "user"]
ISSUE_TITLE_ITEMS = ["dialog", "data model", "attribute", "process", "export"]

_RANDOMIZER = random.Random(0)


class Command(BaseCommand):
    help = "Make demo data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            "-C",
            action="store_true",
            help="remove any possibly existing data first",
        )
        parser.add_argument(
            "--issues",
            "-i",
            default=DEFAULT_ISSUE_COUNT,
            metavar="NUMBER",
            type=int,
            help="Number of demo issue to create",
        )

    def handle(self, *_args, **options):
        has_to_prune = options["clear"]
        issue_count = options["issues"]
        if has_to_prune:
            self.stdout.write("Removing existing data")
            Issue.objects.all().delete()
            Label.objects.all().delete()
        user_count = min(issue_count, DEFAULT_USER_COUNT)
        make_demo_users(self.stdout, user_count)
        make_demo_issues(self.stdout, issue_count)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {user_count} users."))

    # def make_demo_users(self, user_count: int = DEFAULT_USER_COUNT):
    #     for user_index in range(user_count):
    #         if user_index < DEFAULT_USER_COUNT:
    #             first_name = DEMO_FIRST_NAMES[user_index]
    #             last_name = DEMO_LAST_NAMES[user_index]
    #             username = DEMO_USERNAMES[user_index]
    #             email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    #         else:
    #             first_name = ""
    #             last_name = f"User{user_index + 1}"
    #             username = last_name.lower()
    #             email = f"{username}@example.com"
    #         with transaction.atomic():
    #             existing_users = User.objects.filter(username=username).select_for_update()
    #             if not existing_users.exists():
    #                 self.stdout.write(f"  Creating user {username}")
    #                 User.objects.create_user(
    #                     username=username, email=email, first_name=first_name, is_active=False, last_name=last_name
    #                 )

    # def make_demo_issues(self, issue_count: int = DEFAULT_ISSUE_COUNT):
    #     issue_kind_label_titles = ["Bug", "Feature"]
    #     other_label_titles = ["DevOps", "Models", "UI", "Workflow"]
    #     for label_titel in issue_kind_label_titles + other_label_titles:
    #         Label.objects.get_or_create(title=label_titel)
    #     issue_kind_labels = list(Label.objects.filter(title__in=issue_kind_label_titles))
    #     other_labels = list(Label.objects.filter(title__in=other_label_titles))
    #     users = list(User.objects.filter(username__in=DEMO_USERNAMES))
    #     issue_states = list(IssueState)
    #     for issue_index in range(issue_count):
    #         issue_labels = (
    #             list(issue_kind_labels)
    #             if issue_index % 10 == 0
    #             else [_RANDOMIZER.choice(issue_kind_labels)]
    #             if issue_index % 4 != 0
    #             else []
    #         )
    #         is_bug = any(True for issue_label in issue_labels if issue_label.title == "Bug")
    #         other_label_count = _RANDOMIZER.randint(0, 4)
    #         issue_labels += _RANDOMIZER.choices(other_labels, k=other_label_count)
    #         user = _RANDOMIZER.choice(users)
    #         word_pools = [["Fix"] if is_bug else ISSUE_TITLE_ACTIONS, ISSUE_TITLE_NAMES, ISSUE_TITLE_ITEMS]
    #         title = " ".join(_RANDOMIZER.choice(words) for words in word_pools)
    #         description = lorem_ipsum(_RANDOMIZER.randint(10, 25))
    #         issue = Issue.objects.create(
    #             title=title,
    #             assignee=user,
    #             description=description,
    #             state=_RANDOMIZER.choice(issue_states),
    #         )
    #         issue.labels.set(issue_labels)


def make_demo_users(output=None, user_count: int = DEFAULT_USER_COUNT):
    for user_index in range(user_count):
        if user_index < DEFAULT_USER_COUNT:
            first_name = DEMO_FIRST_NAMES[user_index]
            last_name = DEMO_LAST_NAMES[user_index]
            username = DEMO_USERNAMES[user_index]
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        else:
            first_name = ""
            last_name = f"User{user_index + 1}"
            username = last_name.lower()
            email = f"{username}@example.com"
        with transaction.atomic():
            existing_users = User.objects.filter(username=username).select_for_update()
            if not existing_users.exists():
                output_info(output, f"  Creating user {username}")
                User.objects.create_user(
                    username=username, email=email, first_name=first_name, is_active=False, last_name=last_name
                )


def make_demo_issues(output=None, issue_count: int = DEFAULT_ISSUE_COUNT):
    issue_kind_label_titles = ["Bug", "Feature"]
    other_label_titles = ["DevOps", "Models", "UI", "Workflow"]
    output_info(output, "  Creating demo labels")
    for label_titel in issue_kind_label_titles + other_label_titles:
        Label.objects.get_or_create(title=label_titel)
    issue_kind_labels = list(Label.objects.filter(title__in=issue_kind_label_titles))
    other_labels = list(Label.objects.filter(title__in=other_label_titles))
    users = list(User.objects.filter(username__in=DEMO_USERNAMES))
    issue_states = list(IssueState)
    output_info(output, f"  Creating demo {issue_count} issues")
    for issue_index in range(issue_count):
        issue_labels = (
            list(issue_kind_labels)
            if issue_index % 10 == 0
            else [_RANDOMIZER.choice(issue_kind_labels)]
            if issue_index % 4 != 0
            else []
        )
        is_bug = any(True for issue_label in issue_labels if issue_label.title == "Bug")
        other_label_count = _RANDOMIZER.randint(0, 4)
        issue_labels += _RANDOMIZER.choices(other_labels, k=other_label_count)
        user = _RANDOMIZER.choice(users)
        word_pools = [["Fix"] if is_bug else ISSUE_TITLE_ACTIONS, ISSUE_TITLE_NAMES, ISSUE_TITLE_ITEMS]
        title = " ".join(_RANDOMIZER.choice(words) for words in word_pools)
        description = lorem_ipsum(_RANDOMIZER.randint(10, 25))
        issue = Issue.objects.create(
            title=title,
            assignee=user,
            description=description,
            state=_RANDOMIZER.choice(issue_states),
        )
        issue.labels.set(issue_labels)


def lorem_ipsum(word_count=50):
    lorem_ipsum_words = [
        "lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "sed",
        "do",
        "eiusmod",
        "tempor",
        "incididunt",
        "ut",
        "labore",
        "et",
        "dolore",
        "magna",
        "aliqua",
        "enim",
        "ad",
        "minim",
        "veniam",
        "quis",
    ]
    selected_words = _RANDOMIZER.choices(lorem_ipsum_words, k=word_count)
    return " ".join(selected_words) + "."
