# X Analytics Dashboard

X/Twitter用の分析ダッシュボードとツイートスクレイピングツールです。リアルタイムでアカウントの統計データを取得・可視化し、効果的なSNS運用をサポートします。

## 🚀 機能

### フロントエンド
- **📊 アナリティクスダッシュボード**: ツイート数、いいね数、リツイート数などの統計を可視化
- **📈 データ可視化**: 時系列チャート、円グラフ、棒グラフでエンゲージメントを分析
- **✍️ ツイート投稿機能**: X API経由でダッシュボードから直接投稿
- **⚙️ API設定画面**: Bearer TokenやOAuth認証情報を安全に管理
- **📱 レスポンシブ対応**: PC・スマートフォンの両方に最適化

### バックエンド
- **🔍 データスクレーピング**: twikitライブラリを使用したツイートとユーザー情報の収集
- **👥 ユーザー分析**: フォロワー数、ツイート数、プロフィール情報の取得
- **🕒 ゲストモード対応**: ログイン不要でのデータ取得（一部機能制限あり）

## 🛠️ 技術スタック

### フロントエンド
- **Next.js 15** - React フレームワーク
- **TypeScript** - 型安全な開発
- **Tailwind CSS** - ユーティリティファーストCSS
- **Recharts** - データ可視化ライブラリ
- **Lucide React** - アイコンライブラリ

### バックエンド
- **Python** - バックエンド言語
- **twikit** - X/Twitter スクレーピングライブラリ
- **twitter-api-v2** - X API v2 クライアント

### インフラ
- **Vercel** - デプロイプラットフォーム
- **Node.js** - ランタイム環境

## 📋 前提条件

- Node.js 18以上
- Python 3.8以上
- X Developer Portal アカウント（API利用時）

## 🔧 セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd x
```

### 2. フロントエンドのセットアップ

```bash
cd fronend
npm install
```

### 3. バックエンドのセットアップ

```bash
cd ../backend
pip install twikit asyncio
```

### 4. 環境変数の設定

フロントエンドディレクトリに `.env.local` ファイルを作成：

```bash
# X API認証情報（投稿機能用）
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN_KEY=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

## 🚀 使用方法

### フロントエンドの起動

```bash
cd fronend
npm run dev
```

http://localhost:3000 でアクセス可能です。

### バックエンドスクレーピングの実行

```bash
cd backend
python scraper.py
```

### X API認証の設定

1. [X Developer Portal](https://developer.twitter.com) でアプリを作成
2. Keys and Tokens から認証情報を取得
3. ダッシュボードの「設定」タブで認証情報を入力
4. 接続テストを実行

## 📁 プロジェクト構造

```
x/
├── fronend/                 # Next.jsフロントエンド
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/tweet/   # ツイート投稿API
│   │   │   ├── components/  # Reactコンポーネント
│   │   │   ├── page.tsx     # メインダッシュボード
│   │   │   └── layout.tsx   # レイアウト
│   │   └── ...
│   ├── package.json
│   └── ...
├── backend/                 # Pythonスクレーピング
│   ├── scraper.py          # twikitスクレーパー
│   └── tweets_guest.json   # 取得データ
├── vercel.json             # Vercel設定
└── README.md
```

## 🎯 主要コンポーネント

### アナリティクスダッシュボード (`fronend/src/app/page.tsx`)
- KPIカード表示
- 時系列チャート
- エンゲージメント分析
- 人気投稿一覧

### ツイート投稿コンポーネント (`fronend/src/app/components/post.tsx`)
- リアルタイム投稿
- 文字数カウント
- エラーハンドリング

### API エンドポイント (`fronend/src/app/api/tweet/route.ts`)
- X API v2 連携
- 投稿データの処理
- エラーレスポンス

### スクレーピングツール (`backend/scraper.py`)
- ゲストモード対応
- ユーザー情報取得
- ツイート履歴収集

## 🔐 セキュリティ

- API認証情報は環境変数で管理
- フロントエンドでは認証情報を直接扱わない
- HTTPS通信の推奨
- レート制限の考慮

## 📊 分析機能

### 提供される指標
- **投稿数**: 日別・週別・月別の投稿統計
- **エンゲージメント**: いいね数、リツイート数、リプライ数
- **インプレッション**: ツイートの表示回数
- **フォロワー動向**: フォロワー数の推移
- **人気投稿**: エンゲージメントの高い投稿ランキング

### 可視化形式
- 📈 折れ線グラフ: 時系列データ
- 📊 棒グラフ: カテゴリ別比較
- 🥧 円グラフ: 構成比率
- 📋 テーブル: 詳細データ

## 🚀 デプロイ

### Vercelへのデプロイ

1. Vercelアカウントでリポジトリを接続
2. 環境変数を設定
3. 自動デプロイの実行

```bash
# ローカルでビルドテスト
cd fronend
npm run build
npm start
```

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は `LICENSE` ファイルを参照してください。

## 🐛 バグ報告・機能要望

Issues タブから報告をお願いします。以下の情報を含めてください：

- 環境情報（OS、Node.js バージョンなど）
- 再現手順
- 期待される動作
- 実際の動作
- スクリーンショット（該当する場合）

## 📞 サポート

質問や不明点がございましたら、Issues または Discussions でお気軽にお尋ねください。

---

**⚠️ 注意**: X APIの利用には制限があります。レート制限やAPIの利用規約を必ずご確認ください。