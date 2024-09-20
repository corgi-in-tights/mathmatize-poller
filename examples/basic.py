import os, time, asyncio, requests
from mathmatize_poller import MathMatizePoller




def on_poll_update(monitor):
    print (f'There was a poll update on {monitor.url}!')
    print(f'{time.time() + monitor.duration - monitor.start_time} seconds remaining...')

"""
Async is required since the poll runs in the background, easy to port to sync (extend PollMonitor) but
highly recommended to keep as is.

Selenium webdrivers are not thread-safe therefore the driver runs on the main/relevant thread, easy to read, easy to maintain.

Work can be done in the background but it must be `await`ed to gain the benefits of async.
"""
async def start_poller(loop, url):
    poller = MathMatizePoller(
        None, # silently install new chromedriver, best practice is to provide a path to a local chromedriver if avaliable
        os.getenv('MATHMATIZE_EMAIL'),
        os.getenv('MATHMATIZE_PASSWORD')
    )

    monitor = poller.get_or_create_monitor(url, on_poll_update, 60*60, 12, k=4)
    monitor.start()



if __name__ == '__main__':
    url = input('Please enter the poll url:')
    print ('Selected', url)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.create_task(start_poller(loop, url))
        loop.run_forever()
    except KeyboardInterrupt:
        pass