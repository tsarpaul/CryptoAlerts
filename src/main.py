import asyncio

from src.slack.client import SlackClient
from src.collectors.twitter.main import run_twitter

if __name__ == "__main__":
    pub_client = SlackClient()

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(
        asyncio.wait(
            [
                pub_client.throttle_pubs(),
                run_twitter(pub_client=pub_client)
            ],
            return_when=asyncio.FIRST_EXCEPTION
        )
    )

    for result in results:
        print(result)
    loop.close()
