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

    output_txt = "<HTML>dbhost=" + dbhost + "<BR>" + "dbname=" + dbname + "<BR>" + "dbuser=" + dbuser + "<BR>" + "dbpassword=" + dbpassword + "<BR></HTML>"


    con = None
    con = psycopg2.connect(user="gpadmin", database=dbname,host=dbhost , password="gpadmin")
    cur = con.cursor()
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur.execute('DROP TABLE IF EXISTS t1')
    cur.execute('CREATE TABLE t1 (c1 int)' )
    cur.execute('INSERT into t1 VALUES (1),(2),(3)')

    sql = "DROP TABLE IF EXISTS test_data; " \
    "DROP SCHEMA IF EXISTS myschema CASCADE; " \
    "CREATE TABLE test_data (trans_id INT, product TEXT); " \
    "CREATE SCHEMA myschema; " \
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

    output_txt = output_txt + sql

    cur.execute(sql)

    sql = "SELECT * FROM madlib.assoc_rules( .25, .5,'trans_id','product','test_data','myschema',TRUE);"
    cur.execute(sql)


    return output_txt

@route('/t1')
def t1():
    return bottle.request.json

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    bottle.run(host='0.0.0.0', port=port, debug=True, reloader=False)

