from django.contrib import admin
from .models import Department, City, MemberList

admin.site.register(Department)
admin.site.register(City)
admin.site.register(MemberList)