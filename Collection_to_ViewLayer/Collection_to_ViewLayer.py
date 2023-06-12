import bpy
from bpy import context

def duplicate_view_layers_from_collections():
    # ここに本体のスクリプトを書く

    # 除外したいコレクション名のリスト
    excluded_collections = ["Collection"]

    def get_all_children(collection, children_list):
        for child in collection.children:
            children_list.append(child.name)
            get_all_children(child, children_list)
        return children_list

    # 初期化
    Full_Exclud_Collection = excluded_collections.copy()

    for collection_name in excluded_collections:
        # それぞれのコレクションに対してすべての子を取得
        collection = bpy.data.collections.get(collection_name)
        if collection is not None:
            Full_Exclud_Collection += get_all_children(collection, [])

    print("Full Exclud Collection: ", Full_Exclud_Collection)  # 出力: ["Collection", "Collection 1", ...]

    # 選択されたコレクションの名前を保存するリストを初期化
    selected_collections = []

    for window in context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'OUTLINER':
                with context.temp_override(window=window, area=area):
                    for item in context.selected_ids:
                        if item.bl_rna.identifier == "Collection" and item.name not in Full_Exclud_Collection:
                            selected_collections.append(item.name)

    # 選択されたコレクションの名前を表示
    print("Selected collections: ", selected_collections)

    # 現在のビューレイヤーを取得
    current_view_layer = bpy.context.window.view_layer

    # 再帰関数を定義
    def set_collection_exclude(layer_collection, name):
        for child_layer_collection in layer_collection.children:
            if child_layer_collection.name in excluded_collections:
                # このコレクションとその子コレクションの処理をスキップ
                continue

            child_layer_collection.exclude = True

            if child_layer_collection.name == name:
                # 新しいビューレイヤーで対応するコレクションを除外する
                child_layer_collection.exclude = False

            # Recurse into the children
            set_collection_exclude(child_layer_collection, name)

    # 選択された各コレクションに対してビューレイヤーを複製
    for collection_name in selected_collections:
        # 現在のビューレイヤーをコピーして新しいビューレイヤーを作成
        bpy.ops.scene.view_layer_add(type='COPY')

        # 新しいビューレイヤーは自動的にアクティブになるのでその名前を変更
        new_view_layer = bpy.context.window.view_layer
        new_view_layer.name = current_view_layer.name + "_" + collection_name

        # 新しいビューレイヤーのすべてのコレクションを繰り返し処理する
        set_collection_exclude(new_view_layer.layer_collection, collection_name)

    # 現在のビューレイヤーに戻す
    bpy.context.window.view_layer = current_view_layer

# Call the function
duplicate_view_layers_from_collections()
