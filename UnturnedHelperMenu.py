import bpy

class unturnedHelperMenu(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_label = "Unturned"
    bl_category = "Unturned"

    bl_idname = "EDIT_PT_unturnedHelperMenu"

    def draw(self, context):
        row = self.layout.row()
        row.operator("wn.generate_panes", text="Generate Window Panes")
        
def register():
    bpy.utils.register_class(unturnedHelperMenu)
    #bpy.ops.wm.call_menu(name=unturnedMenu.bl_idname)
    
def unregister():
    bpy.utils.unregister_class(unturnedHelperMenu)

if __name__ == "__main__":
    register()