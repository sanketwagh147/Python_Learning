-- CREATE TABLE information(
--     info_id SERIAL PRIMARY KEY,
--     title VARCHAR(500) NOT NULL,
--     person VARCHAR(500) NOT NULL UNIQUE
-- )

-- select * from information

-- alter table information
-- rename to new_info

-- select * from new_info



-- alter table new_info
-- rename column person to people

-- select * from new_info

-- alter table new_info
-- alter column people drop not null

-- insert into new_info(title)
-- VALUES
-- ('some new values')

-- select * from new_info

-- ALTER TABLE new_info
-- DROP COLUMN people

-- SELECT * FROM new_info

ALTER TABLE new_info
DROP COLUMN  IF EXISTS people