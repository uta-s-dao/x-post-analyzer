"use client";

import React from "react";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { useState } from "react";
import {
  BarChart3,
  Users,
  MessageSquare,
  TrendingUp,
  Settings,
  Menu,
  X,
} from "lucide-react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// サイドバーアイテムの定義
const sidebarItems = [
  { id: "dashboard", label: "ダッシュボード", icon: BarChart3 },
  { id: "followers", label: "フォロワー分析", icon: Users },
  { id: "tweets", label: "ツイート分析", icon: MessageSquare },
  { id: "engagement", label: "エンゲージメント", icon: TrendingUp },
  { id: "settings", label: "設定", icon: Settings },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [apiSettings, setApiSettings] = useState({
    isConnected: false,
    username: "",
  });
  const [showApiForm, setShowApiForm] = useState(false);

  // デバッグ用：状態をコンソールに出力
  React.useEffect(() => {
    console.log("isMobileMenuOpen:", isMobileMenuOpen);
    console.log("showApiForm:", showApiForm);
  }, [isMobileMenuOpen, showApiForm]);

  return (
    <html lang='ja'>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-50`}
      >
        <div className='flex h-screen overflow-hidden'>
          {/* モバイル用オーバーレイ */}
          {isMobileMenuOpen && (
            <div
              className='fixed inset-0 z-40 bg-opacity-50 lg:hidden'
              onClick={() => setIsMobileMenuOpen(false)}
            />
          )}

          {/* サイドバー */}
          <div
            className={`
            w-64 bg-white shadow-lg border-r border-gray-200 
            fixed left-0 top-0 h-full overflow-y-auto z-50
            transform transition-transform duration-300 ease-in-out
            lg:translate-x-0 lg:static lg:inset-0
            ${
              isMobileMenuOpen
                ? "translate-x-0"
                : "-translate-x-full lg:translate-x-0"
            }
          `}
          >
            {/* サイドバーヘッダー */}
            <div className='p-6 border-b border-gray-200'>
              <div className='flex items-center justify-between'>
                <div>
                  <h1 className='text-xl font-bold text-gray-900'>
                    X Analytics
                  </h1>
                  <div className='flex items-center mt-2'>
                    <div
                      className={`w-2 h-2 rounded-full mr-2 ${
                        apiSettings.isConnected ? "bg-green-500" : "bg-red-500"
                      }`}
                    ></div>
                    <p className='text-sm text-gray-600'>
                      {apiSettings.isConnected
                        ? `@${apiSettings.username}`
                        : "未接続"}
                    </p>
                  </div>
                </div>
                {/* モバイル用クローズボタン */}
                <button
                  onClick={() => setIsMobileMenuOpen(false)}
                  className='lg:hidden p-2 rounded-md hover:bg-gray-100'
                >
                  <X className='w-5 h-5' />
                </button>
              </div>

              {!apiSettings.isConnected && (
                <button
                  onClick={() => setShowApiForm(true)}
                  className='mt-3 w-full text-sm bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors'
                >
                  API接続
                </button>
              )}

              {apiSettings.isConnected && (
                <button
                  onClick={() =>
                    setApiSettings({ isConnected: false, username: "" })
                  }
                  className='mt-3 w-full text-sm bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors'
                >
                  接続解除
                </button>
              )}
            </div>

            {/* ナビゲーション */}
            <nav className='mt-6'>
              {sidebarItems.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveTab(item.id);
                      setIsMobileMenuOpen(false); // モバイルでメニュー選択時に閉じる
                    }}
                    className={`w-full flex items-center px-6 py-3 text-left hover:bg-blue-50 transition-colors ${
                      activeTab === item.id
                        ? "bg-blue-50 text-blue-600 border-r-2 border-blue-600"
                        : "text-gray-700"
                    }`}
                  >
                    <Icon className='w-5 h-5 mr-3 flex-shrink-0' />
                    <span className='truncate'>{item.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* メインコンテンツエリア */}
          <div className='flex-1 flex flex-col overflow-hidden'>
            {/* モバイル用ヘッダー */}
            <div className='lg:hidden bg-white border-b border-gray-200 p-4 flex items-center justify-between'>
              <button
                onClick={() => setIsMobileMenuOpen(true)}
                className='p-2 rounded-md hover:bg-gray-100'
              >
                <Menu className='w-6 h-6' />
              </button>
              <h2 className='text-lg font-semibold text-gray-900'>
                {sidebarItems.find((item) => item.id === activeTab)?.label}
              </h2>
              <div className='w-10' /> {/* スペーサー */}
            </div>

            {/* メインコンテンツ */}
            <main className='flex-1 overflow-y-auto'>
              <div className='p-4 flex items-center'>{children}</div>
            </main>
          </div>
        </div>

        {/* API設定フォーム（モーダル） */}
        {showApiForm && (
          <div
            className='fixed inset-0 z-50 flex items-center justify-center p-4'
            style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }}
          >
            <div className='bg-white rounded-lg shadow-xl p-6 w-full max-w-md'>
              <h3 className='text-lg font-semibold mb-4'>API接続設定</h3>
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  const formData = new FormData(e.currentTarget);
                  const apiKey = formData.get("apiKey") as string;
                  const username = formData.get("username") as string;

                  // API接続処理（実際の実装では、ここでAPIキーを検証）
                  if (apiKey && username) {
                    setApiSettings({
                      isConnected: true,
                      username: username.replace("@", ""),
                    });
                    setShowApiForm(false);
                  }
                }}
              >
                <div className='mb-4'>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    APIキー
                  </label>
                  <input
                    type='password'
                    name='apiKey'
                    required
                    className='w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                    placeholder='Your API Key'
                  />
                </div>
                <div className='mb-6'>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    ユーザー名
                  </label>
                  <input
                    type='text'
                    name='username'
                    required
                    className='w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                    placeholder='@username'
                  />
                </div>
                <div className='flex space-x-3'>
                  <button
                    type='button'
                    onClick={() => setShowApiForm(false)}
                    className='flex-1 px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors'
                  >
                    キャンセル
                  </button>
                  <button
                    type='submit'
                    className='flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors'
                  >
                    接続
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </body>
    </html>
  );
}
