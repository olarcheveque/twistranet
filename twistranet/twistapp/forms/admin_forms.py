from django.utils.translation import ugettext as _
from django import forms
from django.forms import widgets
from django.forms import fields
from twistranet.twistapp.forms.base_forms import BaseForm
from twistranet.twistapp.models import Menu, MenuItem

class MenuBuilderForm(forms.Form):
    """just a basic form to build menus
    """

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('title', 'description', )

class MenuItemForm(forms.ModelForm):

    title = fields.CharField(
        required = True,
        label = _("Title"),
        help_text = _("Enter the item's title as you want it to be displayed in menu."),
    )

    description = fields.CharField(
        label = _("Description"),
        required = False,
        help_text = _("Enter the item's description as you want it to be displayed on mouse over menu item's."),
        widget = widgets.Textarea(attrs = {'class': 'menu-description-field', 'rows':'2', 'cols': ''}),
    )

    class Meta:
        model = MenuItem
        fields = ('title', 'description' )

class MenuItemLinkForm(MenuItemForm):

    link_url = forms.URLField(
        label = "URL",
        help_text = _("Enter the custom link's url."),
        required = True,
        )
    class Meta:
        model = MenuItem
        fields = ('title', 'description', 'link_url')

class MenuItemContentForm(MenuItemForm):
    """a search form for a target (community or anything else)
       list all communities, with a search filter"""
    title = fields.CharField(
        required = False,
        label = _("Title"),
        help_text = _("Enter the item's title as you want it to be displayed in menu. Leave it blank if you want to keep the target title."),
    )

    description = fields.CharField(
        label = _("Description"),
        help_text = _("Enter the item's description as you want it to be displayed on mouse over menu item's. Leave it blank if you want to keep the target description."),
        widget = widgets.Textarea(attrs = {'class': 'menu-description-field', 'rows':'2', 'cols': ''}),
    )

    target_id = forms.IntegerField(required = True, widget = widgets.HiddenInput)

    class Meta:
        model = MenuItem
        fields = ('title', 'description', 'target_id' )

class MenuItemViewForm(MenuItemForm):

    view_path = forms.URLField(
        label = "View Path",
        help_text = _("Enter the internal view path."),
        required = True,
        )
    class Meta:
        model = MenuItem
        fields = ('title', 'description', 'view_path')