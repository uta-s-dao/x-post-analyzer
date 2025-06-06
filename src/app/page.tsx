"use client";

import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import {
  // Calendar,
  TrendingUp,
  Users,
  MessageCircle,
  Heart,
  Repeat2,
  Eye,
  Settings,
  // Search,
  // Filter,
} from "lucide-react";

const XAnalyticsDashboard = () => {
  // const [selectedTimeRange, setSelectedTimeRange] = useState("7d");
  const [activeTab, setActiveTab] = useState("overview");
  const [apiSettings, setApiSettings] = useState({
    bearerToken: "",
    apiKey: "",
    apiSecretKey: "",
    accessToken: "",
    accessTokenSecret: "",
    isConnected: false,
    username: "",
  });
  const [showApiForm, setShowApiForm] = useState(false);

  // サンプルデータ
  const tweetData = [
    { date: "2025-05-29", tweets: 12, likes: 145, retweets: 23, replies: 8 },
    { date: "2025-05-30", tweets: 8, likes: 89, retweets: 15, replies: 12 },
    { date: "2025-05-31", tweets: 15, likes: 234, retweets: 45, replies: 18 },
    { date: "2025-06-01", tweets: 10, likes: 167, retweets: 32, replies: 14 },
    { date: "2025-06-02", tweets: 18, likes: 298, retweets: 67, replies: 25 },
    { date: "2025-06-03", tweets: 6, likes: 123, retweets: 28, replies: 9 },
    { date: "2025-06-04", tweets: 14, likes: 203, retweets: 41, replies: 16 },
  ];

  const engagementData = [
    { name: "いいね", value: 1259, color: "#ef4444" },
    { name: "リツイート", value: 251, color: "#22c55e" },
    { name: "リプライ", value: 102, color: "#3b82f6" },
    { name: "インプレッション", value: 15420, color: "#f59e0b" },
  ];

  const topTweets = [
    {
      id: 1,
      text: "Next.jsの新機能について調べてみた！App Routerが本当に便利で...",
      likes: 89,
      retweets: 23,
      replies: 12,
      date: "2025-06-02",
    },
    {
      id: 2,
      text: "TypeScriptのベストプラクティスについてまとめました",
      likes: 156,
      retweets: 45,
      replies: 18,
      date: "2025-06-01",
    },
    {
      id: 3,
      text: "React 19の新しいHooksが素晴らしい！特にuseOptimistic...",
      likes: 203,
      retweets: 67,
      replies: 25,
      date: "2025-05-31",
    },
  ];

  const sidebarItems = [
    { id: "overview", label: "概要", icon: TrendingUp },
    { id: "tweets", label: "投稿分析", icon: MessageCircle },
    { id: "engagement", label: "エンゲージメント", icon: Heart },
    { id: "followers", label: "フォロワー", icon: Users },
    { id: "trends", label: "トレンド", icon: TrendingUp },
    { id: "settings", label: "設定", icon: Settings },
  ];

  const handleApiConnect = () => {
    // API接続処理のシミュレーション
    if (
      apiSettings.bearerToken ||
      (apiSettings.apiKey && apiSettings.apiSecretKey)
    ) {
      setApiSettings((prev) => ({
        ...prev,
        isConnected: true,
        username: "your_username", // 実際にはAPIから取得
      }));
      setShowApiForm(false);
      alert("X APIに正常に接続されました！");
    } else {
      alert("必要な認証情報を入力してください。");
    }
  };

  const handleApiDisconnect = () => {
    setApiSettings({
      bearerToken: "",
      apiKey: "",
      apiSecretKey: "",
      accessToken: "",
      accessTokenSecret: "",
      isConnected: false,
      username: "",
    });
    alert("X APIから切断されました。");
  };

  return (
    <div className='min-h-screen bg-gray-50 flex'>
      {/* サイドバー */}
      <div className='w-64 bg-white shadow-lg border-r border-gray-200'>
        <div className='p-6 border-b border-gray-200'>
          <h1 className='text-xl font-bold text-gray-900'>X Analytics</h1>
          <div className='flex items-center mt-2'>
            <div
              className={`w-2 h-2 rounded-full mr-2 ${
                apiSettings.isConnected ? "bg-green-500" : "bg-red-500"
              }`}
            ></div>
            <p className='text-sm text-gray-600'>
              {apiSettings.isConnected ? `@${apiSettings.username}` : "未接続"}
            </p>
          </div>
          {!apiSettings.isConnected && (
            <button
              onClick={() => setShowApiForm(true)}
              className='mt-2 text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors'
            >
              API接続
            </button>
          )}
        </div>

        <nav className='mt-6'>
          {sidebarItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center px-6 py-3 text-left hover:bg-blue-50 transition-colors ${
                  activeTab === item.id
                    ? "bg-blue-50 text-blue-600 border-r-2 border-blue-600"
                    : "text-gray-700"
                }`}
              >
                <Icon className='w-5 h-5 mr-3' />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* メインコンテンツ */}
      <div className='flex-1 overflow-auto'>
        {/* ダッシュボードコンテンツ */}
        <div className='p-6'>
          {activeTab === "overview" && (
            <div className='space-y-6'>
              {/* KPIカード */}
              <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'>
                <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                  <div className='flex items-center justify-between'>
                    <div>
                      <p className='text-sm font-medium text-gray-600'>
                        総投稿数
                      </p>
                      <p className='text-2xl font-bold text-gray-900'>83</p>
                    </div>
                    <MessageCircle className='w-8 h-8 text-blue-600' />
                  </div>
                  <p className='text-sm text-green-600 mt-2'>
                    +12% from last week
                  </p>
                </div>

                <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                  <div className='flex items-center justify-between'>
                    <div>
                      <p className='text-sm font-medium text-gray-600'>
                        総いいね数
                      </p>
                      <p className='text-2xl font-bold text-gray-900'>1,259</p>
                    </div>
                    <Heart className='w-8 h-8 text-red-500' />
                  </div>
                  <p className='text-sm text-green-600 mt-2'>
                    +8% from last week
                  </p>
                </div>

                <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                  <div className='flex items-center justify-between'>
                    <div>
                      <p className='text-sm font-medium text-gray-600'>
                        リツイート数
                      </p>
                      <p className='text-2xl font-bold text-gray-900'>251</p>
                    </div>
                    <Repeat2 className='w-8 h-8 text-green-500' />
                  </div>
                  <p className='text-sm text-green-600 mt-2'>
                    +23% from last week
                  </p>
                </div>

                <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                  <div className='flex items-center justify-between'>
                    <div>
                      <p className='text-sm font-medium text-gray-600'>
                        インプレッション
                      </p>
                      <p className='text-2xl font-bold text-gray-900'>15.4K</p>
                    </div>
                    <Eye className='w-8 h-8 text-purple-500' />
                  </div>
                  <p className='text-sm text-green-600 mt-2'>
                    +15% from last week
                  </p>
                </div>
              </div>

              {/* チャート */}
              <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
                <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                  <h3 className='text-lg font-semibold text-gray-900 mb-4'>
                    投稿数の推移
                  </h3>
                  <ResponsiveContainer width='100%' height={300}>
                    <LineChart data={tweetData}>
                      <CartesianGrid strokeDasharray='3 3' />
                      <XAxis dataKey='date' />
                      <YAxis />
                      <Tooltip />
                      <Line
                        type='monotone'
                        dataKey='tweets'
                        stroke='#3b82f6'
                        strokeWidth={2}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                  <h3 className='text-lg font-semibold text-gray-900 mb-4'>
                    エンゲージメント分布
                  </h3>
                  <ResponsiveContainer width='100%' height={300}>
                    <PieChart>
                      <Pie
                        data={engagementData}
                        cx='50%'
                        cy='50%'
                        outerRadius={80}
                        fill='#8884d8'
                        dataKey='value'
                        label={({ name, percent }) =>
                          `${name} ${(percent * 100).toFixed(0)}%`
                        }
                      >
                        {engagementData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* 人気投稿 */}
              <div className='bg-white rounded-lg shadow-sm border border-gray-200'>
                <div className='p-6 border-b border-gray-200'>
                  <h3 className='text-lg font-semibold text-gray-900'>
                    人気の投稿
                  </h3>
                </div>
                <div className='divide-y divide-gray-200'>
                  {topTweets.map((tweet) => (
                    <div key={tweet.id} className='p-6'>
                      <p className='text-gray-900 mb-3'>{tweet.text}</p>
                      <div className='flex items-center justify-between text-sm text-gray-600'>
                        <span>{tweet.date}</span>
                        <div className='flex items-center space-x-4'>
                          <span className='flex items-center'>
                            <Heart className='w-4 h-4 mr-1' />
                            {tweet.likes}
                          </span>
                          <span className='flex items-center'>
                            <Repeat2 className='w-4 h-4 mr-1' />
                            {tweet.retweets}
                          </span>
                          <span className='flex items-center'>
                            <MessageCircle className='w-4 h-4 mr-1' />
                            {tweet.replies}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === "tweets" && (
            <div className='space-y-6'>
              <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                <h3 className='text-lg font-semibold text-gray-900 mb-4'>
                  投稿パフォーマンス
                </h3>
                <ResponsiveContainer width='100%' height={400}>
                  <BarChart data={tweetData}>
                    <CartesianGrid strokeDasharray='3 3' />
                    <XAxis dataKey='date' />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey='tweets' fill='#3b82f6' name='投稿数' />
                    <Bar dataKey='likes' fill='#ef4444' name='いいね' />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* 他のタブのコンテンツも同様に追加可能 */}
          {activeTab === "settings" && (
            <div className='space-y-6'>
              <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                <h3 className='text-lg font-semibold text-gray-900 mb-4'>
                  X API設定
                </h3>

                {apiSettings.isConnected ? (
                  <div className='space-y-4'>
                    <div className='flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg'>
                      <div className='flex items-center'>
                        <div className='w-3 h-3 bg-green-500 rounded-full mr-3'></div>
                        <div>
                          <p className='font-medium text-green-900'>接続済み</p>
                          <p className='text-sm text-green-700'>
                            @{apiSettings.username}
                          </p>
                        </div>
                      </div>
                      <button
                        onClick={handleApiDisconnect}
                        className='px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors'
                      >
                        切断
                      </button>
                    </div>

                    <div className='grid grid-cols-1 md:grid-cols-2 gap-4 mt-6'>
                      <div className='p-4 border border-gray-200 rounded-lg'>
                        <h4 className='font-medium text-gray-900 mb-2'>
                          API利用状況
                        </h4>
                        <p className='text-sm text-gray-600'>
                          月間リクエスト数: 1,247 / 10,000
                        </p>
                        <div className='w-full bg-gray-200 rounded-full h-2 mt-2'>
                          <div
                            className='bg-blue-600 h-2 rounded-full'
                            style={{ width: "12.47%" }}
                          ></div>
                        </div>
                      </div>

                      <div className='p-4 border border-gray-200 rounded-lg'>
                        <h4 className='font-medium text-gray-900 mb-2'>
                          最終同期
                        </h4>
                        <p className='text-sm text-gray-600'>
                          2025年6月5日 14:32
                        </p>
                        <button className='mt-2 text-xs bg-gray-600 text-white px-3 py-1 rounded hover:bg-gray-700 transition-colors'>
                          今すぐ同期
                        </button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className='text-center py-8'>
                    <div className='w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4'>
                      <Settings className='w-8 h-8 text-gray-400' />
                    </div>
                    <h4 className='text-lg font-medium text-gray-900 mb-2'>
                      X APIに接続してください
                    </h4>
                    <p className='text-gray-600 mb-6'>
                      アカウントデータを分析するためには、X
                      APIの認証情報が必要です。
                    </p>
                    <button
                      onClick={() => setShowApiForm(true)}
                      className='px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors'
                    >
                      API認証情報を設定
                    </button>
                  </div>
                )}
              </div>

              {/* データ設定 */}
              <div className='bg-white p-6 rounded-lg shadow-sm border border-gray-200'>
                <h3 className='text-lg font-semibold text-gray-900 mb-4'>
                  データ設定
                </h3>
                <div className='space-y-4'>
                  <div className='flex items-center justify-between'>
                    <div>
                      <p className='font-medium text-gray-900'>
                        自動データ更新
                      </p>
                      <p className='text-sm text-gray-600'>
                        1時間ごとに最新データを取得
                      </p>
                    </div>
                    <label className='relative inline-flex items-center cursor-pointer'>
                      <input
                        type='checkbox'
                        className='sr-only peer'
                        defaultChecked
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className='flex items-center justify-between'>
                    <div>
                      <p className='font-medium text-gray-900'>
                        データ保存期間
                      </p>
                      <p className='text-sm text-gray-600'>
                        分析データの保存期間を設定
                      </p>
                    </div>
                    <select className='border border-gray-300 rounded-lg px-3 py-2'>
                      <option>30日</option>
                      <option>90日</option>
                      <option>1年</option>
                      <option>無制限</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab !== "overview" &&
            activeTab !== "tweets" &&
            activeTab !== "settings" && (
              <div className='bg-white p-8 rounded-lg shadow-sm border border-gray-200 text-center'>
                {!apiSettings.isConnected ? (
                  <div>
                    <h3 className='text-xl font-semibold text-gray-900 mb-2'>
                      API接続が必要です
                    </h3>
                    <p className='text-gray-600 mb-4'>
                      このセクションを利用するには、まずX
                      APIに接続してください。
                    </p>
                    <button
                      onClick={() => setActiveTab("settings")}
                      className='px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors'
                    >
                      設定画面へ
                    </button>
                  </div>
                ) : (
                  <div>
                    <h3 className='text-xl font-semibold text-gray-900 mb-2'>
                      {
                        sidebarItems.find((item) => item.id === activeTab)
                          ?.label
                      }
                    </h3>
                    <p className='text-gray-600'>このセクションは開発中です</p>
                  </div>
                )}
              </div>
            )}
        </div>
      </div>

      {/* API設定モーダル */}
      {showApiForm && (
        <div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4'>
          <div className='bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto'>
            <div className='p-6 border-b border-gray-200'>
              <h3 className='text-lg font-semibold text-gray-900'>
                X API認証設定
              </h3>
              <p className='text-sm text-gray-600 mt-1'>
                X Developer Portalで取得した認証情報を入力してください
              </p>
            </div>

            <div className='p-6 space-y-4'>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-2'>
                  Bearer Token（推奨）
                </label>
                <input
                  type='password'
                  value={apiSettings.bearerToken}
                  onChange={(e) =>
                    setApiSettings((prev) => ({
                      ...prev,
                      bearerToken: e.target.value,
                    }))
                  }
                  placeholder='AAAAAAAAAAAAAAAAAAAAAA...'
                  className='w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                />
                <p className='text-xs text-gray-500 mt-1'>
                  読み取り専用分析の場合はBearer Tokenのみで十分です
                </p>
              </div>

              <div className='border-t border-gray-200 pt-4'>
                <p className='text-sm font-medium text-gray-700 mb-3'>
                  または OAuth 1.0a認証情報を使用:
                </p>

                <div className='space-y-3'>
                  <div>
                    <label className='block text-sm font-medium text-gray-700 mb-1'>
                      API Key
                    </label>
                    <input
                      type='password'
                      value={apiSettings.apiKey}
                      onChange={(e) =>
                        setApiSettings((prev) => ({
                          ...prev,
                          apiKey: e.target.value,
                        }))
                      }
                      placeholder='abcdefghijklmnopqrstuvwxyz'
                      className='w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                    />
                  </div>

                  <div>
                    <label className='block text-sm font-medium text-gray-700 mb-1'>
                      API Secret Key
                    </label>
                    <input
                      type='password'
                      value={apiSettings.apiSecretKey}
                      onChange={(e) =>
                        setApiSettings((prev) => ({
                          ...prev,
                          apiSecretKey: e.target.value,
                        }))
                      }
                      placeholder='abcdefghijklmnopqrstuvwxyz123456789'
                      className='w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                    />
                  </div>

                  <div>
                    <label className='block text-sm font-medium text-gray-700 mb-1'>
                      Access Token（投稿機能用）
                    </label>
                    <input
                      type='password'
                      value={apiSettings.accessToken}
                      onChange={(e) =>
                        setApiSettings((prev) => ({
                          ...prev,
                          accessToken: e.target.value,
                        }))
                      }
                      placeholder='123456789-abcdefghijklmnopqrstuvwxyz'
                      className='w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                    />
                  </div>

                  <div>
                    <label className='block text-sm font-medium text-gray-700 mb-1'>
                      Access Token Secret（投稿機能用）
                    </label>
                    <input
                      type='password'
                      value={apiSettings.accessTokenSecret}
                      onChange={(e) =>
                        setApiSettings((prev) => ({
                          ...prev,
                          accessTokenSecret: e.target.value,
                        }))
                      }
                      placeholder='abcdefghijklmnopqrstuvwxyz123456789'
                      className='w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                    />
                  </div>
                </div>
              </div>

              <div className='bg-blue-50 p-4 rounded-lg'>
                <h4 className='text-sm font-medium text-blue-900 mb-2'>
                  認証情報の取得方法:
                </h4>
                <ol className='text-xs text-blue-800 space-y-1'>
                  <li>
                    1.{" "}
                    <a
                      href='https://developer.twitter.com'
                      target='_blank'
                      rel='noopener noreferrer'
                      className='underline'
                    >
                      X Developer Portal
                    </a>
                    にアクセス
                  </li>
                  <li>2. アプリを作成またはプロジェクトを選択</li>
                  <li>3. Keys and Tokensから認証情報を取得</li>
                  <li>4. 必要な権限を設定（Read, Write, DM等）</li>
                </ol>
              </div>
            </div>

            <div className='p-6 border-t border-gray-200 flex justify-end space-x-3'>
              <button
                onClick={() => setShowApiForm(false)}
                className='px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors'
              >
                キャンセル
              </button>
              <button
                onClick={handleApiConnect}
                className='px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors'
              >
                接続
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default XAnalyticsDashboard;
