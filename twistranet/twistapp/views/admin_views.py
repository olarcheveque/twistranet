from django.utils.translation import ugettext as _
from twistranet.core.views import BaseView
from twistranet.twistapp.forms.admin_forms import MenuBuilderForm, MenuForm, MenuItemForm
from twistranet.twistapp.models import Menu, MenuItem 

# used for menu_builder json calls
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

# used for menu_builder html calls
def get_html_menu_tree(menu, level=-1):
    html = ''
    level += 1
    for menuitem in menu.children:
        html += '''
<li id="menu-item-%s" class="menu-item menu-item-edit-inactive menu-item-depth-%i">
  <dl class="menu-item-bar">
    <dt class="menu-item-handle">
      <span class="item-title">%s</span>
    </dt>
  </dl>
  <ul class="menu-item-transport"></ul>
</li>
                ''' %(menuitem.id, level, menuitem.label)
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
        self.account = self.auth
        self.actions = None
        self.topmenus = topmenus = Menu.objects.all()
        # start the menu builder for the first menu if exists
        if topmenus:
            self.mainmenu = '<ul id="menu-to-edit" class="menu ui-sortable">\n%s\n</ul>' %get_html_menu_tree(topmenus[0])
        else:
            self.mainmenu = ''
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
        self.account = self.auth
        self.actions = None
        self.form = MenuItemForm()

class MenuItemCreate(MenuItemEdit):
    """
    A view used to create a menuitem
    """
    name = "menu_item_create"
    title = _("MenuItem Create")