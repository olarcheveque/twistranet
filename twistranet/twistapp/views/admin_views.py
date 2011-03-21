from django.utils.translation import ugettext as _
from django.template import loader, Context
from django.core.urlresolvers import reverse
from twistranet.core.views import BaseView
from twistranet.twistapp.views.account_views import HomepageView
from twistranet.twistapp.forms.admin_forms import *
from twistranet.twistapp.models import Menu, MenuItem

label_save = _('Save')
label_edit_menuitem = _('Edit menu entry')
label_delete_menuitem = _('Delete menu entry')
label_cancel = _('Cancel')

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
    initial = {'parent_id' : menu.id}
    for menuitem in menu.children:
        c = Context ({'iid': menuitem.id, 
                     'level': level,
                     'ilabel': menuitem.label, 
                     'label_edit_menuitem': label_edit_menuitem,
                     'label_save': label_save,
                     'label_delete_menuitem': label_delete_menuitem,
                     'label_cancel': label_cancel,
                     'edit_form' : MenuItemLinkForm(instance=menuitem, initial = initial),
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
        "links_form",
        "referer_url",
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
            links_form_initial = {'parent_id': topmenus[0].id}
        else:
            self.mainmenu = ''
            links_form_initial = {}
        self.form = MenuBuilderForm()
        self.links_form = MenuItemLinkForm(initial = links_form_initial)
        referer_path = reverse(HomepageView.name)
        self.referer_url = self.request.build_absolute_uri(referer_path)

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