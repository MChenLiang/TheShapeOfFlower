#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import progress_bar, warning_dlg

reload(progress_bar)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def show_progress(*args, **kwargs):
    progress_bar.show(*args, **kwargs)


def show_warning(txt, key='w'):
    """

    :param txt: in text
    :param key: a: ask, e: error, w: warning
    :return:  dialog.exec_() True or False
    """
    dlg = warning_dlg.warning_ui('MCL_Warning', title=txt, conf=key)
    return dlg.exec_()
