// // app/api/posts/route.ts
// import { NextRequest, NextResponse } from "next/server";
// import { TwitterApi } from "twitter-api-v2";

// // 投稿データの型定義
// interface ScheduledPost {
//   id: string;
//   content: string;
//   scheduledAt: string;
//   status: "pending" | "posted" | "failed";
//   createdAt: string;
// }

// // メモリ上のストレージ（実際の本番環境ではデータベースを使用）
// let scheduledPosts: ScheduledPost[] = [];

// // Twitter API クライアントの初期化
// const twitterClient = new TwitterApi({
//   appKey: process.env.TWITTER_API_KEY!,
//   appSecret: process.env.TWITTER_API_SECRET!,
//   accessToken: process.env.TWITTER_ACCESS_TOKEN!,
//   accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET!,
// });

// export async function GET(request: NextRequest) {
//   try {
//     // 予約投稿一覧を取得
//     return NextResponse.json({
//       success: true,
//       posts: scheduledPosts,
//     });
//   } catch (error) {
//     return NextResponse.json(
//       { success: false, error: "Failed to fetch posts" },
//       { status: 500 }
//     );
//   }
// }

// export async function POST(request: NextRequest) {
//   try {
//     const { content, scheduledAt } = await request.json();

//     // バリデーション
//     if (!content || !scheduledAt) {
//       return NextResponse.json(
//         { success: false, error: "Content and scheduledAt are required" },
//         { status: 400 }
//       );
//     }

//     const scheduledDate = new Date(scheduledAt);
//     const now = new Date();

//     if (scheduledDate <= now) {
//       return NextResponse.json(
//         { success: false, error: "Scheduled time must be in the future" },
//         { status: 400 }
//       );
//     }

//     // 新しい予約投稿を作成
//     const newPost: ScheduledPost = {
//       id: Date.now().toString(),
//       content,
//       scheduledAt,
//       status: "pending",
//       createdAt: new Date().toISOString(),
//     };

//     scheduledPosts.push(newPost);

//     // スケジュールされた時間に投稿を実行
//     schedulePost(newPost);

//     return NextResponse.json({
//       success: true,
//       post: newPost,
//     });
//   } catch (error) {
//     return NextResponse.json(
//       { success: false, error: "Failed to schedule post" },
//       { status: 500 }
//     );
//   }
// }

// export async function DELETE(request: NextRequest) {
//   try {
//     const { searchParams } = new URL(request.url);
//     const postId = searchParams.get("id");

//     if (!postId) {
//       return NextResponse.json(
//         { success: false, error: "Post ID is required" },
//         { status: 400 }
//       );
//     }

//     const postIndex = scheduledPosts.findIndex((post) => post.id === postId);

//     if (postIndex === -1) {
//       return NextResponse.json(
//         { success: false, error: "Post not found" },
//         { status: 404 }
//       );
//     }

//     const post = scheduledPosts[postIndex];

//     if (post.status === "posted") {
//       return NextResponse.json(
//         { success: false, error: "Cannot delete already posted content" },
//         { status: 400 }
//       );
//     }

//     scheduledPosts.splice(postIndex, 1);

//     return NextResponse.json({
//       success: true,
//       message: "Post cancelled successfully",
//     });
//   } catch (error) {
//     return NextResponse.json(
//       { success: false, error: "Failed to cancel post" },
//       { status: 500 }
//     );
//   }
// }

// // 投稿をスケジュールする関数
// function schedulePost(post: ScheduledPost) {
//   const scheduledTime = new Date(post.scheduledAt).getTime();
//   const currentTime = new Date().getTime();
//   const delay = scheduledTime - currentTime;

//   setTimeout(async () => {
//     try {
//       // Twitter APIを使って投稿
//       await twitterClient.v2.tweet(post.content);

//       // ステータスを更新
//       const postIndex = scheduledPosts.findIndex((p) => p.id === post.id);
//       if (postIndex !== -1) {
//         scheduledPosts[postIndex].status = "posted";
//       }

//       console.log(`Tweet posted successfully: ${post.content}`);
//     } catch (error) {
//       console.error("Failed to post tweet:", error);

//       // エラー時のステータス更新
//       const postIndex = scheduledPosts.findIndex((p) => p.id === post.id);
//       if (postIndex !== -1) {
//         scheduledPosts[postIndex].status = "failed";
//       }
//     }
//   }, delay);
// }
