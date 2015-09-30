import json,os,bottle
import psycopg2
from bottle import route, run, template
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

## Pull in CloudFoundry's production settings
if 'VCAP_SERVICES' in os.environ:
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    # XXX: avoid hardcoding here
    dbuser = vcap_services['Echo Service'][0]['credentials']['dbuser']
    dbpassword = vcap_services['Echo Service'][0]['credentials']['dbpassword']
    dbhost = vcap_services['Echo Service'][0]['credentials']['dbhost']
    dbname = vcap_services['Echo Service'][0]['credentials']['dbname']

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/test')
def test():

    con = None
    con = psycopg2.connect(user= dbuser, database= dbname,host = dbhost , password= dbpassword)
    cur = con.cursor()
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur.execute('DROP TABLE IF EXISTS t1')
    cur.execute('CREATE TABLE t1 (c1 int)' )
    cur.execute('INSERT into t1 VALUES (1),(2),(3)')

    sql = "DROP TABLE IF EXISTS test_data; " \
    "CREATE TABLE test_data (trans_id INT, product TEXT); " \
    "INSERT INTO test_data VALUES (1, 'beer'); " \
    "INSERT INTO test_data VALUES (1, 'diapers'); " \
    "INSERT INTO test_data VALUES (1, 'chips'); " \
    "INSERT INTO test_data VALUES (2, 'beer'); " \
    "INSERT INTO test_data VALUES (2, 'diapers'); " \
    "INSERT INTO test_data VALUES (3, 'beer'); " \
    "INSERT INTO test_data VALUES (3, 'diapers'); " \
    "INSERT INTO test_data VALUES (4, 'beer'); " \
    "INSERT INTO test_data VALUES (4, 'chips'); " \
    "INSERT INTO test_data VALUES (5, 'beer'); " \
    "INSERT INTO test_data VALUES (6, 'beer'); " \
    "INSERT INTO test_data VALUES (6, 'diapers'); " \
    "INSERT INTO test_data VALUES (6, 'chips'); " \
    "INSERT INTO test_data VALUES (7, 'beer'); " \
    "INSERT INTO test_data VALUES (7, 'diapers'); " \

    cur.execute(sql)

    return dbuser

@route('/t1')
def t1():
    return bottle.request.json

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    bottle.run(host='0.0.0.0', port=port, debug=True, reloader=False)

