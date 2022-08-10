from bpy.types import Operator, Context, Object, Mesh, MeshPolygon
import bpy
import bmesh

bl_info = {
    'name': 'Smart Unwrap One Click',
    'blender': (2, 80, 0),
    'category': 'Object',
    'author': 'Zenker'
}


class OSC_OT_unwrap(Operator):
    bl_label: str = 'Smart Unwrap One Click'
    bl_idname: str = 'osc.unwrap'
    bl_options = {'REGISTER'}

    def select(self, obj: Object, select: bool = True):
        for polygon in obj.data.polygons:
            polygon.select = select
        for edge in obj.data.polygons:
            edge.select = select
        for vertex in obj.data.polygons:
            vertex.select = select

    def execute(self, context: Context):
        obj: Object

        for obj in context.selected_objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')

            bpy.ops.uv.smart_project(angle_limit=obj.data.auto_smooth_angle)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}


reg, unreg = bpy.utils.register_classes_factory((
    OSC_OT_unwrap,
))

addon_keymaps = []


def register():
    reg()
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(
            name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            OSC_OT_unwrap.bl_idname, type='U', value='PRESS', shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    unreg()
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == '__main__':
    register()
