import base64
import json
import unittest
from types import SimpleNamespace

from yarl import URL

from models.channel import Channel, Stream


class _Response:
    status = 204

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None


class ChannelWatchTest(unittest.IsolatedAsyncioTestCase):
    async def test_send_watch_posts_current_payload_to_spade(self):
        twitch = SimpleNamespace(_auth_state=SimpleNamespace(user_id="789"))
        twitch.request = lambda *args, **kwargs: (
            setattr(twitch, "request_args", (args, kwargs)) or _Response()
        )

        channel = object.__new__(Channel)
        channel._twitch = twitch
        channel.id = 456
        channel._login = "streamer"
        channel._spade_url = URL("https://spade.twitch.tv/track")

        stream = object.__new__(Stream)
        stream.channel = channel
        stream.broadcast_id = 123
        stream.game = None
        channel._stream = stream

        self.assertTrue(await channel.send_watch())
        args, kwargs = twitch.request_args
        self.assertEqual(args[:2], ("POST", channel._spade_url))
        properties = json.loads(base64.b64decode(kwargs["data"]["data"]))[0]["properties"]
        self.assertEqual(properties["minutes_logged"], 1)
        self.assertIn("client_time", properties)


if __name__ == "__main__":
    unittest.main()
