from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from django.utils import timezone

class OtherBranch(models.Model):
    baddr = models.TextField()
    bweb = models.CharField(max_length=50)
    bphone = models.IntegerField()

    def __unicode__(self):
        return self.baddr


class CompanyDetail(models.Model):
    c_name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField()
    web = models.CharField(max_length=50)
    phone = models.IntegerField(null=True)
    branch = models.ManyToManyField(OtherBranch, null=True, blank=True)
   
    def __unicode__(self):
        return self.c_name


class PreCompany(models.Model):
    company_name = models.ForeignKey(CompanyDetail, null=True, blank=True)
    pre_desination = models.CharField(max_length=20, null=True, blank=True)
    leaving_date = models.DateTimeField(default=datetime.now, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.company_name or ' ')


class Employee(models.Model):
    name = models.CharField(max_length=20)
    user = models.OneToOneField(User, null=True)
    desination = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    current_Company = models.ForeignKey(CompanyDetail, null=True, blank=True)
    confermPassword = models.CharField(max_length=10, null=True)
    preCompany = models.ManyToManyField(PreCompany, null=True, blank=True)

    def __unicode__(self):
        return self.name
