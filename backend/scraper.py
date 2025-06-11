# twikit_scraper.py
import asyncio
import json
from datetime import datetime
from twikit import Client
from twikit.guest import GuestClient

class TwikitScraper:
    def __init__(self, use_guest_mode=True):
        """
        Twikitスクレイパーの初期化
        
        Args:
            use_guest_mode (bool): ゲストモード使用（ログイン不要）
        """
        self.use_guest_mode = use_guest_mode
        if use_guest_mode:
            self.client = GuestClient()
        else:
            self.client = Client('ja-JP')  # 日本語設定
    
    async def setup(self, username=None, email=None, password=None):
        """セットアップ"""
        if self.use_guest_mode:
            # ゲストトークンを生成してクライアントを有効化
            await self.client.activate()
            print("ゲストモードで接続しました")
        else:
            if not all([username, email, password]):
                raise ValueError("ログインモードには username, email, password が必要です")
            
            # ログイン（クッキーファイルを使用してセッション保持）
            await self.client.login(
                auth_info_1=username,
                auth_info_2=email,
                password=password,
                cookies_file='cookies.json'  # セッション保持
            )
            print("ログインしました")
    
    async def search_tweets(self, query, product='Latest', count=20):
        """
        ツイート検索
        
        Args:
            query (str): 検索クエリ
            product (str): 'Top', 'Latest', 'Media', 'People'
            count (int): 取得数
        """
        try:
            print(f"検索中: '{query}'")
            
            if self.use_guest_mode:
                # ゲストモードでは検索機能が制限される場合があります
                print("注意: ゲストモードでは一部機能が制限されます")
                return []
            else:
                # ログインモードで検索
                tweets = await self.client.search_tweet(query, product, count)
                
                results = []
                for tweet in tweets:
                    tweet_data = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'user': {
                            'id': tweet.user.id,
                            'name': tweet.user.name,
                            'username': tweet.user.screen_name,
                            'followers_count': tweet.user.followers_count,
                            'verified': tweet.user.verified
                        },
                        'metrics': {
                            'retweet_count': tweet.retweet_count,
                            'favorite_count': tweet.favorite_count,
                            'reply_count': tweet.reply_count,
                            'quote_count': tweet.quote_count if hasattr(tweet, 'quote_count') else 0
                        },
                        'url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                    }
                    results.append(tweet_data)
                
                return results
                
        except Exception as e:
            print(f"検索エラー: {e}")
            return []
    
    async def get_user_info(self, username):
        """ユーザー情報取得"""
        try:
            if self.use_guest_mode:
                user = await self.client.get_user_by_screen_name(username)
            else:
                user = await self.client.get_user_by_screen_name(username)
            
            return {
                'id': user.id,
                'name': user.name,
                'username': user.screen_name,
                'description': user.description,
                'followers_count': user.followers_count,
                'following_count': user.friends_count,
                'tweet_count': user.statuses_count,
                'verified': user.verified,
                'profile_image_url': user.profile_image_url,
                'created_at': user.created_at
            }
            
        except Exception as e:
            print(f"ユーザー情報取得エラー: {e}")
            return None
    
    async def get_user_tweets(self, username, count=20):
        """ユーザーのツイート取得"""
        try:
            if self.use_guest_mode:
                user = await self.client.get_user_by_screen_name(username)
                tweets = await self.client.get_user_tweets(user.id, count=count)
            else:
                user = await self.client.get_user_by_screen_name(username)
                tweets = await self.client.get_user_tweets(user.id, count=count)
            
            results = []
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'reply_count': tweet.reply_count,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}"
                }
                results.append(tweet_data)
            
            return results
            
        except Exception as e:
            print(f"ユーザーツイート取得エラー: {e}")
            return []
    
    async def get_trending_topics(self):
        """トレンド取得（ログイン必要）"""
        try:
            if self.use_guest_mode:
                print("トレンド取得にはログインが必要です")
                return []
            
            trends = await self.client.get_trends()
            return [{'name': trend.name, 'url': trend.url} for trend in trends]
            
        except Exception as e:
            print(f"トレンド取得エラー: {e}")
            return []
    
    def save_to_json(self, data, filename):
        """JSONファイルに保存"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"データを {filename} に保存しました")

# 使用例
async def main():
    # ゲストモードでの使用例
    print("=== ゲストモードテスト ===")
    guest_scraper = TwikitScraper(use_guest_mode=True)
    await guest_scraper.setup()
    
    # ユーザー情報取得
    user_info = await guest_scraper.get_user_info('elonmusk')
    if user_info:
        print(f"ユーザー: @{user_info['username']}")
        print(f"名前: {user_info['name']}")
        print(f"フォロワー数: {user_info['followers_count']:,}")
        print(f"ツイート数: {user_info['tweet_count']:,}")
    
    # ユーザーのツイート取得
    tweets = await guest_scraper.get_user_tweets('elonmusk', count=5)
    print(f"\n取得したツイート数: {len(tweets)}")
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\n{i}. {tweet['text'][:100]}...")
        print(f"   日時: {tweet['created_at']}")
        print(f"   いいね: {tweet['favorite_count']}")
        print(f"   リツイート: {tweet['retweet_count']}")
    
    # データ保存
    if tweets:
        guest_scraper.save_to_json(tweets, 'tweets_guest.json')
    
    print("\n" + "="*50)
    
    # ログインモードでの使用例（アカウント情報が必要）
    print("\n=== ログインモードテスト ===")
    print("注意: ログインモードを使用するには有効なTwitterアカウントが必要です")
    
    # 実際のアカウント情報を使用する場合はコメントアウトを解除
    """
    login_scraper = TwikitScraper(use_guest_mode=False)
    await login_scraper.setup(
        username='your_username',
        email='your_email@example.com',
        password='your_password'
    )
    
    # ツイート検索（ログインモードのみ）
    search_results = await login_scraper.search_tweets('Python programming', count=10)
    print(f"検索結果: {len(search_results)}件")
    
    for i, tweet in enumerate(search_results[:3], 1):
        print(f"\n{i}. @{tweet['user']['username']}")
        print(f"   {tweet['text'][:100]}...")
        print(f"   いいね: {tweet['metrics']['favorite_count']}")
    
    # トレンド取得
    trends = await login_scraper.get_trending_topics()
    print(f"\nトレンド数: {len(trends)}")
    for trend in trends[:5]:
        print(f"  - {trend['name']}")
    """

if __name__ == "__main__":
    # インストールコマンド: pip install twikit
    asyncio.run(main())