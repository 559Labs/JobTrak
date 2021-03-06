from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator
from django.utils.translation import ugettext, ugettext_lazy
from pprint import pprint
from django.contrib.humanize.templatetags.humanize import naturaltime, ordinal, intcomma, naturalday
from mmg.jobtrak.core.models import *

class Country(models.Model):
    """Model for countries"""
    iso_code=models.CharField(
        max_length=2,
        primary_key=True,
        verbose_name=ugettext_lazy('ISO Code'))
    name=models.CharField(
        max_length=45,
        blank=False,
        verbose_name=ugettext_lazy('Name'))
    class Meta:
        verbose_name=ugettext_lazy("Country")
        verbose_name_plural=ugettext_lazy("Countries")
        ordering=["name", "iso_code"]
    def __unicode__(self):
        return self.name

class Address(models.Model):
    """Model to store addresses for accounts"""
    address_line1=models.CharField(
        verbose_name=ugettext_lazy("Address Line 1"),
        max_length=45)
    address_line2=models.CharField(
        verbose_name=ugettext_lazy("Address line 2"),
        max_length=45,
        blank=True)
    city=models.CharField(
        max_length=50,
        blank=False,
        verbose_name=ugettext_lazy("City"))
    state_province=models.CharField(
        max_length=40,
        blank=True,
        verbose_name=ugettext_lazy("State/Province"))
    country=models.ForeignKey(
        Country, blank=False)
    postal_code=models.CharField(
        max_length=10,
        blank=True,
        verbose_name=ugettext_lazy("Postal Code"))
    class Meta:
        verbose_name=ugettext_lazy("Address")
        verbose_name_plural=ugettext_lazy("Addresses")
        unique_together=("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")
    def __unicode__(self):
        return "%s, %s, %s %s" % (self.address_line1, self.city, self.state_province,
                              str(self.country))

class CompanyType(models.Model):
    """CompanyType - defines company classifications"""
    id=models.AutoField(primary_key=True)
    name=models.CharField(
        max_length=64,
        verbose_name=ugettext_lazy("Name"))
    class Meta:
        verbose_name=ugettext_lazy('Company Type')
        verbose_name_plural=ugettext_lazy('Company Types')
    def __unicode__(self):
        return self.name


class Company(models.Model):
    """(Modelname description)"""
    id=models.AutoField(primary_key=True)
    name=models.CharField(
        max_length=128,
        verbose_name=ugettext_lazy("Name"))
    note=models.TextField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy("Note"))
    company_type=models.ForeignKey(
        CompanyType,
        blank=True,
        null=True)
    class Meta:
        verbose_name=ugettext_lazy('Company')
        verbose_name_plural=ugettext_lazy('Companies')
    def __unicode__(self):
        return self.name

class CompanyLocation(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(
        max_length=128,
        verbose_name=ugettext_lazy("Name"))
    company=models.ForeignKey('Company', null=True)
    address=models.ForeignKey('Address', null=True, blank=True)
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    office_tel=models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        verbose_name=ugettext_lazy("Office Phone"))
    office_fax=models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        verbose_name=ugettext_lazy("Office Fax"))
    note=models.TextField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy("Note"))
    class Meta:
        verbose_name=ugettext_lazy('Company Location')
        verbose_name_plural=ugettext_lazy('Company Locations')
    def __unicode__(self):
        return ' - '.join([self.company.name,self.name])

class ContactType(models.Model):
    """(Modelname description)"""
    id=models.AutoField(primary_key=True)
    name=models.CharField(
        max_length=128,
        verbose_name=ugettext_lazy("Name"))
    class Meta:
        verbose_name=ugettext_lazy('Contact Type')
        verbose_name_plural=ugettext_lazy('Contact Types')
    def __unicode__(self):
        return self.name

class Contact(models.Model):
    """(Modelname description)"""
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(
        max_length=128,
        verbose_name=ugettext_lazy("First Name"))
    last_name=models.CharField(
        max_length=128,
        verbose_name=ugettext_lazy('Last Name'))
    contact_type=models.ForeignKey('ContactType')
    title=models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy("Title"))
    company=models.ForeignKey(CompanyLocation, blank=True, null=True)
    email_address=models.EmailField(
        blank=True,
        verbose_name=ugettext_lazy("E-Mail Address"))
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    office_tel=models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        verbose_name=ugettext_lazy("Office Phone"))
    mobile_tel=models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        verbose_name=ugettext_lazy("Mobile Phone"))
    office_fax=models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        verbose_name=ugettext_lazy("Office Fax"))
    birthday=models.DateField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy("Birthday"))
    note=models.TextField(
        blank=True,
        verbose_name=ugettext_lazy("Note"))
    class Meta:
        verbose_name=ugettext_lazy('Contact')
        verbose_name_plural=ugettext_lazy('Contacts')
    def get_name_lastfirst(self):
        return ', '.join([self.last_name,self.first_name])
    get_name_lastfirst.short_description=ugettext_lazy('Full Name')

    def get_name_firstlast(self):
        return ' '.join([self.first_name,self.last_name])
    get_name_firstlast.short_description=ugettext_lazy('Full Name')

    def get_last_contact(self):
        return 0
    #     try:
    #         # TODO Fix this bug. It won't collect the latest
    #    hist=ActionHistory.objects.filter(who__exact=self)
    #    rv=hist.latest()
    #    return rv
    #    except DoesNotExist:
    #        rv=None
    #    except MultipleObjectsReturned:
    #        rv=None
    #    except:
    #        rv=None
    #    return None
    get_last_contact.short_description=ugettext_lazy('Last Contact')

    def __unicode__(self):
        # return ' '.join([self.company.company.name, u'-', self.company.name, u'-',self.first_name, self.last_name])
        return "{} {} / {}".format(self.first_name, self.last_name, self.title)
