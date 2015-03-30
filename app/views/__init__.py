# Automatically import all sub packages in this directory
import pkgutil
import sys

package = sys.modules[__name__]
for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
    pkgutil.importlib.import_module(__name__ + '.' + name)