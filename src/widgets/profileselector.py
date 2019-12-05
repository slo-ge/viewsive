from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox

from utils.config_parser import Profiles
from widgets.config import app_state


class ProfileSelector(QWidget):
    """ defines the layout and append ui element including the cef widget"""

    def __init__(self, profiles: Profiles):
        self.profiles = profiles
        super(ProfileSelector, self).__init__(None)
        layout = QHBoxLayout()
        cb = QComboBox()
        cb.currentIndexChanged.connect(self.selection_change)

        for profile in profiles.profiles:
            cb.addItem(profile.name)

        layout.addWidget(cb)
        self.setLayout(layout)

    @pyqtSlot(int)
    def selection_change(self, index: int):
        print('\n\nSelected Profile: ', index)
        app_state.next_profile(self.profiles.profiles[index])  # $
