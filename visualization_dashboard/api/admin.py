from django.contrib import admin
from api.models import DataPoint


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = (
        'id','intensity','likelihood','relevance','end_year','country','topic','sector','region','pestle','source',
    )

    list_filter = (
        ('end_year', admin.DateFieldListFilter),  
        'sector',
    )

    search_fields = (
        'title','topic','sector','region','country','source','pestle',
    )

    ordering = ('-end_year', 'intensity', 'likelihood')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title','topic','sector','source',
            ),
            'classes': ('wide',), 
        }),
        ('Analysis Details', {
            'fields': (
                'pestle','intensity','likelihood','relevance',
            ),
            'classes': ('collapse',),  
        }),
        ('Date and Location', {
            'fields': (
                'end_year','country','region',
            ),
            'classes': ('wide',),
        }),
    )

    list_per_page = 20 

    save_on_top = True 
    show_full_result_count = True 

