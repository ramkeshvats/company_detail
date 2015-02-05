from django.contrib import admin

from appl.models import Employee, CompanyDetail, OtherBranch, PreCompany

admin.site.register(Employee)
admin.site.register(PreCompany)
admin.site.register(CompanyDetail)
admin.site.register(OtherBranch)
