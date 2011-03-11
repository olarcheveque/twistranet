from django.utils.translation import ugettext as _
from twistranet.core.views import BaseView
from twistranet.twistapp.forms.admin_forms import MenuBuilderForm, MenuForm, MenuItemForm
from twistranet.twistapp.models import Menu, MenuItem 

# used for json calls
def get_menu_tree(menu=None):
    tree = []
    if menu is None:
        menus = Menu.objects.all()
    else:
        menus = menu.children
    for m in menus:
        item = {}
        item['id'] = m.id
        item['title'] = m.label
        item['children'] = get_menu_tree(m)
        tree.append(m)
    return tree

# used for first html call
def get_html_menu_tree(menu, level=0):
    html = ''
    level += 1
    for menuitem in menu.children:
        html += '<div id="menu-item-%s" class="menu-item-level_%i">%s</div>' %(menuitem.id, level, menuitem.label)
        html += get_html_menu_tree(menuitem, level)
    return html

class MenuBuilder(BaseView):
    """
    A view used to build all menus
    """
    name = "menu_builder"
    template_variables = BaseView.template_variables + [
        "form",
        "topmenus",
        "mainmenu"
    ]
    template = 'admin/menu_builder_form.html'
    title = _("Menu Builder")
    
    def prepare_view(self, *args, **kw):
        super(MenuBuilder, self).prepare_view(*args, **kw)
        self.account = self.auth
        self.actions = None
        self.topmenus = topmenus = Menu.objects.all()
        self.mainmenu = get_html_menu_tree(topmenus[0])
        self.form = MenuBuilderForm()

class MenuEdit(BaseView):
    """
    A view used to edit a menu
    """
    name = "menu_edit"
    template_variables = BaseView.template_variables + [
        "form",
    ]
    template = 'admin/menu_edit.html'
    title = _("Menu Edit")
    
    
    def prepare_view(self, *args, **kw):
        super(MenuEdit, self).prepare_view(*args, **kw)
        self.account = self.auth
        self.actions = None
        self.form = MenuForm()

class MenuCreate(MenuEdit):
    """
    A view used to create a menu
    """
    name = "menu_create"
    title = _("Menu Create")

class MenuItemEdit(BaseView):
    """
    A view used to edit a menuitem
    """
    name = "menu_item_edit"
    template_variables = BaseView.template_variables + [
        "form",
    ]
    template = 'admin/menu_item_edit.html'
    title = _("MenuItem Edit")
    
    
    def prepare_view(self, *args, **kw):
        super(MenuItemEdit, self).prepare_view(*args, **kw)
        self.account = self.auth
        self.actions = None
        self.form = MenuItemForm()

class MenuItemCreate(MenuItemEdit):
    """
    A view used to create a menuitem
    """
    name = "menu_item_create"
    title = _("MenuItem Create")