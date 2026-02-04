import httpx
import feedparser
from typing import List, Dict, Any


class NewsTool:
    """Tool for fetching news headlines from RSS feeds (no API key required)."""

    RSS_FEED_URL = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    async def get_news(
        self,
        query: str = "India",
        max_articles: int = 5
    ) -> Dict[str, Any]:
        """
        Get top news headlines from Google News RSS feed.
        
        Args:
            query: Search query for news (default: "India")
            max_articles: Maximum number of articles to return
            
        Returns:
            Dictionary with news headlines
        """
        url = self.RSS_FEED_URL.format(query=query.replace(" ", "+"))
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                feed_content = response.text
            
            feed = feedparser.parse(feed_content)
            
            articles = []
            for entry in feed.entries[:max_articles]:
                articles.append({
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": entry.get("source", {}).get("title", "Unknown")
                })
            
            return {
                "query": query,
                "total_articles": len(articles),
                "articles": articles
            }
        
        except Exception as e:
            return {
                "error": f"Failed to fetch news: {str(e)}",
                "query": query,
                "articles": []
            }
