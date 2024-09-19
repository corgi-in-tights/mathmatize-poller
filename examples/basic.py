import os, time, asyncio
from mathmatize_poller import MathMatizePoller

poll_uuid = input('Please enter the UUID in the Poll URL:')

def on_poll_update(monitor):
    print ('There was a poll update!')
    print (time.monotic() + monitor.duration - monitor.start_time + ' seconds remaining.')

"""
Async is required since the poll runs in the background, easy to port to sync (extend PollMonitor) but
highly recommended to keep as is.

Selenium webdrivers are not thread-safe therefore the driver runs on the main/relevant thread, easy to read, easy to maintain.

Work can be done in the background but it must be `await`ed to gain the benefits of async.
"""
async def start_poller(poll_uuid):
    poller = MathMatizePoller(
            None, # silently install new chromedriver, best practice is to provide a path to a local chromedriver if avaliable
        os.getenv('MATHMATIZE_EMAIL'),
        os.getenv('MATHMATIZE_PASSWORD')
    )

    monitor = poller.get_or_create_monitor(poll_uuid, on_poll_update, 30, 5, k=1.5)
    monitor.start()

    # simulate work
    await asyncio.sleep(30)

    monitor.stop()
    poller.shutdown()


asyncio.run(start_poller(poll_uuid))