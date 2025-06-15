# twikit_scraper.py
import asyncio
import json
import random
import time
from twikit import Client
from twikit.guest import GuestClient

class TwikitScraper:
    def __init__(self, use_guest_mode=True, human_like=True):
        """
        Twikitスクレイパーの初期化
        
        Args:
            use_guest_mode (bool): ゲストモード使用（ログイン不要）
            human_like (bool): 人間らしい動作を模倣（レート制限回避）
        """
        self.use_guest_mode = use_guest_mode
        self.human_like = human_like
        self.request_count = 0
        self.last_request_time = 0
        self.session_start_time = time.time()
        
        if use_guest_mode:
            self.client = GuestClient()
        else:
            self.client = Client('ja-JP')  # 日本語設定
    async def human_delay(self):
        """人間らしい待機時間を作る"""
        if not self.human_like:
            return
        
        self.request_count += 1
        current_time = time.time()
        
        # 基本的なランダム遅延（1-3秒）
        base_delay = random.uniform(1.0, 3.0)
        
        # リクエスト数に応じた追加遅延
        if self.request_count % 10 == 0:
            # 10リクエストごとに長めの休憩（5-10秒）
            base_delay += random.uniform(5.0, 10.0)
            print(f"💤 長めの休憩中... ({base_delay:.1f}秒)")
        elif self.request_count % 5 == 0:
            # 5リクエストごとに中程度の休憩（2-5秒）
            base_delay += random.uniform(2.0, 5.0)
        
        # 前回リクエストから短時間の場合は追加遅延
        time_since_last = current_time - self.last_request_time
        if time_since_last < 2.0:
            base_delay += random.uniform(1.0, 3.0)
        
        # セッション時間に応じた疲労遅延
        session_duration = current_time - self.session_start_time
        if session_duration > 1800:  # 30分以上
            base_delay += random.uniform(2.0, 5.0)
        
        await asyncio.sleep(base_delay)
        self.last_request_time = time.time()

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
        """ユーザー情報取得（ユーザー名指定、@付き対応）"""
        try:
            # 人間らしい遅延
            await self.human_delay()
            
            # @記号を除去して正規化
            clean_username = self.normalize_username(username)
            
            if self.use_guest_mode:
                user = await self.client.get_user_by_screen_name(clean_username)
            else:
                user = await self.client.get_user_by_screen_name(clean_username)
            
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
            # エラー時は少し長めに待機
            if self.human_like:
                await asyncio.sleep(random.uniform(5.0, 10.0))
            return None

    async def get_user_info_by_id(self, user_id):
        """ユーザー情報取得（ユーザーID指定）"""
        try:
            if self.use_guest_mode:
                user = await self.client.get_user_by_id(str(user_id))
            else:
                user = await self.client.get_user_by_id(str(user_id))
            
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
            print(f"ユーザー情報取得エラー (ID: {user_id}): {e}")
            return None
    
    async def get_user_tweets(self, username, count=20):
        """ユーザーのツイート取得（ユーザー名指定、@付き対応）"""
        try:
            # 人間らしい遅延
            await self.human_delay()
            
            # @記号を除去して正規化
            clean_username = self.normalize_username(username)
            
            if self.use_guest_mode:
                user = await self.client.get_user_by_screen_name(clean_username)
                tweets = await self.client.get_user_tweets(user.id, count=count)
            else:
                user = await self.client.get_user_by_screen_name(clean_username)
                tweets = await self.client.get_user_tweets(user.id, count=count)
            
            results = []
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'username': clean_username,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'reply_count': tweet.reply_count,
                    'url': f"https://twitter.com/{clean_username}/status/{tweet.id}"
                }
                results.append(tweet_data)
            
            return results
            
        except Exception as e:
            print(f"ユーザーツイート取得エラー: {e}")
            # エラー時は少し長めに待機
            if self.human_like:
                await asyncio.sleep(random.uniform(5.0, 10.0))
            return []

    async def get_user_tweets_by_id(self, user_id, count=20):
        """ユーザーのツイート取得（ユーザーID指定）"""
        try:
            # まずユーザー情報を取得してユーザー名を取得
            user_info = await self.get_user_info_by_id(user_id)
            if not user_info:
                return []
            
            username = user_info['username']
            
            if self.use_guest_mode:
                tweets = await self.client.get_user_tweets(str(user_id), count=count)
            else:
                tweets = await self.client.get_user_tweets(str(user_id), count=count)
            
            results = []
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'username': username,
                    'user_id': user_id,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'reply_count': tweet.reply_count,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}"
                }
                results.append(tweet_data)
            
            return results
            
        except Exception as e:
            print(f"ユーザーツイート取得エラー (ID: {user_id}): {e}")
            return []

    async def get_multiple_users_tweets(self, usernames, count_per_user=20):
        """複数ユーザーのツイートを一括取得（ユーザー名指定）"""
        all_tweets = []
        
        for username in usernames:
            print(f"@{username} のツイートを取得中...")
            tweets = await self.get_user_tweets(username, count_per_user)
            all_tweets.extend(tweets)
            # human_delay は get_user_tweets 内で呼ばれるので追加の sleep は不要
        
        return all_tweets

    async def get_multiple_users_tweets_by_ids(self, user_ids, count_per_user=20):
        """複数ユーザーのツイートを一括取得（ユーザーID指定）"""
        all_tweets = []
        
        for user_id in user_ids:
            print(f"ID:{user_id} のツイートを取得中...")
            tweets = await self.get_user_tweets_by_id(user_id, count_per_user)
            all_tweets.extend(tweets)
            # human_delay は get_user_tweets_by_id 内で呼ばれるので追加の sleep は不要
        
        return all_tweets

    def normalize_username(self, identifier):
        """ユーザー名を正規化（@記号を除去）"""
        identifier = str(identifier).strip()
        if identifier.startswith('@'):
            return identifier[1:]
        return identifier

    async def get_user_tweets_flexible(self, identifier, count=20):
        """ユーザーのツイート取得（ユーザー名またはID自動判別、@付き対応）"""
        # @記号を除去
        clean_identifier = self.normalize_username(identifier)
        
        # 数字のみの場合はユーザーIDとして扱う
        if clean_identifier.isdigit():
            return await self.get_user_tweets_by_id(clean_identifier, count)
        else:
            return await self.get_user_tweets(clean_identifier, count)

    async def get_user_info_flexible(self, identifier):
        """ユーザー情報取得（ユーザー名またはID自動判別、@付き対応）"""
        # @記号を除去
        clean_identifier = self.normalize_username(identifier)
        
        # 数字のみの場合はユーザーIDとして扱う
        if clean_identifier.isdigit():
            return await self.get_user_info_by_id(clean_identifier)
        else:
            return await self.get_user_info(clean_identifier)

    def calculate_buzz_score(self, tweet):
        """バズ度を計算（エンゲージメント率のみベース、時間減衰なし）"""
        retweets = tweet.get('retweet_count', 0)
        likes = tweet.get('favorite_count', 0)
        replies = tweet.get('reply_count', 0)
        
        # エンゲージメントスコア（時間減衰なし）
        engagement_score = (retweets * 3) + (likes * 1) + (replies * 2)
        
        return engagement_score

    async def get_user_followers(self, username, count=100):
        """ユーザーのフォロワーリストを取得"""
        try:
            if self.use_guest_mode:
                user = await self.client.get_user_by_screen_name(username)
                followers = await self.client.get_user_followers(user.id, count=count)
            else:
                user = await self.client.get_user_by_screen_name(username)
                followers = await self.client.get_user_followers(user.id, count=count)
            
            follower_list = []
            for follower in followers:
                follower_data = {
                    'id': follower.id,
                    'username': follower.screen_name,
                    'name': follower.name,
                    'followers_count': follower.followers_count,
                    'verified': follower.verified
                }
                follower_list.append(follower_data)
            
            return follower_list
            
        except Exception as e:
            print(f"フォロワー取得エラー: {e}")
            return []

    def is_trending_tweet(self, tweet, min_engagement=50):
        """ツイートが伸びているかを判定"""
        retweets = tweet.get('retweet_count', 0)
        likes = tweet.get('favorite_count', 0)
        replies = tweet.get('reply_count', 0)
        
        total_engagement = retweets + likes + replies
        return total_engagement >= min_engagement

    async def get_trending_tweets_only(self, username, count=50, min_engagement=50):
        """指定ユーザーの伸びているツイートのみを取得"""
        try:
            all_tweets = await self.get_user_tweets(username, count)
            trending_tweets = [
                tweet for tweet in all_tweets 
                if self.is_trending_tweet(tweet, min_engagement)
            ]
            
            # バズ度を計算
            for tweet in trending_tweets:
                tweet['buzz_score'] = self.calculate_buzz_score(tweet)
            
            return trending_tweets
            
        except Exception as e:
            print(f"伸びツイート取得エラー ({username}): {e}")
            return []

    async def get_buzz_tweets_from_users_and_followers(self, main_usernames, follower_count=50, tweet_count_per_user=50, min_engagement=100, top_n=30):
        """指定ユーザーとそのフォロワーから伸びているツイートのみを取得"""
        all_trending_tweets = []
        processed_users = set()
        
        print(f"メインユーザー {len(main_usernames)}人とそのフォロワーから伸びツイートを収集中...")
        
        # メインユーザーの処理
        for main_user in main_usernames:
            if main_user in processed_users:
                continue
                
            print(f"\n@{main_user} の伸びツイートを取得中...")
            main_trending = await self.get_trending_tweets_only(
                main_user, tweet_count_per_user, min_engagement
            )
            all_trending_tweets.extend(main_trending)
            processed_users.add(main_user)
            
            # フォロワーを取得
            print(f"@{main_user} のフォロワーを取得中...")
            followers = await self.get_user_followers(main_user, follower_count)
            
            # フォロワーの伸びツイートを取得
            for i, follower in enumerate(followers, 1):
                follower_username = follower['username']
                
                if follower_username in processed_users:
                    continue
                    
                print(f"  ({i}/{len(followers)}) @{follower_username} の伸びツイートをチェック中...")
                
                # フォロワー数が少なすぎる場合はスキップ
                if follower['followers_count'] < 1000:
                    continue
                
                follower_trending = await self.get_trending_tweets_only(
                    follower_username, min(20, tweet_count_per_user), min_engagement
                )
                all_trending_tweets.extend(follower_trending)
                processed_users.add(follower_username)
                
                # human_delay がフォロワーツイート取得で呼ばれるので追加sleep不要
            
            # メインユーザー間の間隔（追加の休憩）
            if self.human_like:
                await asyncio.sleep(random.uniform(3.0, 7.0))
        
        if not all_trending_tweets:
            print("伸びているツイートが見つかりませんでした")
            return []
        
        print(f"\n合計 {len(all_trending_tweets)}件の伸びツイートを発見")
        
        # バズ度順にソート
        buzz_tweets = sorted(all_trending_tweets, key=lambda x: x['buzz_score'], reverse=True)
        
        return buzz_tweets[:top_n]

    async def get_buzz_tweets_from_users(self, usernames, count_per_user=50, top_n=20):
        """指定ユーザーからバズっているツイートを取得"""
        print(f"{len(usernames)}人のアカウントからツイートを取得中...")
        
        all_tweets = await self.get_multiple_users_tweets(usernames, count_per_user)
        
        if not all_tweets:
            return []
        
        # バズ度を計算
        for tweet in all_tweets:
            tweet['buzz_score'] = self.calculate_buzz_score(tweet)
        
        # バズ度順にソート
        buzz_tweets = sorted(all_tweets, key=lambda x: x['buzz_score'], reverse=True)
        
        return buzz_tweets[:top_n]
    
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
    # ゲストモードでの使用例（人間らしい動作有効）
    print("=== ゲストモードテスト（人間らしい動作ON） ===")
    guest_scraper = TwikitScraper(use_guest_mode=True, human_like=True)
    await guest_scraper.setup()
    
    # 単一ユーザーのツイート取得（ユーザー名指定）
    print("\n--- 単一ユーザーのツイート取得（ユーザー名） ---")
    tweets = await guest_scraper.get_user_tweets('jojou7777', count=5)
    
    print(f"取得したツイート数: {len(tweets)}")
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\n{i}. {tweet['text'][:100]}...")
        print(f"   日時: {tweet['created_at']}")
        print(f"   いいね: {tweet['favorite_count']}")
        print(f"   リツイート: {tweet['retweet_count']}")
    
    # ユーザーID直接指定でのツイート取得
    print("\n--- ユーザーID直接指定でのツイート取得 ---")
    user_id = "44196397"  # elonmuskのユーザーID例
    id_tweets = await guest_scraper.get_user_tweets_by_id(user_id, count=3)
    print(f"ID:{user_id} から取得したツイート数: {len(id_tweets)}")
    
    for i, tweet in enumerate(id_tweets, 1):
        print(f"\n{i}. @{tweet['username']}")
        print(f"   {tweet['text'][:100]}...")
        print(f"   いいね: {tweet['favorite_count']}")
    
    # フレキシブル指定（自動判別、@付き対応）
    print("\n--- フレキシブル指定（自動判別、@付き対応） ---")
    flexible_tweets1 = await guest_scraper.get_user_tweets_flexible('@jojou7777', count=2)
    flexible_tweets2 = await guest_scraper.get_user_tweets_flexible(user_id, count=2)
    flexible_tweets3 = await guest_scraper.get_user_tweets_flexible('jojou7777', count=2)
    print(f"@付きユーザー名指定: {len(flexible_tweets1)}件")
    print(f"ID指定: {len(flexible_tweets2)}件")
    print(f"通常ユーザー名指定: {len(flexible_tweets3)}件")
    
    # 指定ユーザーとフォロワーから伸びツイート取得
    print("\n--- 指定ユーザーとフォロワーから伸びツイート取得 ---")
    main_users = ['jojou7777','rei_0951']  # メインユーザー（界隈の中心人物）
    
    # 伸びツイートのみを効率的に収集
    buzz_tweets = await guest_scraper.get_buzz_tweets_from_users_and_followers(
        main_usernames=main_users,
        follower_count=30,        # 各メインユーザーから30人のフォロワーを調査
        tweet_count_per_user=30,  # 各ユーザーから最大30ツイートをチェック
        min_engagement=100,       # 最低エンゲージメント数（いいね+RT+返信）
        top_n=15                  # 最終的に上位15ツイートを取得
    )
    
    print(f"\n界隈のバズツイート TOP {len(buzz_tweets)}")
    for i, tweet in enumerate(buzz_tweets, 1):
        print(f"\n{i}. @{tweet['username']}")
        print(f"   {tweet['text'][:150]}...")
        print(f"   バズ度: {tweet['buzz_score']:.1f}")
        print(f"   いいね: {tweet['favorite_count']:,} | RT: {tweet['retweet_count']:,} | 返信: {tweet['reply_count']:,}")
        print(f"   URL: {tweet['url']}")
    
    # データ保存
    if buzz_tweets:
        guest_scraper.save_to_json(buzz_tweets, 'community_buzz_tweets.json')
    
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
    
    # 特定界隈のバズツイート取得
    tech_influencers = ['jojou7777', 'sundarpichai', 'satyanadella', 'tim_cook']
    buzz_tweets = await login_scraper.get_buzz_tweets_from_users(
        usernames=tech_influencers,
        count_per_user=50,
        top_n=20
    )
    
    # トレンド取得
    trends = await login_scraper.get_trending_topics()
    print(f"\nトレンド数: {len(trends)}")
    for trend in trends[:5]:
        print(f"  - {trend['name']}")
    """

if __name__ == "__main__":
    # インストールコマンド: pip install twikit
    asyncio.run(main())