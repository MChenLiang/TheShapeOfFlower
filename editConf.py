#!/usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'miaochenliang'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
from __init__ import __start_path__
import ConfigParser
import baseEnv

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
__abs_path__ = __start_path__


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class conf(object):
    _in_path = os.path.join(__abs_path__, 'configuration.ini').replace('\\', '/')

    def __init__(self):
        self.cf = ConfigParser.ConfigParser()

    def get(self, field, key):
        try:
            self.cf.read(self._in_path)
            result = self.cf.get(field, key)
        except:
            result = ""

        return result

    def set(self, filed, key, value):
        try:
            self.cf.set(filed, key, value)
            self.cf.write(open(self._in_path, 'w'))
        except ConfigParser.NoSectionError:
            self.add(filed, key, value)
        except:
            return False
        return True

    def add(self, filed, key, value):
        self.cf.add_section(filed)
        self.set(filed, key, value)


def _init_conf(cf):
    cf.set(baseEnv.configuration, baseEnv.name, 'succulentPlants')
    cf.set(baseEnv.configuration, baseEnv.version, '1.0')
    cf.set(baseEnv.configuration, baseEnv.alphabet, map(chr, range(65, 91)))
    cf.set(baseEnv.configuration, baseEnv.path, os.path.dirname(__file__))


def _init_qss(cf):
    value = """
QPushButton{
    border-style: outset;    
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
    stop:0.45 rgb(0, 170, 200, 50), 
    stop:0.49 rgb(100, 100, 100)
    stop:0.5 rgba(255, 255, 255, 0));
    background: transparent;
}

QPushButton:hover{
    background-color :qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
    stop:0.45 #09bb07, 
    stop:0.49 rgb(100, 100, 100)
    stop:0.5 rgba(255, 255, 255, 0));
}

QPushButton:checked{
    background-color:qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, 
    stop:0.45  #09cc07,
    stop:0.49 rgb(100, 100, 100)
    stop:0.5 rgba(255, 255, 255, 0));
}
    """
    menuVal = """
QMenu{background:purple;
    border:1px solid lightgray;
    border-color:green;
}
QMenu::item{padding:0px 40px 0px 20px;
    height:30px;
    color:blue;
    background:white;
    margin:1px 0px 0px 0px;
}

QMenu::item:selected:enabled{background:lightgray;
    color:white;
}
QMenu::item:selected:!enabled{background:transparent;}

QMenu::separator{height:50px;
    width:1px;
    background:white;
    margin:1px 1px 1px 1px;
}

QMenu#menu{background:white;
    border:1px solid lightgray;
}
QMenu#menu::item{padding:0px 40px 0px 30px;
    height:25px;
}
QMenu#menu::item:selected:enabled{background:lightgray;
    color:white;
}
QMenu#menu::item:selected:!enabled{background:transparent;}

QMenu#menu::separator{height:1px;
    background:lightgray;
    margin:2px 0px 2px 0px;
}
QMenu#menu::indicator {padding:10px;}
    """
    cf.set('qss', 'pushbutton', value)
    cf.set('qss', 'menu', menuVal)


def _main():
    cf = conf()
    _init_conf(cf)
    _init_qss(cf)


if __name__ == '__main__':
    # fire.Fire(conf)
    _main()
