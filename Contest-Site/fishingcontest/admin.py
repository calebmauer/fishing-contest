from django.contrib import admin
from fishingcontest.models import Contestant, Fish 

# Register your models here.
class FishInline(admin.TabularInline):
    model = Fish
    extra = 1

class ContestantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name',
                                         'middle_name',
                                         'last_name',
                                         'gender',
                                         'age']}),
        ]
    inlines = [FishInline]
    list_per_page = 600 # default number of rows per page
    ordering = ('last_name',) # Order by last name ascending
	
admin.site.register(Contestant, ContestantAdmin)
#admin.site.register(Fish)
