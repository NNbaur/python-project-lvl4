from django.views.generic.base import TemplateView


class View(TemplateView):
    template_name = 'greet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['who'] = 'World'
        return context