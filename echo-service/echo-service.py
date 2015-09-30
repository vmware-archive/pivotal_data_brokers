import bottle
import json
import os

instance_model = {'bindings': [],'messages': []}
instances = {}

dashboard_template = """
<table class="pure-table">
    <thead>
        <tr>
            <th>Instance</th>
            <th>Database</th>
            <th>Bindings</th>
            <th>Messages</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{{instance_id}}</td>
            <td>{{dbname}}</td>
            <td>{{bindings}}</td>
            <td>{{messages}}</td>
        </tr>
    </tbody>
</table>
"""

# override error handler to return JSON error message provided with call to abort
@bottle.error(401)
@bottle.error(404)
@bottle.error(405)
@bottle.error(409)
@bottle.error(415)
def error(error):
    bottle.response.content_type = 'application/json'
    return '{"error": "%s"}' % error.body

# endpoints used by Service Broker API

@bottle.route('/echo/<instance_id>', method='PUT')
def provision(instance_id):
    """Provision a new instance of echo service

    PUT /echo/<id>:
        id -- instance id

    return:
        JSON document providing the generated ID
        of the newly provisioned instance
    """
    # check for existing instance
    if instance_id in instances:
        bottle.abort(409, "Resource already provisioned for the provided ID")
    # create and store an instance
    instance = {'bindings': [], 'messages': []}
    instances[instance_id] = instance
    # return the instance_id
    return {'instance_id': instance_id, 'state': 'provision_success', 'dashboard_url': "http://localhost:8090/dashboard/"+instance_id}

@bottle.route('/echo/<instance_id>', method='DELETE')
def deprovision(instance_id):
    """Deprovision an existing instance of echo service

    DELETE /echo/<id>:
        id -- instance id

    return:
        JSON document indicating the instance_id and
        the number of related bindings and messages
        that were deleted with the instance
    """
    # remove the instance that corresponds to the given instance_id
    try:
        instance = instances.pop(instance_id)
    except KeyError:
        bottle.abort(404, 'Deprovision failed, Instance not found')
    return {'id': instance_id, 'state': 'deprovision_success', 'bindings': len(instance['bindings']), 'messages': len(instance['messages'])}

@bottle.route('/echo/<instance_id>/<binding_id>', method='PUT')
def bind(instance_id, binding_id):
    """
    Bind an existing instance of echo service to
    the binding_id provided

    PUT /echo/<id>/<app>:
        id -- instance id
        app -- app id

    return:
        JSON document indicating the instance_id,
        binding_id and whether the operation was successful
    """
    # retrieve object for instance_id
    instance = instances.get(instance_id)
    # add binding_id to bindings
    if binding_id in instance['bindings']:
        bottle.abort(409, 'App binding already exists')
    else:
        instance['bindings'].append(binding_id)
    return {'id': instance_id, 'app': binding_id, 'state': 'bind_success'}

@bottle.route('/echo/<instance_id>/<binding_id>', method='DELETE')
def unbind(instance_id, binding_id):
    """
    Unbind an app from an existing instance of echo service

    DELETE /echo/<id>/<app>:
        id -- instance id
        app -- app id

    return:
        JSON document indicating the instance_id,
        binding_id and whether the operation was successful
    """
    # retrieve object for instance_id
    instance = instances.get(instance_id)
    # check for missing binding
    if binding_id not in instance['bindings']:
        bottle.abort(404, 'Binding not found')
    # remove binding_id from bindings
    instance['bindings'].remove(binding_id)
    return {'id': instance_id, 'app': binding_id, 'state': 'unbind_success'}

# accessed via CloudFoundry
@bottle.route('/echo/dashboard/<instance_id>', method='GET')
def dashboard(instance_id):
    """
    Display a simple dashboard showing an instance
    and the number of bindings and messages

    GET /echo/dashboard:

    return:
        HTML showing the current state based on an
        instance and app
    """
    # retrieve instance
    instance = instances.get(instance_id)
    if not instance:
        bottle.abort(404, 'Instance not found')
    # create and send response
    report = bottle.template(dashboard_template,
                      instance_id=instance_id,
                      dbname = instance.get('dbname'),
                      bindings=len(instance.get('bindings')),
                      messages=len(instance.get('messages')))
    return report

# endpoints used by application
@bottle.route('/echo/<instance_id>/<binding_id>', method='POST')
def echo(instance_id, binding_id):
    """
    Log message in instance and echo back

    ACCEPT:
        application/json

    POST /echo/<id>/<app>:
        id -- instance id
        app -- app id

    BODY:
        {"message": "<message>"}

    return:
        JSON document with the message that
        came in with the request
    """
    # extract JSON request from BODY
    if bottle.request.content_type != 'application/json':
        bottle.abort(415, 'Unsupported Content-Type: expecting application/json')
    message = bottle.request.json
    # retrieve instance
    instance = instances.get(instance_id)
    if not instance:
        bottle.abort(404, 'Instance not found')
    # check for binding
    if binding_id not in instance.get('bindings'):
        bottle.abort(404, 'App binding not found')
    # log request
    instance.get('messages').append(message.get('message'))
    # return the message
    return {'response': message.get('message')}

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8090'))
    bottle.run(host='0.0.0.0', port=port, debug=False, reloader=False)
