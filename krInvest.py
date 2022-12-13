import os
import mojito
import pprint
import pandas as pd
import logging, logging.config


class KrInvest:
    
    def __init__(self, api_key:str, api_secret:str, acc_no:str, mock:bool=False):
        """Args:
            api_key (str): 한국투자증권 개인 api key
            api_secret (str): 한국투자증권 개인 api secret key
            acc_no (str): 한국투자증권 계좌 번호
            mock (bool): 모의 투자 여부 (True : 실제거래 / False : 모의투자)
        """
        #self.logger = self.make_logger()
        
        self.broker = mojito.KoreaInvestment(
            api_key=api_key, 
            api_secret=api_secret,
            acc_no=acc_no,
            mock=mock
            )
    
    
    def __del__(self):
        
        # del logger
        del self.broker
        
        
    # def makeLogger(self):
        
    #     if not os.path.exists("./logs/"):
    #         os.makedirs("./logs/")
            
    #     logging.config.fileConfig("./logging.conf", disable_existing_loggers=False)
    #     logger = logging.getLogger('stock_logger')
        
    #     return logger
    
    
    def resetBroker(self, api_key:str, api_secret:str, acc_no:str, mock:bool=False):
        """
        Args:
            api_key (str): 한국투자증권 개인 api key
            api_secret (str): 한국투자증권 개인 api secret key
            acc_no (str): 한국투자증권 계좌 번호
            mock (bool): 모의 투자 여부 (True : 실제거래 / False : 모의투자)
        """
        try:
            self.broker = mojito.KoreaInvestment(
                api_key=api_key, 
                api_secret=api_secret,
                acc_no=acc_no,
                mock=mock
                )
            
        except Exception as e:
            raise Exception(f"ResetBroker Error \n{e}")
    
    
    def getKospiSymbols(self):
        """
        Returns:
            DataFrame
        """
        try:
            return self.broker.fetch_kospi_symbols()
        
        except Exception as e:
            raise Exception(f"GetKospiSymbols Error \n{e}")
            
            
    def getKosdaqSymbols(self):
        """
        코스닥 모든 종목 return 
        Returns:
            DataFrame
        """
        try:
            return self.broker.fetch_kosdaq_symbols()
        
        except Exception as e:
            raise Exception(f"GetKosdaqSymbols Error \n{e}")


    def getSymbolDailyData(self, symbol:str="", since:str="", timeframe:str="D"):
        """
        특정 종목의 기간별시세(일/주/월)
        Args:
            since (str): 수집 시작 일자 일자를 주지 않는 경우 현재 날짜에서 
                        이전 30일 데이터 부터 시작(Defaults : "")
            symbol (str): 종목코드 (Defaults : "")
            timeframe (str): D:일봉, W:주봉, M:월봉 (Defaults : "D")
            
        Returns:
            DataFrame(since ~ today)
        """
        try:
            if symbol == "":
                raise Exception(f"Empty Symbol")
            
            daily = self.broker.fetch_ohlcv(symbol=symbol, since=since, timeframe=timeframe, adj_price=True)
            
            total_data = list()
            for day in daily:
                total_data += day.json()['output2']
                
            df = pd.DataFrame(total_data)
            df['stck_bsop_date'] = pd.to_datetime(df['stck_bsop_date'])
            df.sort_values('stck_bsop_date', ascending=True, inplace=True)
            df.reset_index(inplace=True)
            df.drop(['index'], axis=1, inplace=True)
                
            return df
        
        except Exception as e:
            raise Exception(f"GetSymbolDailyData Error \n{e}")
        
        
    def getMovingAverage(self, baseData=""):
        
        try:
            type_checking_df = pd.DataFrame()
            if type(type_checking_df) != type(baseData):
                raise Exception(f"BaseData Type must be Pandas DataFrame")
            
        except Exception as e:
            raise Exception(e)