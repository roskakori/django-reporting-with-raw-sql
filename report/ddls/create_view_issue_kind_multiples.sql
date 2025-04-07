-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
drop view if exists report.issue_kind_multiples;
create view report.issue_kind_multiples as
with issue_kind as (
    select
        issue_labels.issue_id,
        label.title
    from
        core_issue_labels as issue_labels
        inner join core_label as label on
            label.id = issue_labels.label_id
    where
        label.title in ('Bug', 'Feature')
)
select
    issue.id,
    issue.title,
    coalesce(issue_kind.title, '???') as kind
from
    core_issue as issue
    left join issue_kind on
        issue_kind.issue_id = issue.id
