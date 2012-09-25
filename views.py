from kingofhill.models import Service, State
from register.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from kingofhill.helper import *
from secondround.helper import *
from kingofhill.forms import FlagForm

"""
This is the home page, where the king(team) of the hill will be displayed \


"""

def access_error(request):
    return render_to_response("contest/kingofhill/error.html",{}, context_instance = RequestContext(request))


def kinghome(request):
    
    if not validate_user(request):
        return access_error(request)

    king = "No king"
    status = []
    try:
        state = State.objects.all() 
        service = get_object_or_404(Service, service_name='AD')  
        for team in state:
            if team.end_time is None and team.service == service:
                king = team.teamname

        for team_status in state:
            row = []
            if team_status.end_time is not None: 
                row.append(team_status.service.service_name)
                row.append(team_status.teamname.teamname)
                row.append(team_status.end_time - team_status.start_time)
                status.append(row)  

        return render_to_response("contest/kingofhill/kinghome.html",{'king':king, 'status':status},\
                                context_instance = RequestContext(request))
    except Exception:
        king = "No team could make it to the kingdom"

    return render_to_response("contest/kingofhill/kinghome.html",{'king':king, 'status':status}, \
                                context_instance = RequestContext(request))

def scoreboard(request):
    
    if not validate_user(request):
        return access_error(request)

    score, row, status_team = [], [], []
    try:
        status_team = [team.teamname for team in State.objects.all()]
        for team in Team.objects.all():
            row = []
            if team in status_team:
                row.append(team.teamname)
                row.append(calucate_point(team))
                score.append(row)        
    except Exception:
        pass

    return render_to_response("contest/kingofhill/score.html",{'score':score}, context_instance = RequestContext(request))


def submit_flag(request):
    
    if not validate_user(request):
        return access_error(request)

    form = FlagForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cleaned_form_data = form.cleaned_data
            try:
                state_number = get_state_number(cleaned_form_data['service'])
                flag = generate_flag(state_number, cleaned_form_data['service'])

                if flag is not None:
                    if flag == cleaned_form_data['flag']:
                        msg = "You have given a correct flag"
                        if state_number != 0:
                            update_previous_state(state_number - 1, cleaned_form_data['service'])
                        service = get_object_or_404(Service, service_name=cleaned_form_data['service'])
                        team = get_object_or_404(Team, teamname=request.session['teamname'])
                        status = State(state_number=state_number, service=service, teamname=team) 
                        status.save()       
                    else:
                        msg = "Incorrect flag, try again"
            
            except Exception:
                msg = "Wrong flag"

            return render_to_response("contest/kingofhill/flag.html",{'form':form,"msg":msg}, context_instance = RequestContext(request))


    return render_to_response("contest/kingofhill/flag.html",{'form':form}, context_instance = RequestContext(request)) 
 


