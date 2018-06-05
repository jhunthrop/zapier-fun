from sanic import Sanic
import wtforms_json

from zapier_fun import settings
from zapier_fun.api.v1.api import v1
from zapier_fun.ui.core import core

app = Sanic(__name__)

app.static('/static', settings.STATIC_DIR)

app.blueprint(core)
app.blueprint(v1)

wtforms_json.init()


def main():
    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    main()
