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


def make_yhat() : # 이주간의 예측 
    Continent_name_list = [ 'China', 'Asia', 'America', 'Africa', 'Europe', 'Oceania' ] 

    for Continent in Continent_name_list : 
        model = load_model('model/'+Continent+'_model.h5')
        test_data = pd.read_csv('data/Test/'+Continent+'_x_test_data.csv')
        test_data.set_index('Date',inplace=True)
        
        test_data = np.array(test_data)
        X_test = test_data.reshape(test_data.shape[0],test_data.shape[1],1)

        y_hat = abs(model.predict(X_test, batch_size=1))
        print(Continent + ':')
        print(y_hat)
        
        