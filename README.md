# gregoplus

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

* get [GregoBase DB export](https://github.com/gregorio-project/GregoBase/blob/master/gregobase_online.sql),
  import it in a MySQL database, e. g. `$ mysql -u myuser < gregobase_online.sql`
* install requirements `$ pip install -r requirements.txt`
* copy `.env.template` to `.env`, populate it with the required values
  (or otherwise set the respective environment variables)
* run migrations `$ python manage.py migrate`
* for local development `$ python manage.py runserver`, for production deployment see Django documentation

## License

GNU/GPL 3.0
