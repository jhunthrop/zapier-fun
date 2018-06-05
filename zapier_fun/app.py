from sanic import Sanic
import wtforms_json

from zapier_fun.api.v1.api import v1
from zapier_fun.ui.core import core

app = Sanic(__name__)

app.static('/static', 'static')

app.blueprint(core)
app.blueprint(v1)

wtforms_json.init()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
