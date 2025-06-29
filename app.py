import streamlit as st
import json

# JSONファイル読み込み
with open("commands.json", encoding="utf-8") as f:
    commands = json.load(f)

st.title("🛠️ コマンドリファレンス")

command_names = [cmd["name"] for cmd in commands]
selected = st.selectbox("コマンドを選んでください", command_names)

cmd = next(c for c in commands if c["name"] == selected)

st.subheader("📄 説明")
st.write(cmd["description"])

st.subheader("💻 使用例")
st.code(cmd["usage"], language="bash")