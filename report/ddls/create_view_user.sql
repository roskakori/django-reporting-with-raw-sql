-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
drop view if exists report.user;
create view report.user as
select
    id,
    email,
    first_name,
    is_active,
    last_name,
    username,
    trim(concat(first_name, ' ', last_name)) as name
from
    auth_user;
