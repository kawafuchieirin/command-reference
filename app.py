import streamlit as st
import json

# JSONファイル読み込み
with open("commands.json", encoding="utf-8") as f:
    commands = json.load(f)

st.title("🛠️ コマンドリファレンス")

# カテゴリを抽出（重複なし、ソート済み）
categories = sorted(set(cmd["category"] for cmd in commands))

# カテゴリ選択
selected_category = st.selectbox("📁 カテゴリを選択", categories)

# 選択されたカテゴリのコマンドをフィルタリング
filtered_commands = [cmd for cmd in commands if cmd["category"] == selected_category]
command_names = [cmd["name"] for cmd in filtered_commands]

# コマンド選択
selected_command = st.selectbox("🔧 コマンドを選択", command_names)

# 選択されたコマンドの詳細を取得
cmd = next(c for c in filtered_commands if c["name"] == selected_command)

st.subheader("📄 説明")
st.write(cmd["description"])

st.subheader("💻 使用例")
st.code(cmd["usage"], language="bash")