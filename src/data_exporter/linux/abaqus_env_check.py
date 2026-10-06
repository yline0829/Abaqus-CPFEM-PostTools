# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

print("Abaqus Python executable:")
print(sys.executable)
print("")
print("Abaqus Python version:")
print(sys.version)
print("")

try:
    from odbAccess import openOdb
    print("odbAccess: OK")
except Exception as exc:
    print("odbAccess: FAILED")
    print("%s: %s" % (exc.__class__.__name__, exc))
    sys.exit(2)

try:
    import abaqusConstants
    print("abaqusConstants: OK")
except Exception as exc:
    print("abaqusConstants: WARNING")
    print("%s: %s" % (exc.__class__.__name__, exc))

print("")
print("Environment check: PASS")
