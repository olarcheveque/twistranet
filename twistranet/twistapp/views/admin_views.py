from django.utils.translation import ugettext as _
from django.template import loader, Context
from twistranet.core.views import BaseView
from twistranet.twistapp.forms.admin_forms import *
from twistranet.twistapp.models import Menu, MenuItem

label_save = _('Save')
label_edit_menuitem = _('Edit menu entry')

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
def get_html_menu_tree(t, menu, level=-1):
    html = ''
    level += 1
    for menuitem in menu.children:
        c = Context ({'iid': menuitem.id, 
                     'level': level,
                     'ilabel': menuitem.label, 
                     'label_edit': label_edit_menuitem,
                     'label_save': label_save,
                     'edit_form' : MenuItemLinkForm(instance=menuitem)
                    })
        html += t.render(c)
        html += get_html_menu_tree(t, menuitem, level)
    return html

class MenuBuilder(BaseView):
    """
    A view used to build all menus
    """
    name = "menu_builder"
    template_variables = BaseView.template_variables + [
        "form",
        "topmenus",
        "mainmenu",
        "links_form"
        ""
    ]
    template = 'admin/menu_builder_form.html'
    title = _("Menu Builder")
    
    def prepare_view(self, *args, **kw):
        self.account = self.auth
        self.actions = None
        self.topmenus = topmenus = Menu.objects.all()
        # start the menu builder for the first menu if exists
        if topmenus:
            t = loader.get_template('admin/menu_item_edit.part.html')
            self.mainmenu = '<ul id="menu-to-edit" class="menu ui-sortable">\n%s\n</ul>' %get_html_menu_tree(t, topmenus[0])
        else:
            self.mainmenu = ''
        self.form = MenuBuilderForm()
        self.links_form = MenuItemLinkForm()

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