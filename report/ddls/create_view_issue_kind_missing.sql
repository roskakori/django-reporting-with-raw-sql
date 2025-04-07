-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
drop view if exists report.issue_kind_missing;
create view report.issue_kind_missing as
select
    issue.id,
    issue.title,
    label.title as kind
from
    core_issue as issue
    inner join core_issue_labels as issue_labels on
        issue.id = issue_labels.issue_id
    inner join core_label as label on
        label.id = issue_labels.label_id
        and label.title in ('Bug', 'Feature')
