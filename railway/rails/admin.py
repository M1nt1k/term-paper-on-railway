from django.contrib import admin

from .models import *
from user.models import User

class TrainAdmin(admin.ModelAdmin):
    list_display = ('id','name','start_city','end_city','start_time','end_time')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Train, TrainAdmin)
admin.site.register(Ticket)
admin.site.register(City)
admin.site.register(Carriage)
admin.site.register(Places)
admin.site.register(User)

