from django.contrib import admin
from django.apps import apps
from graphql_jwt.refresh_token.models import RefreshToken
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Category, Image


class MyAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


admin.site.register(Category, MyAdmin)
models = apps.get_models()

for model in models:
    if model == RefreshToken:
        continue
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
