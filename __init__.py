'''
Copyright (C) 2023 Sam Clerke
YOUR@MAIL.com

Created by Sam Clerke
Licensed under the MIT License. See LICENSE for details.
'''

bl_info = {
    "name": "Unturned Helper",
    "description": "A set of automations making life easier for Unturned modders.",
    "author": "Sam Clerke",
    "version": (0, 0, 1),
    "blender": (4, 0, 1),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "3D View" }


import bpy


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())



# register
##################################

import traceback

def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))