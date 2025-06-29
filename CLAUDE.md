# CLAUDE.md

## 1️⃣ プロジェクト概要

### プロジェクトの目的
このプロジェクトは、コマンドラインツールのリファレンスを簡単に検索・表示できるWebアプリケーションです。開発者やシステム管理者が頻繁に使用するコマンドの使い方を素早く確認できるようにすることで、作業効率の向上を図ります。

### 主な機能や背景
- **カテゴリ別表示**: コマンドをカテゴリごとに整理して表示
- **コマンド検索機能**: カテゴリを選択してから必要なコマンドを選択
- **詳細情報表示**: 各コマンドの説明と使用例を表示
- **シンプルなUI**: Streamlitを使用した直感的なインターフェース
- **拡張性**: JSONファイルにコマンドを追加することで簡単に拡張可能

## 2️⃣ システム構成

### 全体アーキテクチャ概要
```
┌─────────────────┐     ┌─────────────────┐
│   Webブラウザ   │────▶│  Streamlit App  │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  commands.json  │
                        └─────────────────┘
```

### 使用技術
- **フロントエンド/バックエンド**: Streamlit (Python)
- **データストレージ**: JSON ファイル
- **プログラミング言語**: Python 3.x

### ディレクトリ構成の説明
```
command-reference/
├── README.md          # プロジェクトの簡単な説明
├── CLAUDE.md          # このドキュメント（詳細な開発ガイド）
├── app.py             # メインアプリケーション（Streamlit）
└── commands.json      # コマンド情報を格納するJSONファイル
```

## 📂 利用可能なカテゴリ

### 現在登録されているカテゴリ
- **Linux**: 基本的なLinuxコマンド（ls, cd, pwd）
- **AWS Core**: AWS CLIの基本設定とSTS関連（aws configure, sts）
- **AWS S3**: S3バケットとオブジェクトの操作
- **AWS EC2**: EC2インスタンスとネットワークの管理
- **AWS Lambda**: Lambda関数の作成・管理
- **AWS IAM**: ユーザー、ロール、ポリシーの管理
- **AWS RDS**: RDSデータベースインスタンスの操作
- **AWS CloudFormation**: インフラストラクチャのコード化
- **AWS DynamoDB**: NoSQLデータベースの操作
- **AWS Messaging**: SQS、SNSメッセージングサービス
- **AWS Monitoring**: CloudWatch、ログの監視
- **AWS Container**: ECR、EKSコンテナサービス
- **AWS Networking**: Route53、API Gateway
- **AWS Management**: Organizations、Cost Explorer

## 3️⃣ 開発環境構築手順

### 前提条件
- Python 3.7以上がインストールされていること
- pip（Pythonパッケージ管理ツール）が使用可能であること

### セットアップ手順
1. リポジトリのクローン
   ```bash
   git clone https://github.com/kawafuchieirin/command-reference.git
   cd command-reference
   ```

2. 仮想環境の作成（推奨）
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. 必要なパッケージのインストール
   ```bash
   pip install streamlit
   ```

## 4️⃣ 動作確認方法

### 実行手順
1. アプリケーションの起動
   ```bash
   streamlit run app.py
   ```

2. ブラウザで自動的に開かれるか、以下のURLにアクセス
   ```
   http://localhost:8501
   ```

### 確認ポイント
- [ ] アプリケーションが正常に起動すること
- [ ] カテゴリ選択ドロップダウンが表示されること
- [ ] カテゴリを選択すると該当するコマンドのみが表示されること
- [ ] コマンドを選択すると説明と使用例が表示されること
- [ ] 日本語が正しく表示されること

### 動作イメージ
アプリケーションは以下のような構成で表示されます：
- タイトル: 「🛠️ コマンドリファレンス」
- カテゴリ選択: 「📁 カテゴリを選択」ドロップダウン
- コマンド選択: 「🔧 コマンドを選択」ドロップダウン（選択したカテゴリのコマンドのみ表示）
- 説明セクション: 選択したコマンドの説明
- 使用例セクション: コマンドの具体的な使用方法

## 5️⃣ デプロイ・運用

### 現状の運用フロー
現在はローカル環境での動作を想定していますが、以下の方法でデプロイ可能です：

1. **Streamlit Community Cloud**（無料）
   - GitHubリポジトリと連携して自動デプロイ
   - https://streamlit.io/cloud でアカウント作成後、リポジトリを接続

2. **その他のクラウドサービス**
   - Heroku、AWS、GCPなどでのデプロイも可能

### 将来的な改善ポイント
- [ ] コマンドの検索機能（フリーワード検索）の追加
- [x] カテゴリ別表示機能の実装 ✅
- [ ] コマンドのお気に入り機能
- [ ] ユーザーによるコマンド追加機能
- [ ] 多言語対応（英語版など）

## 6️⃣ 補足情報

### 参考リンク
- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [Python公式サイト](https://www.python.org/)
- [GitHub - command-reference](https://github.com/kawafuchieirin/command-reference)

### FAQ

**Q: 新しいコマンドを追加するには？**
A: `commands.json`ファイルに以下の形式でコマンド情報を追加してください：
```json
{
  "category": "カテゴリ名",
  "name": "コマンド名",
  "description": "コマンドの説明",
  "usage": "コマンドの使用例"
}
```

**Q: Streamlitアプリが起動しない場合は？**
A: 以下を確認してください：
- Pythonのバージョンが3.7以上か
- Streamlitが正しくインストールされているか（`pip list`で確認）
- ファイアウォールがポート8501をブロックしていないか

**Q: 日本語が文字化けする場合は？**
A: `commands.json`ファイルがUTF-8エンコーディングで保存されているか確認してください。

### 注意事項
- `commands.json`を編集する際は、必ず有効なJSON形式を維持してください
- 本番環境で使用する場合は、適切なセキュリティ対策を実施してください
- 大量のコマンドを追加する場合は、パフォーマンスに注意してください