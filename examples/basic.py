import os, time, asyncio
from mathmatize_poller import MathMatizePoller

poll_uuid = input('Please enter the UUID in the Poll URL:')

poller = MathMatizePoller(
    None, # silently install new chromedriver, best practice is to provide a path to a local chromedriver if avaliable
    os.getenv('MATHMATIZE_EMAIL'),
    os.getenv('MATHMATIZE_PASSWORD')
)

def on_poll_update(monitor):
    print ('There was a poll update!')
    print (time.monotic() + monitor.duration - monitor.start_time + ' seconds remaining.')

async def start_poller():
    poller = MathMatizePoller(
        "/Users/reyaan/Projects/common/web_drivers/chromedriver-mac-arm64/chromedriver",
        os.getenv('MATHMATIZE_EMAIL'),
        os.getenv('MATHMATIZE_PASSWORD')
    )

    monitor = poller.get_or_create_monitor(poll_uuid, on_poll_update, 30, 5, k=1.5)
    monitor.start()

    # simulate work
    await asyncio.sleep(30)

    monitor.stop()
    poller.shutdown()


asyncio.run(start_poller())