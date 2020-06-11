import preprocessing as pr
import make_xtest as mx
import make_model as mm
import preditction as pt
import nlp


#nlp.make_nlp() #뉴스 데이터를 위한 형태소 및 감정분석
#pr.Concat_All() #초기 데이터 전처리
#mx.make_columns() # 테스트 데이터 구축
#mm.lstm_model() # 예측 모델 구현

# ------------------ 전처리 --------------------------
# ------------------ 실제 예측 ----------------------
pt.make_yhat() # 예측

