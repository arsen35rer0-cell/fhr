# main.py
import webview
import asyncio
import aiohttp
import time
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SiteConfig:
    name: str
    url: str
    check_type: str  # "status", "text_absent"
    absent_text: str = ""

SITES: List[SiteConfig] = [
    SiteConfig("GitHub", "https://github.com/{}", "status"),
    SiteConfig("VK", "https://vk.com/{}", "status"),
    SiteConfig("Telegram", "https://t.me/{}", "text_absent", "If you have <strong>Telegram</strong>, you can contact"),
    SiteConfig("Reddit", "https://www.reddit.com/user/{}", "status"),
    SiteConfig("Twitter/X", "https://x.com/{}", "status"),
    SiteConfig("Instagram", "https://www.instagram.com/{}/", "status"),
    SiteConfig("TikTok", "https://www.tiktok.com/@{}", "status"),
    SiteConfig("YouTube", "https://www.youtube.com/@{}", "status"),
    SiteConfig("Steam", "https://steamcommunity.com/id/{}", "text_absent", "The specified profile could not be found"),
    SiteConfig("Twitch", "https://www.twitch.tv/{}", "status"),
    SiteConfig("Pinterest", "https://www.pinterest.com/{}/", "status"),
    SiteConfig("SoundCloud", "https://soundcloud.com/{}", "status"),
    SiteConfig("Medium", "https://medium.com/@{}", "status"),
    SiteConfig("DeviantArt", "https://www.deviantart.com/{}", "status"),
    SiteConfig("Flickr", "https://www.flickr.com/people/{}", "status"),
    SiteConfig("Keybase", "https://keybase.io/{}", "status"),
    SiteConfig("HackerNews", "https://news.ycombinator.com/user?id={}", "text_absent", "No such user."),
    SiteConfig("GitLab", "https://gitlab.com/{}", "status"),
    SiteConfig("BitBucket", "https://bitbucket.org/{}/", "status"),
    SiteConfig("DockerHub", "https://hub.docker.com/u/{}/", "status"),
    SiteConfig("Kaggle", "https://www.kaggle.com/{}", "status"),
    SiteConfig("LeetCode", "https://leetcode.com/{}", "status"),
    SiteConfig("Codeforces", "https://codeforces.com/profile/{}", "text_absent", "User not found"),
    SiteConfig("Habr", "https://habr.com/ru/users/{}", "status"),
    SiteConfig("Pikabu", "https://pikabu.ru/@{}", "status"),
    SiteConfig("OK.ru", "https://ok.ru/{}", "status"),
    SiteConfig("Zhihu", "https://www.zhihu.com/people/{}", "status"),
    SiteConfig("Bilibili", "https://space.bilibili.com/{}", "status"),
    SiteConfig("Spotify", "https://open.spotify.com/user/{}", "status"),
    SiteConfig("Roblox", "https://www.roblox.com/user.aspx?username={}", "text_absent", "Page cannot be found"),
]

class Api:
    async def _check_site(self, session: aiohttp.ClientSession, site: SiteConfig, username: str) -> Dict[str, Any] | None:
        url = site.url.format(username)
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8), allow_redirects=False) as resp:
                if site.check_type == "status":
                    if resp.status == 200:
                        return {"site": site.name, "url": url}
                elif site.check_type == "text_absent":
                    text = await resp.text()
                    if site.absent_text.lower() not in text.lower() and resp.status == 200:
                        return {"site": site.name, "url": url}
        except Exception:
            pass
        return None

    async def search_username(self, username: str) -> Dict[str, Any]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        connector = aiohttp.TCPConnector(limit=20, ssl=False)
        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
            tasks = [self._check_site(session, site, username) for site in SITES]
            results = await asyncio.gather(*tasks)
        
        found = [r for r in results if r is not None]
        return {
            "total": len(SITES),
            "found": found
        }

def main():
    api = Api()
    window = webview.create_window(
        "Shadow OSINT v1.0",
        "interface.html",
        js_api=api,
        width=1100, height=750,
        min_size=(900, 600),
        text_select=True
    )
    webview.start(debug=False)

if __name__ == "__main__":
    main()
