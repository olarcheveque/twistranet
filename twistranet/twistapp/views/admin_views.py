from django.utils.translation import ugettext as _
from twistranet.core.views import BaseView
from twistranet.twistapp.forms.admin_forms import MenuBuilderForm
from twistranet.twistapp.models import Menu, MenuItem 

class MenuBuilder(BaseView):
    """
    A view used to browse and upload resources
    Used by wysiwyg editors
    Based on resource field
    """
    name = "menu_builder"
    template_variables = BaseView.template_variables + [
        "form",
        "menus",
    ]
    template = 'admin/menu_builder_form.html'
    title = _("Menu Builder")
    
    
    def prepare_view(self,):
        self.account = self.auth
        self.actions = None
        self.menus = Menu.objects.all()
        self.form = MenuBuilderForm()