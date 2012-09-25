from django.db import models
from register.models import Team


class Service(models.Model):

    """
    The in king of the hill task will be divided into different levels, each level \
    will have its own services 

    eg:
    
    first level service :
    1) www
    2) service

    second level service:
    1) AD

    The team who capture the flag of the second service and hold it for max time \
    will be the king

    """

    service_name = models.CharField(unique=True, max_length=200, blank=False)
    level = models.IntegerField(blank=False)

    class Meta:
        db_table = 'inctf_service'

    def __unicode__(self):
        return self.service_name

    def get_absolute_url(self):
        return "/kingofhill/%s" % self.service_name


class State(models.Model):

    """
    Each service changes its state ( new flag is planted) once a team captures its \
    flag. Once a team captures a flag, points will be awarded to the that team \
    until another team capture the flag for that service. 
    State no is also important for generating the flag. State of the service for which \
    the flag is captured will be saved

    """

    state_number = models.IntegerField(max_length=8, blank=False)
    service = models.ForeignKey(Service)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    teamname = models.ForeignKey(Team)

    class Meta:
        db_table = 'inctf_servicestate'
    
    def __unicode__(self):
        return self.state_number

    
