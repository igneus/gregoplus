# gregoplus

[![Build Status](https://travis-ci.org/igneus/gregobase.svg?branch=master)](https://travis-ci.org/igneus/gregobase)

[GregoBase](https://gregobase.selapa.net/)
([sources](https://github.com/olivierberten/GregoBase))
is a unique resource of Gregorian chant scores
transcribed using
[Gregorio](http://gregorio-project.github.io/),
but there is almost no active development
and contributions are not accepted.

Fortunately, the database is publicly available.
Thus *gregoplus* uses *GregoBase*'s database to make its contents
more accessible.
The site is read-only. It doesn't attempt to replace
*GregoBase*, but to provide additional tools for exploring
its contents.

Contributions are warmly welcome.
Python was chosen as implementation language,
because it seems to be the scripting language of choice
in the open source music engraving community.

## Desired features

- [ ] parameterized filtering
- [ ] mass gabc export
- [ ] complete score text (for copy-pasting, reachability by fulltext search etc.)
- [ ] links to the CANTUS database
- [ ] JSON API

## Running

* get [GregoBase DB export](https://github.com/gregorio-project/GregoBase/blob/master/gregobase_online.sql),
  import it in a MySQL database, e. g. `$ mysql -u myuser < gregobase_online.sql`
* install requirements `$ pip install -r requirements.txt`
* run migrations `$ python manage.py migrate`
* for local development `$ python manage.py runserver`, for production deployment see Django documentation

## License

GNU/GPL 3.0
