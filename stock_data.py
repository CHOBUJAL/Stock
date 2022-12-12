import os
import mojito
import pprint
import keys
import pandas as pd
import logging, logging.config

if not os.path.exists("./logs/"):
    os.makedirs("./logs/")

logging.config.fileConfig("./logging.conf", disable_existing_loggers=False)
logger = logging.getLogger('stock_logger')

broker = mojito.KoreaInvestment(
    api_key=keys.key, 
    api_secret=keys.secret,
    acc_no=keys.acc_no,
)

kospi = broker.fetch_kospi_symbols()
kosdaq = broker.fetch_kosdaq_symbols()

def get_symbol_daily_data(since:str="", excel_output:bool=False, symbol:str="", timeframe:str="D", pidaq:str="kospi"):
    """특정 종목의 기간별시세(일/주/월)
    Args:
        since (str): 수집 시작 일자 일자를 주지 않는 경우 현재 날짜에서 
                     이전 30일 데이터 부터 시작(Defaults : "")
        excel_output (bool): 수집된 데이터 엑셀 저장 여부 (Defaults : False)
        symbol (str): 종목코드 (Defaults : "")
        timeframe (str): D:일봉, W:주봉, M:월봉 (Defaults : "D")
        pidaq (str): kospi:코스피, kosdaq:코스닥 (Defaults to "kospi")
        
    Returns:
       DataFrame
    """
    
    if symbol == "":
        logger.error(f"종목 코드를 넣어주세요.")
        return
    
    if pidaq == "kospi":
        symbols = kospi
    else:
        symbols = kosdaq
    
    if not (symbols['단축코드'] == symbol).any():
        logger.error(f"{pidaq}에 존재하지않는 종목 코드입니다.")
        return
        
    daily = broker.fetch_ohlcv(symbol=symbol, timeframe=timeframe, adj_price=True, since=since)
    
    total_data = list()
    for day in daily:
        total_data += day.json()['output2']

    df = pd.DataFrame(total_data)
    
    if excel_output:
        df.to_excel("./test.xlsx", sheet_name = 'Sheet1')
    
    return df

# a = get_symbol_daily_data(symbol="000060")
# logger.info(f"{a}")
