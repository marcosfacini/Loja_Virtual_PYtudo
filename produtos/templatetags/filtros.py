from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.filter
def get_item(dictionary, key):
    string = str(key)
    return dictionary.get(string)

@register.filter
def multiply_item(amount, unity_price):
    return amount * unity_price 

@register.filter
def get_cupom_type(dictionary, key):
    if dictionary[str(key)][1] == 'P':
        return f'- {dictionary[str(key)][0]} %'
    elif dictionary[str(key)][1] == 'R':
        return f'- R$ {dictionary[str(key)][0]}'