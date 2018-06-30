#!/usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import psutil
import win32con
import win32gui
import win32api

__all_ui__ = set()
__find_ui__ = str()


def foo(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        __all_ui__.add(hwnd)


def find_window(cla_name, win_t):
    win32gui.EnumWindows(foo, 0)
    for hwnd in __all_ui__:
        if cla_name == win32gui.GetClassName(hwnd) and win_t == win32gui.GetWindowText(hwnd).decode('GB2312'):
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            break


def delete_ui(cla_name, win_t):
    find_ui.find_window(cla_name, win_t)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def get_all_process():
    return {each.name(): each.pid for each in psutil.process_iter()}


def conf_CGTm():
    CGTm = 'CgTeamWork.exe'
    classname = "CgTeamWork"

    all_process = get_all_process()

    # for k, v in all_process.items():
    #     print k, '\t : \t', v

    if CGTm not in all_process.keys():
        return 0
    #
    win = win32gui.FindWindow(None, classname)
    if not win:
        return 0
    return 1

if __name__ == '__main__':
    conf_CGTm()
#     find_window('QWidget', 'VHQLauncher')
# for each in __all_ui__:
#     print each
