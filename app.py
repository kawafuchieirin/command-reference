import streamlit as st
import json
import traceback
import sys

# エラーハンドリングを追加したJSONファイル読み込み
try:
    with open("commands.json", encoding="utf-8") as f:
        commands = json.load(f)
except FileNotFoundError:
    st.error("⚠️ commands.jsonファイルが見つかりません。ファイルが正しい場所にあるか確認してください。")
    st.stop()
except json.JSONDecodeError as e:
    st.error(f"⚠️ commands.jsonの解析エラー: {e}")
    st.stop()
except Exception as e:
    st.error(f"⚠️ 予期しないエラーが発生しました: {e}")
    st.stop()

# セッションステートの初期化
if "builder_command" not in st.session_state:
    st.session_state["builder_command"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "リファレンス"

# サイドバーでページ選択
st.sidebar.title("📚 ナビゲーション")
page = st.sidebar.radio(
    "ページを選択",
    ["リファレンス", "コマンドビルダー"],
    index=0 if st.session_state["current_page"] == "リファレンス" else 1
)

# ページが変更されたら記録
if page != st.session_state["current_page"]:
    st.session_state["current_page"] = page

def show_reference_page():
    """コマンドリファレンスページを表示"""
    try:
        st.title("🛠️ コマンドリファレンス")
    
    # 大カテゴリを抽出（重複なし、ソート済み）
    main_categories = sorted(set(cmd["main_category"] for cmd in commands))
    
    # 大カテゴリ選択
    selected_main_category = st.selectbox("🏢 大カテゴリを選択", main_categories)
    
    # 選択された大カテゴリのサブカテゴリを抽出
    sub_categories = sorted(set(cmd["sub_category"] for cmd in commands if cmd["main_category"] == selected_main_category))
    
    # サブカテゴリ選択
    selected_sub_category = st.selectbox("📁 サブカテゴリを選択", sub_categories)
    
    # 選択されたカテゴリのコマンドをフィルタリング
    filtered_commands = [cmd for cmd in commands 
                        if cmd["main_category"] == selected_main_category 
                        and cmd["sub_category"] == selected_sub_category]
    command_names = [cmd["name"] for cmd in filtered_commands]
    
    # コマンド選択
    if command_names:
        selected_command = st.selectbox("🔧 コマンドを選択", command_names)
        
        # 選択されたコマンドの詳細を取得
        cmd = next(c for c in filtered_commands if c["name"] == selected_command)
        
        st.subheader("📄 説明")
        st.write(cmd["description"])
        
        st.subheader("💻 使用例")
        st.code(cmd["usage"], language="bash")
        
        # ビルダー対応コマンドの場合、ビルダーへの遷移ボタンを表示
        if "builder" in cmd:
            st.markdown("---")
            if st.button("🔧 このコマンドをビルダーで編集", type="primary"):
                # セッションステートにコマンド情報を保存
                st.session_state["builder_command"] = {
                    "main_category": cmd["main_category"],
                    "sub_category": cmd["sub_category"],
                    "name": cmd["name"]
                }
                # ビルダーページへ遷移
                st.session_state["current_page"] = "コマンドビルダー"
                st.rerun()
    else:
        st.info("このカテゴリにはコマンドがありません。")
    except Exception as e:
        st.error(f"⚠️ ページ表示中にエラーが発生しました: {e}")
        st.error(f"詳細: {traceback.format_exc()}")
        st.info("💡 ページをリロードしてください。問題が解決しない場合は、ターミナルでStreamlitを再起動してください。")

def show_builder_page():
    """コマンドビルダーページを表示"""
    try:
        st.title("🛠️ コマンドビルダー")
    
    # ビルダー対応コマンドのみフィルタリング
    builder_commands = [cmd for cmd in commands if "builder" in cmd]
    builder_main_categories = sorted(set(cmd["main_category"] for cmd in builder_commands))
    
    if not builder_commands:
        st.info("現在、コマンドビルダーに対応したコマンドはありません。")
        return
    
    # セッションステートから引き継いだコマンド情報を確認
    preset_command = st.session_state.get("builder_command")
    
    if preset_command:
        # リファレンスから引き継いだ情報がある場合
        st.info(f"📌 リファレンスから選択されたコマンド: {preset_command['name']}")
        
        # 引き継いだ情報をデフォルト値として設定
        default_main_idx = builder_main_categories.index(preset_command["main_category"]) if preset_command["main_category"] in builder_main_categories else 0
        builder_main_category = st.selectbox(
            "🏢 ビルダー対応大カテゴリを選択", 
            builder_main_categories, 
            index=default_main_idx,
            key="builder_main_category"
        )
        
        # サブカテゴリを抽出
        builder_sub_categories = sorted(set(cmd["sub_category"] for cmd in builder_commands if cmd["main_category"] == builder_main_category))
        default_sub_idx = builder_sub_categories.index(preset_command["sub_category"]) if preset_command["sub_category"] in builder_sub_categories else 0
        builder_sub_category = st.selectbox(
            "📁 ビルダー対応サブカテゴリを選択", 
            builder_sub_categories,
            index=default_sub_idx,
            key="builder_sub_category"
        )
        
        # コマンドリストを取得
        filtered_builder_commands = [cmd for cmd in builder_commands 
                                    if cmd["main_category"] == builder_main_category 
                                    and cmd["sub_category"] == builder_sub_category]
        builder_command_names = [cmd["name"] for cmd in filtered_builder_commands]
        
        if builder_command_names:
            default_cmd_idx = builder_command_names.index(preset_command["name"]) if preset_command["name"] in builder_command_names else 0
            selected_builder_command = st.selectbox(
                "🔧 ビルダー対応コマンドを選択", 
                builder_command_names,
                index=default_cmd_idx,
                key="builder_command"
            )
        else:
            selected_builder_command = None
        
        # 使用後はセッションステートをクリア
        if st.button("🔄 選択をリセット"):
            st.session_state["builder_command"] = None
            st.rerun()
    else:
        # 通常の選択UI
        builder_main_category = st.selectbox("🏢 ビルダー対応大カテゴリを選択", builder_main_categories, key="builder_main_category")
        
        # サブカテゴリを抽出
        builder_sub_categories = sorted(set(cmd["sub_category"] for cmd in builder_commands if cmd["main_category"] == builder_main_category))
        builder_sub_category = st.selectbox("📁 ビルダー対応サブカテゴリを選択", builder_sub_categories, key="builder_sub_category")
        
        # 選択されたカテゴリのビルダー対応コマンドをフィルタリング
        filtered_builder_commands = [cmd for cmd in builder_commands 
                                    if cmd["main_category"] == builder_main_category 
                                    and cmd["sub_category"] == builder_sub_category]
        builder_command_names = [cmd["name"] for cmd in filtered_builder_commands]
        
        if builder_command_names:
            selected_builder_command = st.selectbox("🔧 ビルダー対応コマンドを選択", builder_command_names, key="builder_command")
        else:
            selected_builder_command = None
            st.info("このカテゴリにはビルダー対応コマンドがありません。")
    
    # コマンドが選択されている場合、ビルダーUIを表示
    if selected_builder_command:
        # 選択されたコマンドの詳細を取得
        builder_cmd = next(c for c in builder_commands if c["name"] == selected_builder_command)
        
        st.info(f"📝 {builder_cmd['description']}")
        
        # コマンドビルダー
        if "builder" in builder_cmd:
            builder = builder_cmd["builder"]
            
            # パラメータ入力
            param_values = {}
            if builder.get("params"):
                st.subheader("📥 必須パラメータ")
                for param in builder["params"]:
                    # パラメータ名を日本語に変換
                    param_label = {
                        "path": "パス",
                        "source": "ソース",
                        "destination": "宛先",
                        "function-name": "関数名",
                        "output-file": "出力ファイル",
                        "repository-url": "リポジトリURL",
                        "directory": "ディレクトリ"
                    }.get(param, param)
                    
                    param_values[param] = st.text_input(f"{param_label}", key=f"param_{param}")
            
            # オプション選択
            option_values = []
            if builder.get("options"):
                st.subheader("⚙️ オプション")
                
                for opt in builder["options"]:
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.write(opt["name"])
                    
                    with col2:
                        if opt["type"] == "flag":
                            if st.checkbox(opt["description"], key=f"opt_{opt['name']}"):
                                option_values.append(opt["name"])
                        
                        elif opt["type"] == "text":
                            val = st.text_input(
                                opt["description"],
                                key=f"opt_{opt['name']}_text"
                            )
                            if val:
                                option_values.append(f"{opt['name']} {val}")
                        
                        elif opt["type"] == "select":
                            val = st.selectbox(
                                opt["description"],
                                ["選択してください"] + opt["choices"],
                                key=f"opt_{opt['name']}_select"
                            )
                            if val != "選択してください":
                                option_values.append(f"{opt['name']}{val}")
            
            # コマンド生成
            st.subheader("✨ 生成されたコマンド")
            
            # コマンドを組み立て
            cmd_parts = [selected_builder_command]
            
            # パラメータを追加
            for param in builder.get("params", []):
                if param in param_values and param_values[param]:
                    # aws lambda invokeの場合、--function-nameを追加
                    if selected_builder_command == "aws lambda invoke" and param == "function-name":
                        cmd_parts.append(f"--function-name {param_values[param]}")
                    # git cloneの場合、repository-urlとdirectoryは位置引数
                    elif selected_builder_command == "git clone":
                        cmd_parts.append(param_values[param])
                    else:
                        cmd_parts.append(param_values[param])
            
            # オプションを追加
            cmd_parts.extend(option_values)
            
            final_command = " ".join(cmd_parts)
            
            # コマンド表示とコピー機能
            col1, col2 = st.columns([5, 1])
            
            with col1:
                st.code(final_command, language="bash")
            
            with col2:
                # Streamlitのデフォルトのコピー機能を使用するため、
                # 説明テキストのみ表示
                st.write("")
                st.caption("📋 コピー")
            
            # 使用例
            if final_command.strip() and final_command != selected_builder_command:
                st.success("✅ コマンドが生成されました！上記のコマンドをコピーして使用してください。")
    elif not preset_command:
        st.info("📌 リファレンスから選択するか、上記のドロップダウンからコマンドを選択してください。")
    except Exception as e:
        st.error(f"⚠️ ビルダーページ表示中にエラーが発生しました: {e}")
        st.error(f"詳細: {traceback.format_exc()}")
        st.info("💡 ページをリロードしてください。問題が解決しない場合は、ターミナルでStreamlitを再起動してください。")

# ページのルーティング
try:
    if page == "リファレンス":
        show_reference_page()
    else:
        show_builder_page()
except Exception as e:
    st.error(f"⚠️ アプリケーションエラーが発生しました: {e}")
    st.error(f"詳細: {traceback.format_exc()}")
    st.info("💡 以下の方法で問題を解決してください:")
    st.markdown("""
    1. **ブラウザをリロード**: `F5`キーまたは`Ctrl+R`（Mac: `Cmd+R`）
    2. **Streamlitを再起動**: ターミナルで`Ctrl+C`で停止後、再度`streamlit run app.py`を実行
    3. **自動再起動の有効化**: `streamlit run app.py --server.runOnSave true`
    """)