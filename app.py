import streamlit as st
import json

# JSONファイル読み込み
with open("commands.json", encoding="utf-8") as f:
    commands = json.load(f)

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
else:
    st.info("このカテゴリにはコマンドがありません。")

# コマンドビルダーセクション
st.markdown("---")
st.title("🛠️ コマンドビルダー")

# ビルダー対応コマンドのみフィルタリング
builder_commands = [cmd for cmd in commands if "builder" in cmd]
builder_main_categories = sorted(set(cmd["main_category"] for cmd in builder_commands))

if builder_commands:
    # 大カテゴリ選択（ビルダー用）
    builder_main_category = st.selectbox("🏢 ビルダー対応大カテゴリを選択", builder_main_categories, key="builder_main_category")
    
    # サブカテゴリを抽出（ビルダー用）
    builder_sub_categories = sorted(set(cmd["sub_category"] for cmd in builder_commands if cmd["main_category"] == builder_main_category))
    
    # サブカテゴリ選択（ビルダー用）
    builder_sub_category = st.selectbox("📁 ビルダー対応サブカテゴリを選択", builder_sub_categories, key="builder_sub_category")
    
    # 選択されたカテゴリのビルダー対応コマンドをフィルタリング
    filtered_builder_commands = [cmd for cmd in builder_commands 
                                if cmd["main_category"] == builder_main_category 
                                and cmd["sub_category"] == builder_sub_category]
    builder_command_names = [cmd["name"] for cmd in filtered_builder_commands]
    
    if builder_command_names:
        # コマンド選択（ビルダー用）
        selected_builder_command = st.selectbox("🔧 ビルダー対応コマンドを選択", builder_command_names, key="builder_command")
        
        # 選択されたコマンドの詳細を取得
        builder_cmd = next(c for c in filtered_builder_commands if c["name"] == selected_builder_command)
        
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
    else:
        st.info("このカテゴリにはビルダー対応コマンドがありません。")
else:
    st.info("現在、コマンドビルダーに対応したコマンドはありません。")