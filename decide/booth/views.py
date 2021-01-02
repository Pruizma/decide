import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from base import mods
from census.models import Census
from voting.models import Voting
from store.models import Vote
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models.functions import ExtractMonth
from django.db.models import Count

class LoginView(TemplateView):
    template_name = 'booth/login.html'

class LogoutView(TemplateView):
    template_name = 'booth/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.session.get('user_token')
        if token: 
            mods.post('authentication', entry_point='/logout/', json={'token':token})
            del self.request.session['user_token']
            del self.request.session['voter_id']
    
        return context

def autenticacion(request, username, password):
    token= mods.post('authentication', entry_point='/login/', json={'username':username, 'password':password})
    request.session['user_token']=token
    voter = mods.post('authentication', entry_point='/getuser/', json=token)
    voter_id = voter.get('id', None)
    request.session['voter_id'] = voter_id
    if voter_id == None:
        return False, voter_id
    return True, voter_id

def dashboard_details(voter_id):
    context={}
    vot_dis=[]
    votaciones_por_meses=[]
    context['no_censo'], context['no_vot_dis'] = False, False

    census_by_user = Census.objects.filter(voter_id=voter_id)
    if census_by_user.count() == 0 :
        context['no_censo'] = True
    else:
        list_vid=[]
        for c in census_by_user:
            vid = c.voting_id
            list_vid.append(vid)
        try:
            votaciones = Voting.objects.filter(id__in=list_vid).filter(end_date__isnull=True).exclude(start_date__isnull=True)
            for v in votaciones:
                if Vote.objects.filter(voting_id=v.id, voter_id=voter_id).count()==0:
                    vot_dis.append(v)
        except Exception:
            error='No se encuentra la votación'
        try:
            fecha = datetime.now() + relativedelta(months=-1)
            votaciones_meses = Voting.objects.filter(id__in=list_vid).annotate(month=ExtractMonth('start_date')).values('month').annotate(votaciones=Count('id')).order_by()
            for votaciones_mes in votaciones_meses:
                votaciones_por_meses.append(votaciones_mes['votaciones'])

        except Exception:
            error='No se encuentra la votación'
    
    context['vot_dis'] = vot_dis
    context['votaciones_por_meses'] = votaciones_por_meses
    if len(vot_dis) == 0:
        context['no_vot_dis'] = True
    
    return context

def authentication_login(request):
    
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        # Autenticacion
        voter, voter_id = autenticacion(request, username, password)
        if not voter:
            return render(request, 'booth/login.html', {'no_user':True})
        else:
            context = dashboard_details(voter_id)
            return render(request, 'booth/dashboard.html', context)
    else:

        token = request.session.get('user_token', None)
        if token == None:
            return render(request, 'booth/login.html')
        else:
            voter_id = request.session.get('voter_id', None)
            context = dashboard_details(voter_id)
            return render(request, 'booth/dashboard.html', context)


class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        token = self.request.session.get('user_token', None)
        context['token']= json.dumps(token.get('token', None))
        voter = mods.post('authentication', entry_point='/getuser/', json=token)
        context['voter']= json.dumps(voter)
        voter_id = voter.get('id', None)

        try:
            r = mods.get('voting', params={'id': vid})
            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])

            if Vote.objects.filter(voting_id=vid, voter_id=voter_id).count()!=0:
                context['voted'] = True 

        except:
            raise Http404 

        context['KEYBITS'] = settings.KEYBITS

        return context
