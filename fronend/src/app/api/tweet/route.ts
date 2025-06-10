import { NextRequest, NextResponse } from "next/server";
import { TwitterApi } from "twitter-api-v2";

export async function POST(request: NextRequest) {
  try {
    const { tweetData } = await request.json();

    if (!tweetData) {
      return NextResponse.json(
        { error: "Tweet data is required" },
        { status: 400 }
      );
    }

    // Twitter API クライアントの初期化
    const client = new TwitterApi({
      appKey: process.env.TWITTER_API_KEY!,
      appSecret: process.env.TWITTER_API_SECRET!,
      accessToken: process.env.TWITTER_ACCESS_TOKEN_KEY!,
      accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET!,
    });

    const twitterClient = client.readWrite;
    const data = await twitterClient.v2.tweet(tweetData);

    return NextResponse.json({
      success: true,
      tweet: data,
      message: "Tweet posted successfully",
    });
  } catch (error) {
    console.error("Twitter API Error:", error);
    return NextResponse.json(
      { error: "Failed to post tweet" },
      { status: 500 }
    );
  }
}
