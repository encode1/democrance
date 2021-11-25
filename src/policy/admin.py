from django.contrib import admin
from .models import Coverage, AgePremiumDifferential, Policy, PolicyHistory

class CoverageAdmin(admin.ModelAdmin):
    list_display = ('title','premium', 'cover')
    prepopulated_fields = {'type': ('title',)}


class AgePremiumDifferentialAdmin(admin.ModelAdmin):
    list_display = ('coverage', 'start_age', 'end_age', 'amount')


class PolicyAdmin(admin.ModelAdmin):
    list_display = ('customer', 'coverage', 'state', 'premium', 'cover')


class PolicyHistoryAdmin(admin.ModelAdmin):
    list_display = ('policy', 'state', 'created')
admin.site.register(Coverage, CoverageAdmin)
admin.site.register(AgePremiumDifferential, AgePremiumDifferentialAdmin)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(PolicyHistory, PolicyHistoryAdmin)
