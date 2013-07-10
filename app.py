import datetime
import flask
import importlib
import os
import time
app = flask.Flask(__name__)
app.debug = True

os.environ['TZ'] = 'US/Eastern'
time.tzset()

menu = [
    {'tab': 'Progress', 'path': '/chart/index'},
    {'tab': 'Dummy', 'path': '/dummy/index'}
]

@app.route('/')
def dispatch_root():
    return flask.redirect(menu[0]['path'])

@app.route('/<controller>/')
def dispath_controller(controller):
    return flask.redirect('/%s/index' % controller)

@app.route('/<controller>/<action>/', methods=['GET', 'POST'])
def dispatch_controller_action(controller, action):
    return dispatch(controller, action, None)

@app.route('/<controller>/<action>/<path:path>', methods=['GET', 'POST'])
def dispatch(controller, action, path):
    if controller == 'static':
        # This catch-all otherwise clobbers Flask's static behaviour.
        return app.send_static_file(flask.request.path[8:])
    try:
        controller_module = importlib.import_module('controllers.%s' % controller)
    except ImportError:
        flask.abort(404)

    try:
        action_function = getattr(controller_module, action)
    except AttributeError:
        flask.abort(404)

    # The parameters to pass to the dispatch are any from the URL, the path, and a post if applicable.
    params = flask.request.args.copy()
    params['path'] = path.split('/') if path else []
    if flask.request.method == 'POST':
        params['post'] = flask.request.form

    result = action_function(params)

    # If there's a template, use it.civ
    template_name = '%s/%s.html' % (controller, action)
    if os.path.exists('templates/' + template_name):
        # Allow no return to work, for a template with no parameters.
        if result is None:
            result = dict()
        # Add parameters for layout
        result['tabs'] = tab_info()

        return flask.render_template(template_name, **result)
    else:
        # The Flask encoder doesn't handle dates, so injecting one that does saves some boilerplate.
        return flask.Response(flask.json.dumps(result, cls=LocalJSONEncoder),
            mimetype='application/json')

def tab_info():
    '''
    Info about all tabs including which is selected, for the layout and navbar.
    '''
    result = []
    for menu_tab in menu:
        tab = menu_tab.copy()
        tab['selected'] = flask.request.path.startswith(tab['path'])
        result.append(tab)

    return result

class LocalJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()

if __name__ == '__main__':
    app.run()