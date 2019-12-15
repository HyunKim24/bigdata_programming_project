import os
import pandas as pd

def stock_preprocessing():
    # 파일 목록 가져오기
    path = "C:\\Users\\hyunmok\\Desktop\\stock_data"
    file_list = os.listdir(path)
    
    # 파일 목록 중 확장자가 csv인 파일만 따로 저장하기
    stock_csv = [file for file in file_list if file.endswith(".csv")]
    
    # 주가가 변동하는 시간에 크롤링된 데이터만 추출한다.
    time = ['_9시30분','_10시0분','_10시30분','_11시0분','_11시30분','_12시0분',
            '_12시30분','_13시0분','_13시30분','_14시0분','_14시30분','_15시0분','_15시30분','_16시0분']

    stock_time_csv = list()
    for i in stock_csv:
        for j in time:
            if j in i:
                stock_time_csv.append(i)
                
    # 수집한 데이터의 컬럼 목록을 가져온다. 
    tmp_columns = pd.read_csv('C:\\Users\\hyunmok\\Desktop\\stock_data\\'+stock_csv[0]).columns
    
    # 최종 데이터셋을 구성할 데이터프레임 선언
    final_dataset = pd.DataFrame(columns=tmp_columns)
    
    # final_dataset에 모든 데이터를 병합한다.
    for i in stock_time_csv:
        data = pd.read_csv('C:\\Users\\hyunmok\\Desktop\\stock_data\\'+i)
        final_dataset = pd.concat([final_dataset,data])
        
    # 불필요한 열을 제거한다.
    final_dataset.drop(['Unnamed: 0','NO'],axis=1,inplace=True)
    
    # 계산에 필요한 컬럼들은 천의자리의 콤마를 지우고 데이터 타입은 numeric으로 변경
    final_dataset['현재가'] = final_dataset.현재가.str.replace(',', '').astype('int64')
    final_dataset['전일비'] = final_dataset.전일비.str.replace(',', '').astype('int64')
    final_dataset['액면가'] = final_dataset.액면가.str.replace(',', '').astype('int64')
    final_dataset['시가총액'] = final_dataset.시가총액.str.replace(',', '').astype('int64')
    final_dataset['거래량'] = final_dataset.거래량.str.replace(',', '').astype('int64')
    final_dataset['상장주식수'] = final_dataset.상장주식수.str.replace(',', '').astype('int64')
    
    final_dataset['외국인비율'] = final_dataset.외국인비율.astype('float')
    final_dataset['PER'] = final_dataset.PER.str.replace(',', '').astype('float')
    final_dataset['ROE'] = final_dataset.ROE.str.replace(',', '').astype('float')
    
    # 시간 데이터를 포맷팅해준다.
    time = final_dataset['시간']
    new_time = list()
    for i in time:
        t = i.split(':')
        if len(t[0]) != 2:
            t[0] = '0'+t[0]
            new_time.append(":".join(t))
        elif len(t[1]) != 2:
            t[1] = t[1]+'0'
            new_time.append(":".join(t))
        else:
            new_time.append(":".join(t))
            
    final_dataset['시간'] = new_time
    
    # 날짜와 시간으로 정렬을 해주고 인덱스를 재설정 해준다.
    final_dataset.sort_values(['날짜','시간'],ascending=True,inplace = True)
    final_dataset.reset_index(drop=True,inplace=True)
    
    # 최종 파일을 csv 형태로 저장해준다.
    final_dataset.to_csv('final_dataset.csv',encoding = 'utf-8')

if __name__ == "__main__":
    stock_preprocessing()