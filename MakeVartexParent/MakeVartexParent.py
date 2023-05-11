# 基本情報
bl_info = {
    "name": "Make Vertex Parent",
    "author": "moteki",
    "version": (0, 0, 6),
    "blender": (3, 0, 0),
    "location": "3D View",
    "support": "TESTING",
    "category": "Mesh",
}

# ライブラリインポート
import bpy
import bmesh
from bpy.types import Panel,Operator
from mathutils import Vector

# メニューに実行ボタン追加するための関数
def menu_MakeVertexParent(self, context):
   self.layout.separator()
   #第一引数は実行機能クラスのbl_idname、textは間違えないようにあえてSaruと書いた
   self.layout.operator(MakeVertexParent_operator.bl_idname, text="AAA")

# サイドバーに実行ボタンを追加するためのクラス
class MakeVertexParent_Panel(Panel):
    bl_label = "Make Vertex Parent"
    bl_idname = "MAKE_VERTEX_PARENT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Item'

    '''empty_type: bpy.props.EnumProperty(
        name="Empty Type",
        items=[
            ('ARROWS', "Arrows", ""),
            ('PLAIN_AXES', "Plain Axes", ""),
            ('SINGLE_ARROW', "Single Arrow", ""),
            ('CUBE', "Cube", ""),
            ('SPHERE', "Sphere", ""),
            ('CONE', "Cone", ""),
            ('IMAGE', "Image", ""),
            ('CIRCLE', "Circle", ""),
        ],
        default='PLAIN_AXES',
    )'''

    '''empty_size: bpy.props.FloatProperty(
        name="Empty Size",
        description="Size of the Empty",
        default=1.0,
        min=0.0001,
        soft_max=10,
    )'''

    def draw(self, context):
       layout = self.layout
       # layout.label(text="Make Vertex Parent")
       # 第一引数は実行機能クラスのbl_idname
       layout.operator(MakeVertexParent_operator.bl_idname, text="Add")

class MakeVertexParent_operator(Operator):
    bl_idname = "makevertexparent.operator" #bl_idnameは小文字必須
    bl_label = "lbl_MakeVertexParent_operator"

    def execute(self, context):
        print("run Make Vertex Parent") #処理開始

        # 現在のモードを保存
        current_mode = bpy.context.object.mode

        # オブジェクトモードに切り替える
        bpy.ops.object.mode_set(mode='OBJECT')

        # BMeshのインスタンスを取得
        obj = context.active_object

        # 選択された3つの頂点を取得する
        selVers = [v for v in obj.data.vertices if v.select]
        if len(selVers) != 3:
            self.report({'ERROR'}, "編集モードで頂点を3つ選択してから実行して下さい")
            # 保存しておいたモードに戻す
            bpy.ops.object.mode_set(mode=current_mode)
            return {'CANCELLED'}

        # 選択された3つの頂点の中心座標を計算する
        selCenter = sum([v.co for v in selVers], Vector()) / 3

        # 中心座標をワールド座標に変換する
        selCenter_world = obj.matrix_world @ selCenter

        # エンプティを新規作成する
        bpy.ops.object.add(type='EMPTY', align='WORLD')
        empty = bpy.context.active_object
        empty.select_set(True)

        # エンプティーの座標を変更する
        empty.location = selCenter_world

        # "empty" と "obj" を選択状態にする
        empty.select_set(True)
        obj.select_set(True)

        # "obj" をアクティブにする
        context.view_layer.objects.active = obj

        # 編集モードに切り替える
        bpy.ops.object.mode_set(mode='EDIT')

        # 頂点ペアレント作成
        bpy.ops.object.vertex_parent_set()

        # 重要：操作が完了したことをBlenderに伝える（通常のOperatorのメソッドには必須）
        return {'FINISHED'} 

# 作ったクラスを格納
classes = [MakeVertexParent_Panel, MakeVertexParent_operator]

# belnderに登録する関数
def register():
   for cls in classes:
       bpy.utils.register_class(cls)
   # メニュー関数はappendする
   bpy.types.VIEW3D_MT_mesh_add.append(menu_MakeVertexParent)

# belnderから登録解除する関数
def unregister():
   for cls in classes:
       bpy.utils.unregister_class(cls)
   bpy.types.VIEW3D_MT_mesh_add.remove(menu_MakeVertexParent)

# pythonファイルを実行するおまじない
if __name__ == "__main__":
   register()