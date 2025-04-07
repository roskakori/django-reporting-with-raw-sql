-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
select
    issue_labels.issue_id,
    label.title
from
    core_issue_labels as issue_labels
    inner join core_label as label on
        label.id = issue_labels.label_id
where
    label.title in ('Bug', 'Feature')
