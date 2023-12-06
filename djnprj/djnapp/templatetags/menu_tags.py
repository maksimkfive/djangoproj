from django import template
from ..models import MenuItem

register = template.Library()

def build_menu_tree(queryset, current_url, parent=None, level=-1):
    tree = []
    for item in queryset:
        if item.parent == parent:
            new_item = item
            new_item.level = level + 1
            new_item.is_active = current_url.startswith(item.get_absolute_url())
            new_item.children = build_menu_tree(queryset, current_url, parent=item, level=new_item.level)
            tree.append(new_item)
    return tree

@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    all_items = MenuItem.objects.filter(menu_name=menu_name)
    menu_tree = build_menu_tree(all_items, request.path)
    return {'menu_items': menu_tree}
