import os

from sanic import Blueprint
from sanic.response import html, redirect

from zapier_fun.forms import IntroduceForm
from zapier_fun.utils import call_webhook
from zapier_fun.utils import BaseView

core = Blueprint('core')

PATH = os.path.dirname(os.path.realpath(__file__))


class IndexView(BaseView):

    async def get(self, request):
        return redirect('/introduce')


class ThanksView(BaseView):

    async def get(self, request):
        return html(self.render('thanks'))


class IntroduceView(BaseView):

    async def get(self, request):
        form = IntroduceForm()
        return html(self.render('introduce', context={"form": form}))

    async def post(self, request):

        form = IntroduceForm(request.form)

        if form.validate():

            await call_webhook(form)

            return redirect('/thanks')

        return html(self.render('introduce', context={"form": form}), 400)


core.add_route(IndexView.as_view(), '/')
core.add_route(IntroduceView.as_view(), '/introduce')
core.add_route(ThanksView.as_view(), '/thanks')
