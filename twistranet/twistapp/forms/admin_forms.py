from django import forms
from twistranet.twistapp.forms.base_forms import BaseForm
from twistranet.twistapp.models import Menu, MenuItem

class MenuBuilderForm(forms.Form):
    """just a basic form to build menus
    """

class MenuForm(BaseForm):
    class Meta:
        model = Menu
        fields = ('title', 'description', )

class MenuItemForm(BaseForm):
    class Meta:
        model = MenuItem