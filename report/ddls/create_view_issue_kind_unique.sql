-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
drop view if exists report.issue_kind_unique;
create view report.issue_kind_unique as
with issue_kind as (
    select
        issue_labels.issue_id,
        issue_labels.label_id,
        label.title,
        -- Partition by issue
        row_number() over (
            partition by issue_labels.issue_id
            order by label.title
        ) as "label_number"
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
        -- Pick only the first label of the issue
        and issue_kind.label_number = 1
