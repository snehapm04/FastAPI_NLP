from twitter_client import search_tweets, get_direct_replies

async def fetch_main_and_direct_comments(query: str, post_limit: int, reply_limit: int):
    main_posts = await search_tweets(query=query, max_results=post_limit)
    result = {}
    for post in main_posts:
        text = post["text"]
        conversation_id = post["conversation_id"]
        author_id = post["author_id"]

        replies = await get_direct_replies(conversation_id=conversation_id, author_id=author_id, max_results=reply_limit)
        reply_texts = [r["text"] for r in replies] if replies else []
        result[text] = reply_texts
    return result
