# window.py
#
# Copyright 2022 Jordi Chulia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

from .graph_area import GraphArea
from .headerbar_wrapper import HeaderBarWrapper
from .preferences_box import PreferencesBox
from .cpu_monitor_widget import CpuMonitorWidget
from .gpu_monitor_widget import GpuMonitorWidget
from .memory_monitor_widget import MemoryMonitorWidget
from ..monitor_type import MonitorType
from .window_layour_manager import WindowLayoutManager


@Gtk.Template(resource_path='/org/github/jorchube/gpumonitor/gtk/single-window.ui')
class SingleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'SingleWindow'

    _overlay= Gtk.Template.Child()
    _monitors_box= Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout_managet = WindowLayoutManager(self, self._set_horizontal_layout, self._set_vertical_layout)
        self._preferences_box = PreferencesBox(type)

        self._monitor_widgets = [
            CpuMonitorWidget(),
            GpuMonitorWidget(),
            MemoryMonitorWidget(),
        ]

        self._headerbar_wrapper = HeaderBarWrapper(PreferencesBox(MonitorType.CPU))
        self._overlay.add_overlay(self._headerbar_wrapper.root_widget)

        self.connect("close-request", self._close_request)
        self._install_motion_event_controller()

        for widget in self._monitor_widgets:
            self._monitors_box.append(widget)
            widget.start_sampling()

    def _set_horizontal_layout(self):
        self._monitors_box.set_orientation(Gtk.Orientation.HORIZONTAL)

    def _set_vertical_layout(self):
        self._monitors_box.set_orientation(Gtk.Orientation.VERTICAL)

    def _install_motion_event_controller(self):
        controller = Gtk.EventControllerMotion()
        controller.connect("enter", self._on_mouse_enter)
        controller.connect("leave", self._on_mouse_leave)
        self._overlay.add_controller(controller)

    def _on_mouse_enter(self, motion_controller, x, y):
        self._headerbar_wrapper.on_mouse_enter()

    def _on_mouse_leave(self, motion_controller):
        self._headerbar_wrapper.on_mouse_exit()

    def _close_request(self, user_data):
        for widget in self._monitor_widgets:
            widget.stop_sampling()
