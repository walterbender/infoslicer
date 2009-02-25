# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
from gettext import gettext as _

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.activity.activity import ActivityToolbox

from GUI_Components.Edit_Pane import Edit_Pane
from GUI_Components.Format_Pane import Format_Pane
from GUI_Components.Image_Pane import Image_Pane

TABS = (Edit_Pane(),
        Image_Pane(),
        Format_Pane())

class View(gtk.Notebook):
    def __init__(self):
        gtk.Notebook.__init__(self)
        self.props.show_border = False
        self.props.show_tabs = False

        for i in TABS:
            self.append_page(i)
            i.show()

class Toolbar(gtk.Toolbar):
    def __init__(self, edit):
        gtk.Toolbar.__init__(self)
        self.edit = edit

        txt_toggle = ToggleToolButton('ascii')
        img_toggle = ToggleToolButton('image')

        txt_toggle.show()
        txt_toggle.set_tooltip(_('Text'))
        txt_toggle.connect('toggled', self._toggle_cb, [txt_toggle, img_toggle])
        self.insert(txt_toggle, -1)

        img_toggle.show()
        img_toggle.set_tooltip(_('Images'))
        img_toggle.connect('toggled', self._toggle_cb, [txt_toggle, img_toggle])
        self.insert(img_toggle, -1)

        separator = gtk.SeparatorToolItem()
        self.insert(separator, -1)
        separator.show()

        for tab in TABS:
            for i in tab.toolitems:
                self.insert(i, -1)

    def _toggle_cb(self, widget, toggles):
        for tab in TABS:
            for i in tab.toolitems:
                i.hide()

        if not widget.get_active():
            index = 2
        else:
            another = toggles[0] == widget and 1 or 0
            toggles[another].set_active(False)
            toggles[another].stop_emission('toggled')
            index = int(not another)

        for i in TABS[index].toolitems:
            i.show()
        self.edit.set_current_page(index)
