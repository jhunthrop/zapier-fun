from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView

from zapier_fun.exceptions import ZapierException
from zapier_fun.forms import IntroduceForm
from zapier_fun.utils import call_webhook

v1 = Blueprint('v1', url_prefix='/api/v1')


class IntroduceView(HTTPMethodView):

    async def post(self, request):
        """Introduce yourself"""

        form = IntroduceForm.from_json(request.json)

        if not form.validate():

            return json({"errors": form.errors}, status=400)

        try:
            response = await call_webhook(form)
        except ZapierException as e:
            abort(500, "There was an issue calling the "
                  "Zapier web hook: {0} {1}".format(type(e).__name__, e))

        return json(response)


v1.add_route(IntroduceView.as_view(), '/introduce')
