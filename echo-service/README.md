CloudFoundry Echo Service (to validate a Service Broker API)
===============

A basic echo service to validate a [Service Broker API v2.3 implementation](https://github.com/dwatrous/cf-service-broker-python) implementation for CloudFoundry, Stackato, or HP Helion Development Platform. This service was designed to respond to provision, bind, unbind and deprovision requests as defined by the [Service Broker API v2.3 specification](http://docs.cloudfoundry.org/services/api.html). This is relevant for CloudFoundry, Stackato and HP Helion Development Platform.

[Step by step example usage in CloudFoundry](http://software.danielwatrous.com/managed-services-in-cloudfoundry/)

[Step by step example usage in Stackato](http://software.danielwatrous.com/managed-services-in-stackato/)

#### Dependencies
 * Python 3.x
 * bottle (http://bottlepy.org/docs/dev/index.html)

# Install and Run

The echo service can be run easily on any system that satisfies the dependiencies above. This repository also contains artifacts that make it easy to deploy to Stackato or HP Helion Development Platform.

## Windows
Clone this repository on to your Windows machine. Change into the directory where the files were cloned and use the python executable to run the script. The console session will look like the snippet below.

```
C:\Users\watrous\Documents\GitHub\cf-echo-service>\Python32\python.exe echo-service.py
Bottle v0.13-dev server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:8090/
Hit Ctrl-C to quit.
```

## Linux
Clone this repository on to your Linux system. Change into the directory and run the script. The session will look something like what's shown below.

```
vagrant@vagrant-ubuntu-trusty-64:~/cf-echo-service$ python3 echo-service.py
Bottle v0.12.7 server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:8090/
Hit Ctrl-C to quit.
```

## Deployed
The echo service can be deployed in stackato using the command line. The snippet below shows what that looks like.

Stackato supports Python 3.3 (at least it did when I wrote this). Before pushing to stackato, update the **runtime.txt** to have "python-3.3"

```
C:\Users\watrous\Documents\GitHub\cf-echo-service>stackato push
Would you like to deploy from the current directory ?  [Yn]:
Using manifest file "manifest.yml"
Application Deployed URL [echo-service.stackato.danielwatrous.com]:
Application Url:   https://echo-service.stackato.danielwatrous.com
Creating Application [echo-service] as [https://api.stackato.danielwatrous.com -> Test -> somespace -> echo-service] ... OK
  Map https://echo-service.stackato.danielwatrous.com ... OK
Bind existing services to 'echo-service' ?  [yN]:
Create services to bind to 'echo-service' ?  [yN]:
Uploading Application [echo-service] ...
  Checking for bad links ...  OK
  Copying to temp space ...  OK
  Checking for available resources ...  OK
  Processing resources ... OK
  Packing application ... OK
  Uploading (3K) ...  OK
Push Status: OK
Starting Application [echo-service] ...
OK
http://echo-service.stackato.danielwatrous.com/ deployed
```

or for CloudFoundry

CloudFoundry supports Python 3.4.1 (at least it did when I wrote this). Before pushing to CloudFoundry, update the **runtime.txt** to have "python-3.4.1"

```
vagrant@vagrant-ubuntu-trusty-64:~/cf-echo-service$ cf push
Using manifest file /home/vagrant/cf-echo-service/manifest.yml

Creating app echo-service in org myorg / space mydept as admin...
OK

Creating route echo-service.10.244.0.34.xip.io...
OK

Binding echo-service.10.244.0.34.xip.io to echo-service...
OK

Uploading echo-service...
Uploading app files from: /home/vagrant/cf-echo-service
Uploading 14.4K, 6 files
Done uploading
OK

Starting app echo-service in org myorg / space mydept as admin...
-----> Downloaded app package (8.0K)
-------> Buildpack version 1.0.5
Use locally cached dependencies where possible
-----> Installing runtime (python-3.4.1)
-----> Installing dependencies with pip
       Downloading/unpacking bottle (from -r requirements.txt (line 1))
         Running setup.py (path:/tmp/pip_build_vcap/bottle/setup.py) egg_info for package bottle

       Installing collected packages: bottle
         Running setup.py install for bottle
           changing mode of build/scripts-3.4/bottle.py from 644 to 755

           changing mode of /app/.heroku/python/bin/bottle.py to 755
       Successfully installed bottle
       Cleaning up...

-----> Uploading droplet (33M)

1 of 1 instances running

App started


OK
Showing health and status for app echo-service in org myorg / space mydept as admin...
OK

requested state: started
instances: 1/1
usage: 256M x 1 instances
urls: echo-service.10.244.0.34.xip.io
last uploaded: Fri Nov 21 20:37:51 UTC 2014

     state     since                    cpu    memory          disk
#0   running   2014-11-21 08:38:27 PM   0.0%   52.2M of 256M   0 of 1G
```

# Usage
To use the echo service, it may be helpful to install a REST client, such as [Fiddler](http://www.telerik.com/download/fiddler) or [Advanced REST Client](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo?hl=en-US). The examples below first show a request and then the expected response.

## Provision

#### Request
The PUT call below, with an empty BODY, provisions(creates) a new resource with the identifier `51897770-560b-11e4-b75a-9ad2017223a9`.
```
PUT http://localhost:8090/echo/51897770-560b-11e4-b75a-9ad2017223a9
```

#### Response
```
{
  instance_id: "51897770-560b-11e4-b75a-9ad2017223a9"
  state: "provision_success"
  dashboard_url: "http://localhost:8090/dashboard/51897770-560b-11e4-b75a-9ad2017223a9"
}
```

## Bind

#### Request
The PUT call below, with an empty BODY, binds an app with the identifier `myapp` to the already provisioned instance `51897770-560b-11e4-b75a-9ad2017223a9`.
```
PUT http://localhost:8090/echo/51897770-560b-11e4-b75a-9ad2017223a9/myapp
```

#### Response
```
{
  app: "myapp"
  id: "51897770-560b-11e4-b75a-9ad2017223a9"
  state: "bind_success"
}
```

## Echo

#### Request
The POST call below sends the JSON document in the BODY to the echo sevice based on a specific instance and binding.
```
POST http://localhost:8090/echo/51897770-560b-11e4-b75a-9ad2017223a9/myapp

{"message": "Hello World"}
```

#### Response
```
{"response": "Hello World"}
```

## Dashboard

#### Request
The GET call below will retrieve a dashboard report for the instance `51897770-560b-11e4-b75a-9ad2017223a9`.
```
GET http://localhost:8090/echo/dashboard/51897770-560b-11e4-b75a-9ad2017223a9
```

#### Response
```html

<table class="pure-table">
    <thead>
        <tr>
            <th>Instance</th>
            <th>Bindings</th>
            <th>Messages</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>51897770-560b-11e4-b75a-9ad2017223a9</td>
            <td>1</td>
            <td>1</td>
        </tr>
    </tbody>
</table>
```

## Unbind

#### Request
The DELETE call below unbinds an app with the identifier `myapp` from the instance `51897770-560b-11e4-b75a-9ad2017223a9`.
```
DELETE http://localhost:8090/echo/51897770-560b-11e4-b75a-9ad2017223a9/myapp
```

#### Response
```
{
  app: "myapp"
  id: "51897770-560b-11e4-b75a-9ad2017223a9"
  state: "unbind_success"
}
```

## Deprovision

#### Request
The DELETE call below deprovisions(deletes) a resource with the identifier `51897770-560b-11e4-b75a-9ad2017223a9`, including any bindings and metadata.
```
DELETE http://localhost:8090/echo/51897770-560b-11e4-b75a-9ad2017223a9
```

#### Response
```
{
  bindings: 0
  state: "deprovision_success"
  messages: 1
  id: "51897770-560b-11e4-b75a-9ad2017223a9"
}
```
