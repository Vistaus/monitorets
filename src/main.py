# main.py
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import MonitorWindow
from .samplers.gpu_sampler import GpuSampler
from .samplers.cpu_sampler import CpuSampler
from .samplers.memory_sampler import MemorySampler


class MonitorApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.github.jorchube.gpumonitor',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.on_quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """

        self._cpu_sampler = CpuSampler()
        cpu_window = MonitorWindow("CPU", self._cpu_sampler, application=self)

        self._gpu_sampler = GpuSampler("/sys/class/drm/card0/device/gpu_busy_percent")
        gpu_window = MonitorWindow("GPU", self._gpu_sampler, application=self)

        self._memory_sampler = MemorySampler()
        memory_window = MonitorWindow("Memory", self._memory_sampler, application=self)

        cpu_window.present()
        gpu_window.present()
        memory_window.present()

        self._windows = [cpu_window, gpu_window, memory_window]

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='gpumonitor',
                                application_icon='org.github.jorchube.gpumonitor',
                                developer_name='Jordi Chulia',
                                version='0.1.0',
                                developers=['Jordi Chulia'],
                                copyright='© 2022 Jordi Chulia')
        about.present()

    def on_quit(self, *args, **kwargs):
        for window in self._windows:
            window.close()

        self.quit()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = MonitorApplication()
    return app.run(sys.argv)
