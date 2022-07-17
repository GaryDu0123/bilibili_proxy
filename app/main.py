from socket import timeout
import httpx
from fastapi import FastAPI
from app.bilibili.search import bvid_to_music
from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask


app = FastAPI()

client = httpx.AsyncClient()

@app.get("/{bvid}")
async def bproxy(bvid: str):
    matched, source = await bvid_to_music(bvid)

    url = httpx.URL(source)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{bvid}"
    }
    rp_req = client.build_request("GET", url, headers=headers, timeout=None)
    rp_resp = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )
