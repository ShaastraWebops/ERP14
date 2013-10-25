from django.contrib import admin
from events.models import ParticipantEvent, AudienceEvent, GenericEvent, Tab

admin.site.register(Tab)
admin.site.register(GenericEvent)
admin.site.register(ParticipantEvent)
admin.site.register(AudienceEvent)
