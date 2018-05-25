#!/usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import sys
import time
import pg_conf

import progress_bar, warning_dlg

reload(progress_bar)

from functools import partial


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def show_progress(*args, **kwargs):
    progress_bar.show(*args, **kwargs)



from PyQt4.QtCore import *
from PyQt4.QtGui import *

class t_ui(QWidget):
    def __init__(self):
        super(t_ui, self).__init__()
        self.pt = QPushButton("clicked", parent=self)
        self.pt.clicked.connect(partial(show_progress, "txt_", None, self.txt_pro))

    def txt_pro(self):
        pg_conf.progress_title = 'Start'
        for i in range(101):
            time.sleep(0.1)
            pg_conf.progress_current_val = i
            pg_conf.progress_label = "Had Finished {}%!!".format(i)


# def main():
if __name__ == '__main__':
    app = QApplication([])
    Form = t_ui()
    Form.show()
    sys.exit(app.exec_())
