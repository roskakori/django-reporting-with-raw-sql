-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
drop view if exists report.issue_labels;
create view report.issue_labels as
select
    issue_id,
    label_id
from
    core_issue_labels
