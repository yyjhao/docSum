#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

for line in sys.stdin:
    l = "\"".join(line.split("''"))
    l = "\"".join(l.split("”"))
    l = "\"".join(l.split("“"))
    l = "'".join(l.split("‘"))
    l = "'".join(l.split("’"))
    print l
