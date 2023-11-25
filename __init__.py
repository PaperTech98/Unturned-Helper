'''
Copyright (C) 2023 Sam Clerke

Created by Sam Clerke
Licensed under the MIT License. See LICENSE for details.
'''

bl_info = {
    "name": "Unturned Helper",
    "description": "A set of automations making life easier for Unturned modders.",
    "author": "Sam Clerke",
    "version": (0, 0, 2),
    "blender": (4, 0, 1),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "3D View" }


modulesNames = ['UnturnedHelperMenu', 'WindowPaneGeneration'] 
import sys
import importlib

modulesFullNames = {}
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

if __name__ == "__main__":
    register()