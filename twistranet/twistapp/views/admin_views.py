from django.utils.translation import ugettext as _
from twistranet.core.views import BaseView
from twistranet.twistapp.forms.admin_forms import *
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
<li id="menu-item-%(iid)s" 
    class="menu-item menu-item-edit-inactive menu-item-depth-%(level)i">
  <dl class="menu-item-bar">
    <dt class="menu-item-handle">
      <span class="item-title">%(ilabel)s</span>
      <span class="item-controls">
        <span class="item-type"></span>
        <a href="#"
           id="edit-%(iid)s"
           title="%(label_edit)s"
           class="item-edit">&nbsp;</a>
      </span>
    </dt>
  </dl>
  <div id="menu-item-settings-%(iid)s"
       class="menu-item-settings">
  </div>
  <ul class="menu-item-transport"></ul>
</li>''' %{'iid': menuitem.id, 
           'level': level,
           'ilabel': menuitem.label, 
           'label_edit': _('Edit menu entry'),
           }
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
            self.mainmenu = '<ul id="menu-to-edit" class="menu ui-sortable">\n%s\n</ul>' %get_html_menu_tree(topmenus[0])
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