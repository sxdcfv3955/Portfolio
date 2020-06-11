import matplotlib.pyplot as plt
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


def make_df(DataFrame) :  # 파생변수 생성 및 새로운 데이터 프레임 생성
    df = pd.DataFrame()

    df['Confirm'] = (DataFrame['Daily_confirmed'] + DataFrame['Daily_deaths']) / DataFrame['Total_confirmed']   # 확진 데이터 파생변수
    df['Flight'] = DataFrame['Passenger_arrivals'] / DataFrame['Flight_arrivals']   # 항공 데이터 파생변수
    df['Ship'] = ( DataFrame['Ship_crew(korea)'] + DataFrame['Ship_crew(foreign)'] + DataFrame['Ship_passenger'] ) / DataFrame['Ship_count']    #선박 데이터 파생변수
    df['News'] = DataFrame['News_Negative'] / DataFrame['News_Sum'] #뉴스 데이터 파생변수
    df['Date'] = DataFrame['Date'].astype(int)

    df.fillna(0, inplace = True)
    df.set_index('Date',inplace=True)

    df = df.loc[20200101:20200505]  #1월 1일 부터 5월 5일까지의 데이터 사용
    
    Flight_df = pd.DataFrame(df['Flight'])
    Flight_df.columns = ['Flight']

    Ship_df = pd.DataFrame(df['Ship'])
    Ship_df.columns = ['Ship']

    Confirm_df = pd.DataFrame(df['Confirm'])
    Confirm_df.columns = ['Confirm']

    News_df = pd.DataFrame(df['News'])
    News_df.columns = ['News']
    
    return Flight_df, Ship_df, Confirm_df, News_df

def make_x_train_test(DataFrame, name) :    #X_test 데이터 예측을 위해서 shift
    
    df = DataFrame[:][:]
    
    shift_size = 14 #2주간 데이터를 구하기 위해서 2주 Shift
    
    for s in range(1, shift_size+1):
        df['shift_{}'.format(s)] = df[name].shift(s)
          
    y_train = np.asarray(df[name][shift_size:-1])
    
    df.drop( name, axis=1, inplace=True)
    
    X_train = np.array(df[shift_size:-1])
    X_test = np.array(df[-1:])

    X_train_r = X_train.reshape(X_train.shape[0],X_train.shape[1],1)
    X_test_r = X_test.reshape(X_test.shape[0],X_test.shape[1],1)
      
    return X_train_r, X_test_r, y_train


def model ( X_train, X_test, y_train, save_path ) :
    K.clear_session()
    xInput = Input(batch_shape=(None, X_train.shape[1], X_train.shape[2]))
    xLstm_1 = LSTM(20, return_sequences = True, activation='tanh', recurrent_activation='sigmoid')(xInput)
    xLstm_2 = Bidirectional(LSTM(20))(xLstm_1)
    xOutput = Dense(1)(xLstm_2)    
    model = Model(xInput, xOutput)
    model.compile(loss='mse', optimizer='adam',  metrics = [ 'mae' ])
    early_stop = EarlyStopping(monitor='loss', patience=10, mode='min', verbose=2)
    model.fit(X_train, y_train, epochs=2000, batch_size=1, verbose=2, shuffle=False, callbacks=[early_stop])
    y_hat = model.predict(X_test, batch_size=1)
    model.save('model/'+save_path+'.h5')
    return y_hat

def make_columns() :    #실제 데이터 생성 및 저장
    China_df = pd.read_csv('data/Concat/China_concat.csv', header=0)
    Asia_df = pd.read_csv('data/Concat/Asia_concat.csv', header=0)
    America_df = pd.read_csv('data/Concat/America_concat.csv', header=0)
    Africa_df = pd.read_csv('data/Concat/Africa_concat.csv', header=0)
    Europe_df = pd.read_csv('data/Concat/Europe_concat.csv', header=0)
    Oceania_df = pd.read_csv('data/Concat/Oceania_concat.csv', header=0)
    
    Continent_list = [ China_df, Asia_df, America_df, Africa_df, Europe_df, Oceania_df ]
    Continent_name_list = [ 'China', 'Asia', 'America', 'Africa', 'Europe', 'Oceania' ] 
    df_name_list = [ 'Flight', 'Ship', 'Confirm', 'News' ]
    
    for Continent_index in range(len(Continent_list)) : 
        Flight_df, Ship_df, Confirm_df, News_df = make_df(Continent_list[Continent_index])
        df_list = [ Flight_df, Ship_df, Confirm_df, News_df ]

        for df_index in range(len(df_list)) :
            df = df_list[df_index]
            sc = MinMaxScaler() #스케일러
            df = sc.fit_transform(df)
            df = pd.DataFrame(df, columns=[df_name_list[df_index]])

            date_list = [ len(df)+1, len(df)+2, len(df)+3, len(df)+4, len(df)+5, len(df)+6, len(df)+7, len(df)+8, len(df)+9, len(df)+10, len(df)+11, len(df)+12, len(df)+13, len(df)+14 ]

            for date in date_list : 
                df.loc[date] = 0
                X_train, X_test, y_train = make_x_train_test(df, df_name_list[df_index])
                path = Continent_name_list[Continent_index]+df_name_list[df_index]
                y_hat = model(X_train, X_test, y_train, path)
                df.loc[date] = y_hat

            df_list[df_index]=df[:]

        test_df = pd.DataFrame()    
        test_df = pd.concat( [ df_list[0].tail(14), df_list[1].tail(14), df_list[2].tail(14), df_list[3].tail(14) ] , axis=1)
        test_df.to_csv('data/Test/'+Continent_name_list[Continent_index]+ '_test_data.csv', index=False)        #테스트 데이터 저장
