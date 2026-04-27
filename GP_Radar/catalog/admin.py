from django.contrib import admin
from .models import GPPractices, GPDetails, GPPopulations

@admin.register(GPPractices)
class GPPracticesAdmin(admin.ModelAdmin):
    list_display = ('practice_code', 'name', 'list_size', 'health_board', 'postcode', 'telephone')
    list_filter = ('health_board',)
    search_fields = ('name', 'address', 'postcode', 'practice_code')
    ordering = ('name',)
    readonly_fields = ('practice_code',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('practice_code', 'name', 'list_size')
        }),
        ('Contact Information', {
            'fields': ('address', 'postcode', 'telephone')
        }),
        ('Location', {
            'fields': ('health_board', 'latitude', 'longitude')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('practice_code',)
        return self.readonly_fields

@admin.register(GPDetails)
class GPDetailsAdmin(admin.ModelAdmin):
    list_display = ('medical_council_number', 'forename', 'surname', 'sex', 'designation', 'practice')
    list_filter = ('sex', 'designation', 'practice__health_board')
    search_fields = ('forename', 'surname', 'medical_council_number', 'practice__name')
    ordering = ('surname', 'forename')
    readonly_fields = ('medical_council_number',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('medical_council_number', 'forename', 'middle_initial', 'surname', 'sex')
        }),
        ('Professional Information', {
            'fields': ('designation', 'practice')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('medical_council_number',)
        return self.readonly_fields

@admin.register(GPPopulations)
class GPPopulationsAdmin(admin.ModelAdmin):
    list_display = ('practice', 'sex', 'total_population')
    list_filter = ('sex', 'practice__health_board')
    search_fields = ('practice__name',)
    ordering = ('practice', 'sex')
    
    def total_population(self, obj):
        total = (
            obj.ages00to04 + obj.ages05to09 + obj.ages10to14 + obj.ages15to19 +
            obj.ages20to24 + obj.ages25to29 + obj.ages30to34 + obj.ages35to39 +
            obj.ages40to44 + obj.ages45to49 + obj.ages50to54 + obj.ages55to59 +
            obj.ages60to64 + obj.ages65to69 + obj.ages70to74 + obj.ages75to79 +
            obj.ages80to84 + obj.ages85plus
        )
        return f"{total:,}"
    total_population.short_description = 'Total Population'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('practice', 'sex')
        }),
        ('Age Groups (0-44)', {
            'fields': (
                'ages00to04', 'ages05to09', 'ages10to14', 'ages15to19',
                'ages20to24', 'ages25to29', 'ages30to34', 'ages35to39',
                'ages40to44'
            ),
            'classes': ('collapse',)
        }),
        ('Age Groups (45-84)', {
            'fields': (
                'ages45to49', 'ages50to54', 'ages55to59', 'ages60to64',
                'ages65to69', 'ages70to74', 'ages75to79', 'ages80to84'
            ),
            'classes': ('collapse',)
        }),
        ('Age Groups (85+)', {
            'fields': ('ages85plus',),
            'classes': ('collapse',)
        }),
    )

# Customize admin site header
admin.site.site_header = 'GP Radar Administration'
admin.site.site_title = 'GP Radar Admin'
admin.site.index_title = 'Welcome to GP Radar Administration'
