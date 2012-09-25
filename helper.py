from django.shortcuts import get_object_or_404
from kingofhill.models import Service, State
from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime
import md5
def calucate_point(teamname):

    score = 0
    teams = State.objects.filter(teamname=teamname)
    
    for t in teams:
        if t.end_time is not None:
            time_diff = t.end_time - t.start_time 
            mintues = time_diff.seconds%3600/60
            if t.service.service_name == 'AD': 
                score = score + 2 * (mintues)
            else:
                score = score + mintues
        else:
            pass
    return score

def get_state_number(service):
    
    service = get_object_or_404(Service, service_name = service)
    state = State.objects.filter(service=service).order_by('-state_number')
    if state:
        return state[0].state_number+1
    else:
        return 0


def generate_flag(state_number, service):
    
    if service == "www":
        base = "wadminqwerty"
    elif service == "service":
        base = "sadminqwerty"
    else:
        base = "adadminqwerty"
        
    return md5.md5(base+str(state_number)).hexdigest()


def update_previous_state(state_number, service):
    
    states = State.objects.filter(state_number=state_number)
    service = get_object_or_404(Service, service_name=service)    

    for s in states:
        if s.end_time is None and s.service == service:
            try:
                st = State.objects.get(pk=s.pk)
                st.end_time = datetime.datetime.now()
                st.save()
            except Exception:
                pass


