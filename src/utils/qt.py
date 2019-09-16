import os

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton


def create_button(name) -> QPushButton:
    resources = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "resources"
    )
    pixmap = QPixmap(os.path.join(resources, "{0}.png".format(name)))
    icon = QIcon(pixmap)
    button = QPushButton()
    button.setIcon(icon)
    button.setIconSize(pixmap.rect().size())

    return button
