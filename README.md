# gregoplus

![Build Status](https://github.com/igneus/gregoplus/actions/workflows/ci.yml/badge.svg)

Readonly chant database based on the publicly available
[GregoBase](https://gregobase.selapa.net/)
([sources](https://github.com/olivierberten/GregoBase))
database dump.

GregoBase has been great in attracting contributors and accumulating
chant transcriptions ready for reuse;
GregoPlus strives to use the full potential of the data thus collected
and provide its users with improved tools for browsing, searching
and analyzing the chant repertory.

## Desired features

- [ ] parameterized filtering
- [ ] mass gabc export
- [ ] complete score text (for copy-pasting, reachability by fulltext search etc.)
- [ ] JSON API

## Running

* install requirements `$ pip install -r requirements.txt`
* `$ docker compose up` to spin up a dockerized MariaDB instance
  (or otherwise make available a compatible database server)
* copy `.env.template` to `.env`, populate it with db credentials and other required values
  (or otherwise set the respective environment variables)
* `$ ./init_data.sh` to initialize the database
* for local development `$ python manage.py runserver`, for production deployment see Django documentation

## Tests

`$ python manage.py test`

## License

GNU/GPL 3.0
