from deta import Deta
from sharekhanConnect import SharekhanConnect
import pandas as pd
import time


deta = Deta('d0rwyaghixk_xdYc2J98omec5FU2bEyrePtiYZXPwHPF')
sharekhan_keys_db = deta.Base('sharekhan-keys')
report_drive = deta.Drive('report')

api_key = sharekhan_keys_db.get('api_key')['value']
secret_key = sharekhan_keys_db.get('secret_key')['value']
user_id = sharekhan_keys_db.get('user_id')['value']
customer_id = sharekhan_keys_db.get('customer_id')['value']
access_token = sharekhan_keys_db.get('access_token')['value']
version_id = "1005"


sharekhan = SharekhanConnect(api_key,access_token=access_token)

def date_converter(date):
    date_split = date.split()
    date = date_split[1]
    year = date[-4:]
    month = date[-7:-4]
    day = date[:-7]

    converted = "".join([day,'-',month,'-',year])

    return converted

while 1:

    report = sharekhan.reports(customer_id)

    report_df = pd.DataFrame(report['data'])



    df = pd.DataFrame({})


    df['Trade No'] = report_df['exchOrderId']
    df['Trade Status'] = 11
    df['Instrument Name'] = 'OPTIDX'
    df['Symbol'] = report_df['contract']
    df['Expiry Date'] = report_df['tradingSymbol'].apply(date_converter)
    df['Strike Price'] = report_df['strikePrice']
    df['Option Type'] = report_df['optionType']
    df['Security Name'] = report_df['tradingSymbol']
    df['Book Type'] = 1
    df['Book Type Name'] = 'RL'
    df['Market Type'] = 1
    df['User ID'] = "MBS100"
    df['Branch ID'] = 14
    df['BuySell'] = report_df.apply(lambda x : 1 if x['buySell'] == "B" else 2,axis=1)
    df['Qty Traded'] = report_df['orderQty']
    df['Price'] = report_df['execPrice']
    df['Pro/Cli'] = 1
    df['Client AC'] = 2683052
    df['Participant Code'] = 10733
    df['Open Close'] = "OPEN"
    df['Cover UnCover'] = ""
    df['Entry Time'] = report_df['lastModTime']
    df['Modify DateTime'] = report_df['lastModTime']
    df['Order No'] = report_df['exchOrderId']
    df['CP Id'] = 'NIL'
    df['ProductType'] = 'CarryForward'

    df.to_csv("mbs100_sk.txt",header=None)

    f = open('./mbs100_sk.txt', 'r')
    report_drive.put('mbs100_sk.txt', f)
    f.close()

    time.sleep(180)

