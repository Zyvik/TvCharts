from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def pagination_with_vars(context, **kwargs):
    queryset = context['request'].GET.copy()
    queryset['page'] = kwargs['page']
    return queryset.urlencode()
