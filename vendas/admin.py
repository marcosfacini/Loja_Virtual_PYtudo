from django.contrib import admin
from .models import ListaDesejo, Venda, ItemVenda, CupomDesconto, HistoricoCupomDesconto

admin.site.register(ListaDesejo)
admin.site.register(Venda)
admin.site.register(ItemVenda)
admin.site.register(CupomDesconto)
admin.site.register(HistoricoCupomDesconto)

