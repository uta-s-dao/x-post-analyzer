"use client";

import { useState } from "react";

interface TwitterPostProps {
  defaultText?: string;
  onSuccess?: (data: []) => void;
  onError?: (error: string) => void;
}

export default function TwitterPost({
  defaultText = "",
  onSuccess,
  onError,
}: TwitterPostProps) {
  const [tweetText, setTweetText] = useState(defaultText);
  const [isPosting, setIsPosting] = useState(false);
  const [message, setMessage] = useState("");

  const postToTwitter = async () => {
    if (!tweetText.trim()) {
      setMessage("ツイート内容を入力してください");
      return;
    }

    setIsPosting(true);
    setMessage("");

    try {
      const response = await fetch("/api/tweet", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tweetData: tweetText }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("ツイートが投稿されました！");
        setTweetText("");
        onSuccess?.(data);
      } else {
        setMessage(`エラー: ${data.error}`);
        onError?.(data.error);
      }
    } catch {
      const errorMsg = "ツイートの投稿に失敗しました";
      setMessage(errorMsg);
      onError?.(errorMsg);
    } finally {
      setIsPosting(false);
    }
  };

  return (
    <div className='max-w-md mx-auto p-6 bg-white rounded-lg'>
      <h2 className='text-2xl font-bold mb-4 text-center text-gray-900'>
        Twitter投稿
      </h2>

      <textarea
        value={tweetText}
        onChange={(e) => setTweetText(e.target.value)}
        placeholder='ポストを書いてください'
        className='w-full p-3 border border-gray-300 text-gray-900 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500'
        rows={4}
        maxLength={280}
        disabled={isPosting}
      />

      <div className='flex text-gray-900 justify-between items-center mt-2 mb-4'>
        <span
          className={`text-sm ${
            tweetText.length > 260 ? "text-red-500" : "text-gray-500"
          }`}
        >
          {tweetText.length}/280
        </span>
      </div>

      <button
        onClick={postToTwitter}
        disabled={isPosting || !tweetText.trim()}
        className={`w-full py-2 px-4 rounded-md font-medium transition-colors ${
          isPosting || !tweetText.trim()
            ? "bg-gray-300 cursor-not-allowed"
            : "bg-blue-500 hover:bg-blue-600 text-white"
        }`}
      >
        {isPosting ? "投稿中..." : "ツイート"}
      </button>

      {message && (
        <div
          className={`mt-4 p-3 rounded-md ${
            message.includes("エラー") || message.includes("失敗")
              ? "bg-red-100 text-red-700"
              : "bg-green-100 text-green-700"
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
}
