-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
-- Copyright (C) 2023-2025 by Siisurit e.U., Austria. All rights reserved.
--
-- Drop all Siisurit report views, typically so that they can be re-created anew with a possibly updated data model.
do $$
declare
    view_record record;
begin
    for view_record in
        select
            schemaname,
            viewname
          from
              pg_views
          where
              schemaname = 'report'
    loop
        execute format('drop view if exists %s.%s cascade', view_record.schemaname, view_record.viewname);
    end loop;
end $$;
