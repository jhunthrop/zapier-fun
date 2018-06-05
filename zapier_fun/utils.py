import os
from aiohttp import ClientSession

from htmlmin import minify
from jinja2 import FileSystemLoader, Environment
from sanic.views import HTTPMethodView

from zapier_fun import settings
from zapier_fun.exceptions import ViewException, ZapierException


class BaseView(HTTPMethodView):

    def __init__(self):
        """Constructor"""
        templates_dir = settings.TEMPLATES_DIR
        if not os.path.exists(templates_dir):
            raise ValueError("The template directory specified: {} "
                             "does not exist".format(templates_dir))
        loader = FileSystemLoader([templates_dir])
        self.engine = Environment(loader=loader, autoescape=True)

    def render_as_html(self, template, context):
        """Render a template given the template name and rendering context

        :param template: The name of the template to render.
        :type template: str.
        :param context: The context variables for rendering.
        :type context: dict.
        :returns: str -- Jinja2 renderered template.

        """
        t = self.engine.get_template(template + '.html')
        return t.render(**context)

    def render(self, template, context=None, ctype='html'):
        """Render a template

        :param template: The name of the template to render.
        :type template: str.
        :param context: The context variables for rendering.
        :type context: dict.
        :returns: str -- Jinja2 renderered template.
        :raises: ViewException

        """
        if not context:
            context = {}

        renderer = getattr(self, 'render_as_' + ctype, None)

        if renderer and callable(renderer):
            try:
                return minify(renderer(template, context))
            except Exception as e:
                raise ViewException(
                    "Problem rendering view {0}: {1} {2}".format(
                        ctype, type(e).__name__, e))

        raise self.ViewException("View format `{0}` is unknown".format(ctype))


async def post_zap(session, payload):
    """Post Zapier webhook

    :param session: An aiohttp client session.
    :type session: aiohttp ClientSession object.
    :param payload: JSON payload to post.
    :type payload: Dict.
    :returns: json
    :raises: ZapierException.
    """
    try:
        async with session.post(settings.WEBHOOK_URL,
                                json=payload) as response:
            r = await response.json()
            if r["status"] != "success":
                raise ZapierException(
                    "Zapier returned an invalid status: {0}".format(
                        r['status']))
            return r
    # -1 laziness
    except Exception as e:
        raise ZapierException(
            "Error communicating with Zapier: {0} {1}".format(type(e).__name__,
                                                              e)) from e


async def call_webhook(form):
    """Wrapper function for calling zapier webhook

    :param form: IntroduceForm object.
    :type form: Object.
    :returns: json

    """
    payload = {'contact': {}}
    payload['contact']['name'] = "{} {}".format(form.first_name.data,
                                                form.last_name.data)
    payload['contact']['email'] = form.email.data

    async with ClientSession() as session:
        return await post_zap(session, payload)
