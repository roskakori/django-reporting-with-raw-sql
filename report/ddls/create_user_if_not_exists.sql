-- Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
-- Create user unless it already exists.
do $$
begin
    if not exists (
        select from pg_user where usename = :username
    ) then
        -- NOTE: We cannot use `:username` here because it has to be quoted in double quotes.
        --  This means the caller has to replace ${username} by themselves. Because of that,
        --  this SQL statement is vulnerable to injections, so outside validation of the
        --  username is is mandatory.
        create user "${username}" with password :password;
    end if;
end $$;
