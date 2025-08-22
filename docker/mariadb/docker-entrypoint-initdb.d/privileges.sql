-- N.B. it's legit to grant privileges regarding a database
-- which doesn't exist (yet) https://stackoverflow.com/a/45131868/2034213
grant all on gregobase.* to db2user;
grant all on test_gregobase.* to db2user;
