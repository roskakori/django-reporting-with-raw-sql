-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
-- Copyright (C) 2023-2025 by Siisurit e.U., Austria. All rights reserved.
--
-- Grant a user access to reports.
grant connect on database "${database}" to "${username}";
revoke all privileges on schema public from "${username}";
grant usage on schema report to "${username}";
grant select on all tables in schema report to "${username}";
alter default privileges in schema report grant select on tables to "${username}";
-- TODO: Do we need this? alter role "${username}" set search_path = 'report';
