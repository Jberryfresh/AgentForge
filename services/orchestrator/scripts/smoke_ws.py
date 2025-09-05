import asyncio
import json
import os

import websockets


def _ws_url(agent_id: str) -> str:
    host = os.environ.get("SMOKE_HOST", "127.0.0.1")
    port = int(os.environ.get("SMOKE_PORT", "8000"))
    return f"ws://{host}:{port}/ws/agents/{agent_id}"


async def run() -> None:
    a_uri = _ws_url("agentA")
    b_uri = _ws_url("agentB")

    async with websockets.connect(b_uri) as wb:
        received = {}

        async def recv_b():
            received["msg"] = await wb.recv()

        task = asyncio.create_task(recv_b())
        async with websockets.connect(a_uri) as wa:
            await wa.send(json.dumps({"to": "agentB", "data": {"ping": "hello"}}))
            await asyncio.sleep(0.3)
            assert "msg" in received, "agentB did not receive from agentA"
            data = json.loads(received["msg"])  # type: ignore[index]
            assert data.get("from") == "agentA", data
            await wb.send(json.dumps({"to": "agentA", "data": {"pong": "hi"}}))
            reply = await wa.recv()
            print("WS A<->B reply:", reply)
            r = json.loads(reply)
            assert r.get("from") == "agentB", r
            assert r.get("data", {}).get("pong") == "hi", r


if __name__ == "__main__":
    asyncio.run(run())

