#!/bin/bash

# Streamlit開発サーバー起動スクリプト
# 自動再起動機能を有効にして起動します

echo "🚀 Streamlit開発サーバーを起動しています..."
echo "📝 ファイルを保存すると自動的に再起動されます"
echo "🛑 終了するには Ctrl+C を押してください"
echo ""

# 自動再起動を有効にしてStreamlitを起動
streamlit run app.py --server.runOnSave true