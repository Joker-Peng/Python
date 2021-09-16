import win32api,win32con,time

from apscheduler.schedulers.blocking import BlockingScheduler

def DrunkWater():

    win32api.MessageBox(0, "你的欠款已逾期，为了不影响朋友间的感情，请尽快结清！", "还钱小助手",win32con.MB_OK)
    # BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(DrunkWater, 'interval', minutes=1)

if __name__ == '__main__':
    while True:
        scheduler.start()
        time.sleep(1)
