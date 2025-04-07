-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
drop view if exists report.issue;
create view report.issue as
select
    -- Issue details
    issue.id,
    issue.title,
    issue.state,
    issue.description,
    -- Assignee details
    issue.assignee_id,
    "user".name,
    "user".email
from
    core_issue as issue
    inner join report.user as "user" on  -- NOTE: Quote "user" to prevent keyword clash.
        issue.assignee_id = "user".id
