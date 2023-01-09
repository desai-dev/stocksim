from django.contrib import admin
from .models import Portfolio
from .models import Cash

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Cash)