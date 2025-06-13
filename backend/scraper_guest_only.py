# guest_only_scraper.py
import asyncio
import json
import random
import time
from twikit.guest import GuestClient

class GuestTwikitScraper:
    def __init__(self, human_like=True):
        """
        ゲスト専用Twikitスクレイパーの初期化
        
        Args:
            human_like (bool): 人間らしい動作を模倣（レート制限回避）
        """
        self.human_like = human_like
        self.request_count = 0
        self.last_request_time = 0
        self.session_start_time = time.time()
        self.client = GuestClient()
    
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

    async def setup(self):
        """セットアップ"""
        await self.client.activate()
        print("ゲストモードで接続しました")

    def normalize_username(self, identifier):
        """ユーザー名を正規化（@記号を除去）"""
        identifier = str(identifier).strip()
        if identifier.startswith('@'):
            return identifier[1:]
        return identifier

    async def get_user_info(self, username):
        """ユーザー情報取得（ユーザー名指定、@付き対応）"""
        try:
            await self.human_delay()
            clean_username = self.normalize_username(username)
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
            if self.human_like:
                await asyncio.sleep(random.uniform(5.0, 10.0))
            return None

    async def get_user_info_by_id(self, user_id):
        """ユーザー情報取得（ユーザーID指定）"""
        try:
            await self.human_delay()
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
            if self.human_like:
                await asyncio.sleep(random.uniform(5.0, 10.0))
            return None
    
    async def get_user_tweets(self, username, count=20):
        """ユーザーのツイート取得（ユーザー名指定、@付き対応）"""
        try:
            await self.human_delay()
            clean_username = self.normalize_username(username)
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
            if self.human_like:
                await asyncio.sleep(random.uniform(5.0, 10.0))
            return []

    async def get_user_tweets_by_id(self, user_id, count=20):
        """ユーザーのツイート取得（ユーザーID指定）"""
        try:
            user_info = await self.get_user_info_by_id(user_id)
            if not user_info:
                return []
            
            username = user_info['username']
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
            if self.human_like:
                await asyncio.sleep(random.uniform(5.0, 10.0))
            return []

    async def get_multiple_users_tweets(self, usernames, count_per_user=20):
        """複数ユーザーのツイートを一括取得（ユーザー名指定）"""
        all_tweets = []
        
        for username in usernames:
            print(f"@{username} のツイートを取得中...")
            tweets = await self.get_user_tweets(username, count_per_user)
            all_tweets.extend(tweets)
        
        return all_tweets

    async def get_multiple_users_tweets_by_ids(self, user_ids, count_per_user=20):
        """複数ユーザーのツイートを一括取得（ユーザーID指定）"""
        all_tweets = []
        
        for user_id in user_ids:
            print(f"ID:{user_id} のツイートを取得中...")
            tweets = await self.get_user_tweets_by_id(user_id, count_per_user)
            all_tweets.extend(tweets)
        
        return all_tweets

    async def get_user_tweets_flexible(self, identifier, count=20):
        """ユーザーのツイート取得（ユーザー名またはID自動判別、@付き対応）"""
        clean_identifier = self.normalize_username(identifier)
        
        if clean_identifier.isdigit():
            return await self.get_user_tweets_by_id(clean_identifier, count)
        else:
            return await self.get_user_tweets(clean_identifier, count)

    async def get_user_info_flexible(self, identifier):
        """ユーザー情報取得（ユーザー名またはID自動判別、@付き対応）"""
        clean_identifier = self.normalize_username(identifier)
        
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
            await self.human_delay()
            clean_username = self.normalize_username(username)
            user = await self.client.get_user_by_screen_name(clean_username)
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
            if self.human_like:
                await asyncio.sleep(random.uniform(5.0, 10.0))
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
        
        for main_user in main_usernames:
            if main_user in processed_users:
                continue
                
            print(f"\n@{main_user} の伸びツイートを取得中...")
            main_trending = await self.get_trending_tweets_only(
                main_user, tweet_count_per_user, min_engagement
            )
            all_trending_tweets.extend(main_trending)
            processed_users.add(main_user)
            
            print(f"@{main_user} のフォロワーを取得中...")
            followers = await self.get_user_followers(main_user, follower_count)
            
            for i, follower in enumerate(followers, 1):
                follower_username = follower['username']
                
                if follower_username in processed_users:
                    continue
                    
                print(f"  ({i}/{len(followers)}) @{follower_username} の伸びツイートをチェック中...")
                
                if follower['followers_count'] < 1000:
                    continue
                
                follower_trending = await self.get_trending_tweets_only(
                    follower_username, min(20, tweet_count_per_user), min_engagement
                )
                all_trending_tweets.extend(follower_trending)
                processed_users.add(follower_username)
            
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
    
    async def search_user_tweets(self, username, keyword, count=50):
        """特定ユーザーのツイートからキーワード検索"""
        try:
            print(f"@{username} のツイートから '{keyword}' を検索中...")
            
            # ユーザーのツイートを取得
            all_tweets = await self.get_user_tweets(username, count)
            
            # キーワードでフィルタリング
            keyword_lower = keyword.lower()
            matching_tweets = []
            
            for tweet in all_tweets:
                if keyword_lower in tweet['text'].lower():
                    # バズ度を計算
                    tweet['buzz_score'] = self.calculate_buzz_score(tweet)
                    tweet['search_keyword'] = keyword
                    matching_tweets.append(tweet)
            
            # バズ度順にソート
            matching_tweets.sort(key=lambda x: x['buzz_score'], reverse=True)
            
            return matching_tweets
            
        except Exception as e:
            print(f"ユーザーツイート検索エラー ({username}): {e}")
            return []

    async def search_multiple_users_tweets(self, usernames, keyword, count_per_user=50, top_n=20):
        """複数ユーザーのツイートからキーワード検索"""
        all_matching_tweets = []
        
        print(f"{len(usernames)}人のユーザーから '{keyword}' を検索中...")
        
        for username in usernames:
            matching_tweets = await self.search_user_tweets(username, keyword, count_per_user)
            all_matching_tweets.extend(matching_tweets)
        
        if not all_matching_tweets:
            print(f"キーワード '{keyword}' に一致するツイートが見つかりませんでした")
            return []
        
        # バズ度順にソート
        all_matching_tweets.sort(key=lambda x: x['buzz_score'], reverse=True)
        
        return all_matching_tweets[:top_n]

    async def search_followers_tweets(self, main_username, keyword, follower_count=30, tweet_count_per_user=30, top_n=15):
        """メインユーザーとそのフォロワーのツイートからキーワード検索"""
        all_matching_tweets = []
        processed_users = set()
        
        print(f"@{main_username} とフォロワーから '{keyword}' を検索中...")
        
        # メインユーザーから検索
        main_matches = await self.search_user_tweets(main_username, keyword, tweet_count_per_user)
        all_matching_tweets.extend(main_matches)
        processed_users.add(main_username)
        
        # フォロワーを取得
        followers = await self.get_user_followers(main_username, follower_count)
        
        # フォロワーのツイートから検索
        for i, follower in enumerate(followers, 1):
            follower_username = follower['username']
            
            if follower_username in processed_users:
                continue
                
            print(f"  ({i}/{len(followers)}) @{follower_username} のツイートを検索中...")
            
            # フォロワー数が少ない場合はスキップ
            if follower['followers_count'] < 1000:
                continue
            
            follower_matches = await self.search_user_tweets(
                follower_username, keyword, min(20, tweet_count_per_user)
            )
            all_matching_tweets.extend(follower_matches)
            processed_users.add(follower_username)
        
        if not all_matching_tweets:
            print(f"キーワード '{keyword}' に一致するツイートが見つかりませんでした")
            return []
        
        print(f"\n合計 {len(all_matching_tweets)}件のマッチするツイートを発見")
        
        # バズ度順にソート
        all_matching_tweets.sort(key=lambda x: x['buzz_score'], reverse=True)
        
        return all_matching_tweets[:top_n]

    def save_to_json(self, data, filename):
        """JSONファイルに保存"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"データを {filename} に保存しました")

# 使用例
async def main():
    # ゲスト専用スクレイパー（人間らしい動作ON）
    print("=== ゲスト専用スクレイパー ===")
    scraper = GuestTwikitScraper(human_like=True)
    await scraper.setup()
    
    # 単一ユーザーのツイート取得
    print("\n--- 単一ユーザーのツイート取得 ---")
    tweets = await scraper.get_user_tweets('@jojou7777', count=5)
    print(f"取得したツイート数: {len(tweets)}")
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\n{i}. {tweet['text'][:100]}...")
        print(f"   日時: {tweet['created_at']}")
        print(f"   いいね: {tweet['favorite_count']}")
        print(f"   リツイート: {tweet['retweet_count']}")
    
    # ユーザーID直接指定
    print("\n--- ユーザーID直接指定 ---")
    user_id = "44196397"
    id_tweets = await scraper.get_user_tweets_by_id(user_id, count=3)
    print(f"ID:{user_id} から取得したツイート数: {len(id_tweets)}")
    
    # フレキシブル指定（@付き対応）
    print("\n--- フレキシブル指定 ---")
    flexible_tweets1 = await scraper.get_user_tweets_flexible('@jojou7777', count=2)
    flexible_tweets2 = await scraper.get_user_tweets_flexible(user_id, count=2)
    print(f"@付きユーザー名指定: {len(flexible_tweets1)}件")
    print(f"ID指定: {len(flexible_tweets2)}件")
    
    # 界隈のバズツイート取得
    print("\n--- 界隈のバズツイート取得 ---")
    main_users = ['jojou7777', 'rei_0951']
    
    buzz_tweets = await scraper.get_buzz_tweets_from_users_and_followers(
        main_usernames=main_users,
        follower_count=30,
        tweet_count_per_user=30,
        min_engagement=100,
        top_n=15
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
        scraper.save_to_json(buzz_tweets, 'community_buzz_tweets.json')
    
    # キーワード検索機能のテスト
    print("\n--- キーワード検索テスト ---")
    
    # 単一ユーザーからキーワード検索
    keyword_tweets = await scraper.search_user_tweets('jojou7777', 'Python', count=30)
    print(f"@jojou7777 から 'Python' を検索: {len(keyword_tweets)}件")
    
    # 複数ユーザーからキーワード検索
    multi_search = await scraper.search_multiple_users_tweets(
        usernames=['jojou7777', 'rei_0951'],
        keyword='AI',
        count_per_user=30,
        top_n=10
    )
    print(f"複数ユーザーから 'AI' を検索: {len(multi_search)}件")
    
    # フォロワー込みでキーワード検索
    follower_search = await scraper.search_followers_tweets(
        main_username='jojou7777',
        keyword='プログラミング',
        follower_count=20,
        top_n=10
    )
    print(f"フォロワー込みで 'プログラミング' を検索: {len(follower_search)}件")
    
    # 検索結果の表示例
    if keyword_tweets:
        print(f"\n=== '{keyword_tweets[0]['search_keyword']}' 検索結果 TOP 3 ===")
        for i, tweet in enumerate(keyword_tweets[:3], 1):
            print(f"\n{i}. @{tweet['username']}")
            print(f"   {tweet['text'][:100]}...")
            print(f"   バズ度: {tweet['buzz_score']:.1f}")
            print(f"   エンゲージメント: ❤️{tweet['favorite_count']} 🔄{tweet['retweet_count']} 💬{tweet['reply_count']}")
            print(f"   URL: {tweet['url']}")

if __name__ == "__main__":
    # インストールコマンド: pip install twikit
    asyncio.run(main())