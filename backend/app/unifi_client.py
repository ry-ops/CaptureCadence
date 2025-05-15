import httpx
from typing import List

class UniFiClient:
    def __init__(self, ip: str, api_key: str, username: str, password: str):
        self.base_url = f"https://{ip}/proxy/access"
        self.api_key = api_key
        self.username = username
        self.password = password
        self.token = None
        self.client = httpx.AsyncClient(verify=False)  # disable SSL verify for local IPs

    async def login(self):
        login_url = f"{self.base_url}/api/login"
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        resp = await self.client.post(login_url, json=payload, headers=headers)
        resp.raise_for_status()
        self.token = resp.cookies.get("unifises")
        self.client.cookies.set("unifises", self.token)

    async def get_cameras(self) -> List[dict]:
        if not self.token:
            await self.login()
        url = f"{self.base_url}/api/cameras"
        headers = {"x-api-key": self.api_key}
        resp = await self.client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", [])

    async def capture_still(self, camera_id: str, output_path: str):
        if not self.token:
            await self.login()
        url = f"{self.base_url}/api/cameras/{camera_id}/snapshot"
        headers = {"x-api-key": self.api_key}
        resp = await self.client.post(url, headers=headers)
        resp.raise_for_status()
        snapshot_url = resp.json().get("url")
        if not snapshot_url:
            raise Exception("Snapshot URL not found")

        image_resp = await self.client.get(snapshot_url)
        image_resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(image_resp.content)

    async def capture_video(self, camera_id: str, length_sec: int, output_path: str):
        if not self.token:
            await self.login()
        start_url = f"{self.base_url}/api/cameras/{camera_id}/video/start"
        headers = {"x-api-key": self.api_key}
        payload = {"length": length_sec}
        resp = await self.client.post(start_url, json=payload, headers=headers)
        resp.raise_for_status()
        video_data = resp.json()
        clip_url = video_data.get("clip_url")

        if not clip_url:
            raise Exception("Video clip URL not found")

        video_resp = await self.client.get(clip_url)
        video_resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(video_resp.content)
