import asyncio
import warnings

import janus
import requests

from .conf.channels import channel_urls


class SlackClient:
    def __init__(self):
        self.pub_rate = 1  # 1 sec
        self._pub_throttle = janus.Queue().async_q
        self.throttling = False

    async def publish(self, ch, msg):
        await self._pub_throttle.put((ch, msg))

    async def _publish_to_channel(self, ch, msg):
        ch = ch.lower()
        ch_url = channel_urls.get(ch)
        if not ch_url:
            warnings.warn("Requested channel {ch} does not exist!".format(ch=ch))
            return None
        return requests.post(ch_url, json={'text': msg})

    async def throttle_pubs(self):
        """Process the publish queue, and throttle publish messages based on the publish rate"""
        while True:
            ch, msg = await self._pub_throttle.get()  # Blocks until we get an item
            resp = await self._publish_to_channel(ch, msg)
            print(resp)
            print("[ *] Published to channel {ch} message: \n{msg}\n".format(ch=ch, msg=msg))
            if resp:
                await asyncio.sleep(self.pub_rate)

