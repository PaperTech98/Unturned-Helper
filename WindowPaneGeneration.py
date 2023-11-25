import bpy, bmesh
from array import *
import numpy as np

from . import Window

class WindowPaneOperator(bpy.types.Operator):
    bl_idname = "wn.generate_panes"
    bl_label = "Unturned Generate Building Panes"
    
    def execute(self, context):

        if bpy.context.mode != 'EDIT_MESH':
            raise Exception("Oops, you are not in edit mode")

        #initialise mesh
        obj = bpy.context.object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)

        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')

        window_verts = np.empty(0)

        for vert in bm.verts:
            try:
                if not np.isin(vert, window_verts):
                    window = Window.Window(vert)
                    window_verts = np.concatenate((window.get_verts(), window_verts));
                    print('valid window')
                    window.generate_pane(bm)
            except Exception as err:
                #print(err)
                pass
            
        #Actually apply our updates from code
        bmesh.update_edit_mesh(obj.data)
        
# Only needed if you want to add into a dynamic menu.
def menu_func(self, context):
    self.layout.operator(WindowPaneOperator.bl_idname, text="Unturned Generate Building Panes")
    
def register():
    bpy.utils.register_class(WindowPaneOperator)
    
def unregister():
    bpy.utils.unregister_class(WindowPaneOperator)
    
if __name__ == "__main__":
    register()