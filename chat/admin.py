from django.contrib import admin
from django.apps import apps

# Register your models here.
class MyModelAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        return tuple(i.name for i in self.model._meta.get_fields() if not i.is_relation)

    def get_search_fields(self, reques):
        return tuple(i.name for i in self.model._meta.get_fields() if not i.is_relation)


apps_ = apps.get_app_config('chat').get_models()
for i in apps_:
    try:
        admin.site.register(i,MyModelAdmin)
    except AlreadyRegistered:
        continue

