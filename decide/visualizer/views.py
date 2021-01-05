import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from census.models import Census
from store.models import Vote


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context

class StatisticsView(TemplateView):
    template_name = 'visualizer/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            census = Census.objects.filter(voting_id=vid).all()
            votes = Vote.objects.filter(voting_id=vid).all()
            c=census.count()
            v=votes.count()
            stat = {"census":c}
            stat["votes"] = v
            if v>0:
                stat["percentage"] = round(v/c*100,2);
            else:
                stat["percentage"] = 0;
            context['voting'] = json.dumps(r[0])
            context['stats'] = json.dumps(stat)
        except:
            raise Http404

        return context