from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django import forms

from .models import Agency, Project, ProfitLossAccount, ProjectAlert, AccountingCode


class AgencyAdmin(admin.ModelAdmin):
    search_fields = ['name',]


class AccountingCodeAdmin(admin.ModelAdmin):
    search_fields = ['agency__name', 'office',]

class ProfitLossAccountForm(forms.ModelForm):
    class Meta:
        model = ProfitLossAccount
        exclude = []
    def clean(self):
        if self.cleaned_data.get(
            'as_start_date'
        ) > self.cleaned_data.get(
            'as_end_date'
        ):
            raise forms.ValidationError(
                'Start date cannot occur before the end date.'
            )
        return self.cleaned_data

class ProfitLossAccountAdmin(admin.ModelAdmin):
    form = ProfitLossAccountForm
    search_fields = ['name',]

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = []
    def clean(self):
        if 'profit_loss_account' in self.cleaned_data:
            if self.cleaned_data['start_date']:
                if self.cleaned_data['start_date'] < \
                self.cleaned_data['profit_loss_account'].as_start_date:
                    raise forms.ValidationError(
                        'Profit/Loss accounting string will not be active '\
                        'until {}. Please select an profit/loss accounting '\
                        'string that is will be active on or before the start '\
                        'date of this project.'\
                        .format(
                            self.cleaned_data['profit_loss_account'].as_start_date
                        )
                    )
            if self.cleaned_data['profit_loss_account'].account_type == \
            'Expense':
                raise forms.ValidationError(
                    'You have assigned the {} profit/loss '\
                    'accounting information to {}. The accounting information '\
                    'type is {}, which is cannot be assigned to a '\
                    'project. Only accounting information that is of the'\
                    'Revenue type may be assigned to a project.'.format(
                        self.cleaned_data['profit_loss_account'],
                        self.cleaned_data['name'],
                        self.cleaned_data['profit_loss_account'].account_type
                    )
                )
        return self.cleaned_data

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    search_fields = ['name',]
    fields = [
        'name',
        'mbnumber',
        'accounting_code',
        'profit_loss_account',
        'project_lead',
        'start_date',
        'end_date',
        'active',
        'agreement_URL',
        'description',
        'alerts',
        'notes_required',
        'notes_displayed',
    ]

class ProjectAlertAdmin(admin.ModelAdmin):
    search_fields = ['title',]


admin.site.register(Agency, AgencyAdmin)
admin.site.register(AccountingCode, AccountingCodeAdmin)
admin.site.register(ProfitLossAccount, ProfitLossAccountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAlert, ProjectAlertAdmin)
