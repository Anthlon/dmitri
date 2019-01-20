from django.contrib import admin
from .models import FeedbackModel, DefenderModel


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('date_time_post', 'user', 'member', 'content')
    list_display_links = ('date_time_post', 'user', 'member')
    list_filter = ('user', 'member')
    date_hierarchy = 'date_time_post'
    list_per_page = 10
    list_max_show_all = 15

    fieldsets = (
        ('Клиент', {'fields': (('user', 'member'),)},),
        ('Заявка', {'fields': (('name',), ('email', 'phone_number', 'preferred'), ('content',))},),
    )


admin.site.register(FeedbackModel, FeedbackAdmin)


class DefenderModelAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'excess', 'banned_dt', 'counter', 'total_counter')


admin.site.register(DefenderModel, DefenderModelAdmin)
