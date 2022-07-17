import aiohttp


BILIBILI_VIDEO_INFO_API = "http://api.bilibili.com/x/web-interface/view"
BILIBILI_AUDIO_SOURCE_API = "https://api.bilibili.com/x/player/playurl"


async def fetch_cid_by_BVid(BVid: str):
    url = f"{BILIBILI_VIDEO_INFO_API}?bvid={BVid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            resp_json = await r.json()
            status = resp_json.get("code", 1)
            if status != 0:
                raise Exception(resp_json.get("message", "fetch video info failed, unknown reason."))
            else:
                data = resp_json.get("data", {})
                if data:
                    matched = True
                    cid = data.get("cid", 0)
                else:
                    matched = False
                    cid = 0
    return matched, cid

async def fetch_audio_source_by_BVid_and_cid(BVid: str, cid: int):
    url = f"{BILIBILI_AUDIO_SOURCE_API}?bvid={BVid}&cid={cid}&qn=16&fnval=80"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            resp_json = await r.json()
            status = resp_json.get("code", 1)
            if status != 0:
                raise Exception(resp_json.get("message", "fetch audio source failed, unknown reason."))
            else:
                data = resp_json.get("data", {})
                if data:
                    matched = True
                    dash = data.get("dash", {})
                    audio = dash.get("audio", [])
                    if not audio:
                        raise Exception("empty audio source")
                    else:
                        source = audio[0].get("base_url", "")
                else:
                    matched = False
                    source = ""
    return matched, source

async def bvid_to_music(BVid: str):
    matched, cid = await fetch_cid_by_BVid(BVid=BVid)
    if not matched:
        source = ""
    else:
        matched, source = await fetch_audio_source_by_BVid_and_cid(BVid=BVid, cid=cid)
    
    return matched, source