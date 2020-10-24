import random
import pandas as pd
import numpy as np

def to_csv(df, file_name):
    df.to_csv(file_name, index=False)
    
def read_csv(file_name):
    for enc in ['big5', 'utf-8']:
        try:
            return pd.read_csv(file_name, encoding=enc)
        except:
            pass
    raise RuntimeError('We try all encoding but cannot read the csv')
    
def rand_df(rand_dict, row_num, miss_rate=0, na_values = None):
    """
    函數功能: 依指定規則生成一個隨機dataframe
    參數:
        rand_dict: key為column名稱，value為自定義隨機函數
        row_num: 總共有幾筆資料
        miss_rate: 資料丟失的機率
        na_values: 可迭代容器，當資料丟失時產生的值 (默認為 np.nan)
    caller example:
        rand_dict = {'status': lambda: random.choice(['Wait', 'Start'])}
        print(rand_df(rand_dict, 20, miss_rate=0.2, na_values=['None', 'NoData']))  
    """
    def miss_judge(val):
        if random.random()<= miss_rate:
            return random.choice(na_values) if na_values else np.nan
        return val
        
    assert 0 <= miss_rate <= 1, 'probability must in [0,1]'
    df = pd.DataFrame()
    for k,v in rand_dict.items():
        df[k] = [miss_judge(v()) for _ in range(row_num)]
    return df

        
if __name__=='__main__':
    rand_dict = {'status': lambda: random.choice(['Wait', 'Start'])}
    print(rand_df(rand_dict, 20, miss_rate=0.2, na_values=['None', 'NoData']))
    