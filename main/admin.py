from django.contrib import admin
import datetime
from .models import AdvUser, SubRubric, SuperRubric, Bb, AdditionalImage, Comment, Stars, Rating
from .utilities import send_activation_notification
from .forms import SubRubricForm

def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')

send_activation_notifications = 'Отправка писем с требованием активации'

class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return(
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'image', 'email'), ('first_name', 'last_name'), ('is_staff', 'is_superuser'), 'groups', 'user_permissions', ('last_login', 'date_joined'), 'is_activated')
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)

admin.site.register(AdvUser, AdvUserAdmin)

class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

admin.site.register(SuperRubric, SuperRubricAdmin)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm

admin.site.register(SubRubric, SubRubricAdmin)

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage



class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', ('delivery1', 'comment1'), ('delivery2', 'comment2'), ('delivery3', 'comment3'),('money', 'сashless', 'invoce', 'visa', 'mastercard'), 'city', 'street', 'image', 'is_active')
    inlines = (AdditionalImageInline,)

admin.site.register(Bb, BbAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('bb', 'author', 'content', 'star', 'user')
    fields = ('bb', 'author', 'content', 'star', 'user')
admin.site.register(Comment, CommentAdmin)


class StarsAdmin(admin.ModelAdmin):
    list_display = ('star',)
admin.site.register(Stars, StarsAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('login', 'star', 'user')
    fields = ('login', 'star', 'user')
admin.site.register(Rating, RatingAdmin)
