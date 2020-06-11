import numpy as np
import pandas as pd
from keras.layers import *
from keras.models import *
from keras.utils import *
from sklearn.preprocessing import *
import keras.backend as K
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Bidirectional
from keras.callbacks import EarlyStopping
from keras.models import load_model

def make_df(DataFrame, test) : #테스트 데이터와 합쳐서 최종 데이터 생성
    df = pd.DataFrame()
    
    Test = pd.read_csv('data/Test/'+test+'_test_data.csv')
    Test['Date'] = [20200506, 20200507, 20200508, 20200509, 20200510, 20200511,20200512, 20200513, 20200514,20200515, 20200516, 20200517, 20200518, 20200519]
    Test.set_index('Date',inplace=True)

    
    DataFrame.set_index('Date',inplace=True)
    label = DataFrame[DataFrame.columns[-1]]
    
    

    df['Confirm'] = (DataFrame['Daily_confirmed'] + DataFrame['Daily_deaths']) / DataFrame['Total_confirmed']
    df['Flight'] = DataFrame['Passenger_arrivals'] / DataFrame['Flight_arrivals']
    df['Ship'] = ( DataFrame['Ship_crew(korea)'] + DataFrame['Ship_crew(foreign)'] + DataFrame['Ship_passenger'] ) / DataFrame['Ship_count']
    df['News'] = DataFrame['News_Negative'] / DataFrame['News_Sum']

    df.fillna(0, inplace = True)
    

    df = df.loc[20200101:20200505]  #1월1일 부터 5월 5일까지의 데이터 사용
    
    sc = MinMaxScaler()

    df['Confirm'] = sc.fit_transform(pd.DataFrame(df['Confirm']))
    df['Flight'] = sc.fit_transform(pd.DataFrame(df['Flight']))
    df['Ship'] = sc.fit_transform(pd.DataFrame(df['Ship']))
    df['News'] = sc.fit_transform(pd.DataFrame(df['News']))
    
    df = pd.concat([df,Test])
    
    y_train = np.array(label.loc[20200115:20200505])
    
    return df, y_train

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True, filename=''): #shift 함수
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        
    for i in range(0, n_out+1):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    
    if dropnan:
        agg.dropna(inplace=True)
        
        
    X_train = np.array(agg.loc[:20200505])
    X_test = agg.loc[20200505:]
    X_test.to_csv('data/Test/'+filename+'_x_test_data.csv')

    
    X_train = X_train.reshape(X_train.shape[0],X_train.shape[1],1)
        
    return X_train

def prediction(X_train, y_train, name) :     #모델 학습 후 저장

    K.clear_session()     # 모델 생성전에 tensorflow의 graph 영역을 clear한다.
    xInput = Input(batch_shape=(None, X_train.shape[1], X_train.shape[2]))
    xLstm_1 = LSTM(20, return_sequences = True, activation='tanh', recurrent_activation='sigmoid')(xInput)
    xLstm_4 = Bidirectional(LSTM(20))(xLstm_1)
    xOutput = Dense(1)(xLstm_4)

    model = Model(xInput, xOutput)
    model.compile(loss='mse', optimizer='adam', metrics = [ 'mae' ])

    early_stop = EarlyStopping(monitor='loss', patience=10, mode='min', verbose=2)

    model.fit(X_train, y_train, epochs=2000, batch_size=1, verbose=2, shuffle=False)
    
    model.save('model/'+name+'_model.h5')

def lstm_model() : # 모델 생성 메인 함수
    China_df = pd.read_csv('data/Concat/China_concat.csv', header=0)
    Asia_df = pd.read_csv('data/Concat/Asia_concat.csv', header=0)
    America_df = pd.read_csv('data/Concat/America_concat.csv', header=0)
    Africa_df = pd.read_csv('data/Concat/Africa_concat.csv', header=0)
    Europe_df = pd.read_csv('data/Concat/Europe_concat.csv', header=0)
    Oceania_df = pd.read_csv('data/Concat/Oceania_concat.csv', header=0)
    
    Continent_list = [ China_df, Asia_df, America_df, Africa_df, Europe_df, Oceania_df ]
    Continent_name_list = [ 'China', 'Asia', 'America', 'Africa', 'Europe', 'Oceania' ] 
    
    for index in range(len(Continent_list)) :
        df, y_train = make_df(Continent_list[index],  Continent_name_list[index])
        X_train = series_to_supervised(df,14,0, filename = Continent_name_list[index])
        prediction(X_train, y_train, Continent_name_list[index])
        
