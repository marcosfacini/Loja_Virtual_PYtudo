from django.contrib import admin
from .models import ListaDesejo, CupomDesconto, HistoricoCupomDesconto

admin.site.register(ListaDesejo)
admin.site.register(CupomDesconto)
admin.site.register(HistoricoCupomDesconto)

