# 🛠️ コマンドリファレンス

コマンドラインツールのリファレンスを簡単に検索・表示できるWebアプリケーションです。

## 概要

開発者やシステム管理者が頻繁に使用するコマンドの使い方を素早く確認できるツールです。Streamlitを使用したシンプルなインターフェースで、必要なコマンドの情報にすぐにアクセスできます。

## 主な機能

- **コマンド検索機能**: ドロップダウンメニューから必要なコマンドを選択
- **詳細情報表示**: 各コマンドの説明と使用例を表示
- **シンプルなUI**: Streamlitを使用した直感的なインターフェース
- **拡張性**: JSONファイルにコマンドを追加することで簡単に拡張可能

## クイックスタート

### 前提条件

- Python 3.7以上
- pip（Pythonパッケージ管理ツール）

### インストール

1. リポジトリのクローン
   ```bash
   git clone https://github.com/kawafuchieirin/command-reference.git
   cd command-reference
   ```

2. 必要なパッケージのインストール
   ```bash
   pip install streamlit
   ```

### 起動方法

```bash
streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501` でアプリケーションにアクセスできます。

## 使い方

1. アプリケーションを起動する
2. ドロップダウンメニューから確認したいコマンドを選択
3. 選択したコマンドの説明と使用例が表示される

## コマンドの追加方法

`commands.json`ファイルに以下の形式でコマンド情報を追加します：

```json
{
  "name": "コマンド名",
  "description": "コマンドの説明",
  "usage": "コマンドの使用例"
}
```

## プロジェクト構成

```
command-reference/
├── README.md          # このファイル
├── CLAUDE.md          # 詳細な開発ガイド
├── app.py             # メインアプリケーション
└── commands.json      # コマンド情報を格納するJSONファイル
```

## デプロイ

### Streamlit Community Cloud（推奨）

1. [Streamlit Cloud](https://streamlit.io/cloud)でアカウントを作成
2. このGitHubリポジトリと連携
3. 自動的にデプロイされます

## 貢献方法

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/new-command`)
3. 変更をコミット (`git commit -am 'Add new command'`)
4. ブランチにプッシュ (`git push origin feature/new-command`)
5. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 作者

- [@kawafuchieirin](https://github.com/kawafuchieirin)

## 参考リンク

- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [Python公式サイト](https://www.python.org/)