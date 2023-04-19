from deta import Deta
import pandas as pd
import schedule
import time


SAVE_PATH = r'./mbs100_sk.txt'

deta = Deta('d0rwyaghixk_xdYc2J98omec5FU2bEyrePtiYZXPwHPF')
sharekhan_keys_db = deta.Base('sharekhan-keys')
report_drive = deta.Drive('report')
print("Deta setup done!")

def download_report():
    report_file = report_drive.get('mbs100_sk.txt')
    file_data = report_file.read().decode()


    with open(SAVE_PATH,'w') as f:
        for line in file_data:
            f.write(line)

        f.close()

    print(f'New report updated at {time.ctime()}')


schedule.every(2).minutes.do(download_report)
print(schedule.get_jobs())

while 1:
    schedule.run_pending()
    time.sleep(5)



