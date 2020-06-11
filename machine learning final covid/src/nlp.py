# nltk
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize

import pandas as pd
import numpy as np
import re, requests
import summa
import glob, os.path
from bs4 import BeautifulSoup

from collections import Counter

# 데이터프레임에 기사 내용 추가
def news_load(df,file_list):
    df['내용'] = df['파일명']
    for j,i in enumerate(file_list):
        name = os.path.basename(i)
        with open( i , 'r', encoding = 'ISO-8859-1') as f:
            lines = f.readlines()
            tmp = lines[:len(lines)-1]
            tmp = ''.join(tmp)
            df['내용'][j]= tmp
    return df

# 각 기사 분류를 대륙과 전세계기준으로 분류
def trans_code(text):
    text = text.apply(lambda x : x.replace('GOARN (Global Outbreak Alert and Response Network)','Global' ))
    text = text.apply(lambda x : x.replace('Ministry of Health(Saudi Arabia)','Asia' ))
    text = text.apply(lambda x : x.replace('CIDARS (China Infectious Disease Automated Alert and Re sponse System)','China'))
    text = text.apply(lambda x : re.sub("GPHIN|HealthMap|Flu Trackers|Outbreak News Today|ProMED|WHO/DONs|CIDRAP|WAHIS|WHO/IHR|WHO/News|Disease Daily", 'Global', str(x)))
    text = text.apply(lambda x : re.sub("All africa|AFRO|CDC Nigeria|WHO/EMRO", 'Africa', str(x)))
    text = text.apply(lambda x : re.sub("CNN|CBC|Ministry of Health|Health Canada|GEIS|WHO/PAHO", 'America', str(x)))
    text = text.apply(lambda x : re.sub("Al jazeera|Tuoitre|Dantri Vietnam|VCDC|Reliefweb|CDC Taiwan|WHO/SEARO|Centre for Health Protection", 'Asia', str(x)))
    text = text.apply(lambda x : re.sub("REUTERS|MediSys|BBC|Public Health England|ECDC|EFSA", 'Europe', str(x)))
    text = text.apply(lambda x : re.sub("Xinhua|SINA|Health Commission of Guangdong Province|Shanghai Municioal Health Commission|Wuhan Municipal Health Commission", 'China', str(x)))
    return text

# classific_global 함수에서 분류한 숫자를 대륙으로 변경
def trans_num(text):
    answer = 1
    if text == 1:
        answer = 'Asia'
    if text == 2:
        answer = 'Africa'
    if text == 3:
        answer = 'America'
    if text == 4:
        answer = 'Europe'
    if text == 5:
        answer = 'China'
    if text == 6:
        answer = 'Oceania'
    return answer

# 전세계기준의 기사를 기사속 언급된 국가를 기분으로 분류
def classific_global(text):
    asia = ["afghanistan",'afghan','armenia','armenian',\
            'azerbaijan','azerbaijani','bahrain',"bahraini",\
            'bangladeshi',"bangladesh",'bhutan','bhutanese','brunei','bruneian',\
            'burma','myanmar','burmese','cambodia','cambodian','georgia','georgian',\
            'india','indian','indonesia','indonesian','iran','iranian','iraq','iraqi',\
            'israel','israeli','japan','japanese','jordan','jordanian','kazakhstan',\
            'kazakh','kuwait','kuwaiti','laos','laotian','lebanon','lebanese',\
            'malaysia','malaysian','maldives','maldivian','mongolia','mongolian',\
            'nepal','nepalese','north','korea','korean','south','north korea','south korea',\
            'oman','omani','pakistan','pakistani','philippines','philippine','filipino',\
            'qatar','qatari','saudi','arabia','arabian','saudi arabia','singapore','singaporean',\
            'sri','sri lnakan','lankan','syria','syrian','taiwan','taiwanese','tajikistan',\
            'tajik','tadjik','thailand','thai','arab','emirates','UAE','emirati','uzbekistan',\
            'uzbek','vietnam','vietnamese','yemen','yemeni'
            ]
    africa = ["algeria",'algerian','angola',"angolan",'benin','beninese',\
            'botswana','botswanan','burkina','burkinese','burundi','burundian',\
            'cameroon','cameroonian','cape verde','cape verdean','chad','chadian',\
            'congo','congolese','djibouti','djiboutian','egypt','egyptian','el',\
            'salvador','el salvador','salvadorean','eritrea','eritrean','ethiopia',\
            'ethiopian','gabon','gabonese','gambia','gambian','ghana','ghanaian',\
            'guinea','guinean','kenya','kenyan','liberia','liberian','libya','libyan',\
            'madagascar','malagasy','madagascan','malawi','malawian','mali',\
            'malian','mauritania','mauritanian','mauritius','mauritian','morocco',\
            'moroccan','mozambique','mozambican','namibia','namibian','niger',\
            'nigerien','nigeria','nigerian','rwanda','rwandan','senegal',\
            'senegalese','seychelles','seychellois','sierra leone','sierra','leone',\
            'leonian','somalia','somali','africa','african','sudan','sudanese',\
            'swaziland','swazi','tanzania','tanzanian','togo','togolese','tunisia',\
            'tunisian','uganda','ugandan','zaire','zarean','zambia','zambian','zimbabwe',\
            'zimbabwean'
            ]
    america =["argentina",'argentinian','bahamas','bahamian',\
              'barbados','barbadian','belize','belizian','bolivia','bolivian',\
              'brazil','brazilian','canada','canadian','chile','chilean','colombia',\
              'colombian','costa rica','costa','cuban','cuba','dominica','dominican',\
              'ecuador','ecuadorean','grenada','grenadian','guatemala','guatemalan',\
              'guyana','guyanese','haiti','haitian','honduras','honduran','jamaica',\
              'jamaican','mexico','mexican','nicaragua','nicaraguan','panama','panamaian',\
              'paraguay','paraguayan','peru','peruvian','suriname','surinamese','surinamer',\
              'surinamese','trinidadd','tobago','trinidadian','USA','american','america',\
              'states','uruguay','uruguayan'
              ]
    europe = ["albania",'albanian','andorra','andorran','austria',\
            "austrian","belarus",'belarusian','belarusan','belgium',\
            'belgian','bosnia herzegovina','bosnian','britain','british','briton',\
            'bulgaria','bulgarian','bosnia','croatia','croat','croatian','cyprus',\
            'cypriot','czech','denmark','danish','dane','england','englishman',\
            'englishwoman','estonia','estonian','finland','finnish','finn','france',\
            'french','frenchman','frenchwoman','germany','german','greece','greek',\
            'holland','netherlands','dutch','dutchman','dutchwoman','hungary','hungarian',\
            'iceland','icelandic','icelander','ireland','irish','italy','italian','latvia',\
            'latvian','liechtenstein','liechtensteiner','lithuania','lithuanian','luxembourg',\
            'luxembourger','macedonia','macedonian','malta','maltese','moldova',\
            'moldovan','monaco','mongasque','monacan','montenegro','montenegrin',\
            'norway','norwegian','poland','polish','pole','portugal','portuguese',\
            'portuguese','romania','romanian','russia','russian','scotland','scottish',\
            'scot','serbia','serb','serbian','slovakia','slovak','slovenia','slovene',\
            'slovenian','spain','spanish','spaniard','sweden','swedish','swede',\
            'switzerland','Swiss','turkey','turkish','turk','turkmenistan','ukraine',\
            'ukrainian','kingdom','UK','vatican','venezuela','venezuelan','wales','welsh',\
            'yugoslavia','yugoslav'
            ]
    china =['china','chinese']
    oceania =["australia",'australian','fiji','fijian','zealand','zealander',\
              'new zealand','papua new guinea','guinea',"guinean",'tuvaluan','tuvali','tuvalu',\
              'vanuatu','vanuatuan','samoa','samoan'
              ]
    count = [0, 0, 0, 0, 0, 0]
    
    ## 1.asia, 2.africa, 3.america, 4.europe, 5.china, 6.oceania
    for key, word in enumerate(text):
        answer=0
        if word in asia:
            count[0] += 1
        if word in africa:
            count[1] += 1
        if word in america:
            count[2] += 1
        if word in europe:
            count[3] += 1
        if word in china:
            count[4] += 1
        if word in oceania:
            count[5] += 1
    for k, d in enumerate(count):
        if d == max(count):
            answer= k+1
    
    return trans_num(answer)

# vader 감정어 사전을 통해 기사를 긍부정 분류
def vader_polarity(text):
    analyser = SentimentIntensityAnalyzer()
    tmp = text.apply(lambda x : re.sub(r'\([^)]*\)', '',str(x)))
    tmp = tmp.apply(lambda x : sent_tokenize(str(x)))
    result = []
    for text in tmp:
        count = 0
        for sent in text:
            score = analyser.polarity_scores(sent)
            if score['pos'] > score['neg']:
                count += 1
            else:
                count -= 1
        if count > 0:
            result.append(1) ##pos
        elif count<= 0:
            result.append(0) ##pos
    return result

# Oceania 내용 저장 함수
def save_Oceania(text, date):
    add_list = []
    add_list.append(date)
    target=text
    add_list.append('Oceania')
    tmp_n = target.loc[target['result'] == 0 ]
    tmp_p = target.loc[target['result'] == 1 ]
    add_list.append(target.shape[0])
    add_list.append(tmp_n.shape[0])
    add_list.append(tmp_p.shape[0])
    df_rate = pd.DataFrame(add_list)
    df_rate.to_csv('data/df_global_rate/{}_{}'.format(df_rate[0][0], df_rate[0][1]))

# Asia 내용 저장 함수    
def save_Asia(text, date):
    add_list = []
    add_list.append(date)
    target=text
    add_list.append('Asia')
    tmp_n = target.loc[target['result'] == 0 ]
    tmp_p = target.loc[target['result'] == 1 ]  
    add_list.append(target.shape[0])
    add_list.append(tmp_n.shape[0])
    add_list.append(tmp_p.shape[0])
    df_rate = pd.DataFrame(add_list)
    df_rate.to_csv('data/df_global_rate/{}_{}'.format(df_rate[0][0], df_rate[0][1]))
    
# China 내용 저장 함수
def save_China(text, date):
    add_list = []
    add_list.append(date)
    target=text
    add_list.append('China')
    tmp_n = target.loc[target['result'] == 0 ]
    tmp_p = target.loc[target['result'] == 1 ]
    add_list.append(target.shape[0])
    add_list.append(tmp_n.shape[0])
    add_list.append(tmp_p.shape[0])
    df_rate = pd.DataFrame(add_list)
    df_rate.to_csv('data/df_global_rate/{}_{}'.format(df_rate[0][0], df_rate[0][1]))
    
# Africa 내용 저장 함수    
def save_Africa(text, date):
    add_list = []
    add_list.append(date)
    target=text
    add_list.append('Africa')
    tmp_n = target.loc[target['result'] == 0 ]
    tmp_p = target.loc[target['result'] == 1 ]
    add_list.append(target.shape[0])
    add_list.append(tmp_n.shape[0])
    add_list.append(tmp_p.shape[0])
    df_rate = pd.DataFrame(add_list)
    df_rate.to_csv('data/df_global_rate/{}_{}'.format(df_rate[0][0], df_rate[0][1]))
    
# America 내용 저장 함수
def save_America(text, date):
    add_list = []
    add_list.append(date)
    target=text
    add_list.append('America')
    tmp_n = target.loc[target['result'] == 0 ]
    tmp_p = target.loc[target['result'] == 1 ]
    add_list.append(target.shape[0])
    add_list.append(tmp_n.shape[0])
    add_list.append(tmp_p.shape[0])
    df_rate = pd.DataFrame(add_list)
    df_rate.to_csv('data/df_global_rate/{}_{}'.format(df_rate[0][0], df_rate[0][1]))
    
# Europe 내용 저장 함수   
def save_Europe(text, date,):
    add_list = []
    add_list.append(date)
    target=text
    add_list.append('Europe')
    tmp_n = target.loc[target['result'] == 0 ]
    tmp_p = target.loc[target['result'] == 1 ]
    add_list.append(target.shape[0])
    add_list.append(tmp_n.shape[0])
    add_list.append(tmp_p.shape[0])
    df_rate = pd.DataFrame(add_list)
    df_rate.to_csv('data/df_global_rate/{}_{}'.format(df_rate[0][0], df_rate[0][1]))
# 위에 대륙별 저장함수 사용 및 폴더 저장
def total_save(df_data):
    target_1 = df_data
    date = target_1['날짜'].iloc[0]
    Oceania =target_1.drop(target_1.loc[target_1['채널명_trans'] != 'Oceania'].index)
    Asia   =target_1.drop(target_1.loc[target_1['채널명_trans'] != 'Asia'].index)
    China  =target_1.drop(target_1.loc[target_1['채널명_trans'] != 'China'].index)
    Africa =target_1.drop(target_1.loc[target_1['채널명_trans'] != 'Africa'].index)
    America=target_1.drop(target_1.loc[target_1['채널명_trans'] != 'America'].index)
    Europe =target_1.drop(target_1.loc[target_1['채널명_trans'] != 'Europe'].index)
    save_Oceania(Oceania, date)
    save_Asia(Asia, date)
    save_China(China, date)
    save_Africa(Africa, date)
    save_America(America, date)
    save_Europe(Europe, date)

# 기사속 대륙관련 언급단어 key도출함수
def filt(text):
    diease_Dic = ["afghanistan",'afghan','armenia','armenian',\
            'azerbaijan','azerbaijani','bahrain',"bahraini",\
            'bangladeshi',"bangladesh",'bhutan','bhutanese','brunei','bruneian',\
            'burma','myanmar','burmese','cambodia','cambodian','georgia','georgian',\
            'india','indian','indonesia','indonesian','iran','iranian','iraq','iraqi',\
            'israel','israeli','japan','japanese','jordan','jordanian','kazakhstan',\
            'kazakh','kuwait','kuwaiti','laos','laotian','lebanon','lebanese',\
            'malaysia','malaysian','maldives','maldivian','mongolia','mongolian',\
            'nepal','nepalese','north','korea','korean','south','north korea','south korea',\
            'oman','omani','pakistan','pakistani','philippines','philippine','filipino',\
            'qatar','qatari','saudi','arabia','arabian','saudi arabia','singapore','singaporean',\
            'sri','sri lnakan','lankan','syria','syrian','taiwan','taiwanese','tajikistan',\
            'tajik','tadjik','thailand','thai','arab','emirates','UAE','emirati','uzbekistan',\
            'uzbek','vietnam','vietnamese','yemen','yemeni',"algeria",'algerian','angola',"angolan",'benin','beninese',\
            'botswana','botswanan','burkina','burkinese','burundi','burundian',\
            'cameroon','cameroonian','cape verde','cape verdean','chad','chadian',\
            'congo','congolese','djibouti','djiboutian','egypt','egyptian','el',\
            'salvador','el salvador','salvadorean','eritrea','eritrean','ethiopia',\
            'ethiopian','gabon','gabonese','gambia','gambian','ghana','ghanaian',\
            'guinea','guinean','kenya','kenyan','liberia','liberian','libya','libyan',\
            'madagascar','malagasy','madagascan','malawi','malawian','mali',\
            'malian','mauritania','mauritanian','mauritius','mauritian','morocco',\
            'moroccan','mozambique','mozambican','namibia','namibian','niger',\
            'nigerien','nigeria','nigerian','rwanda','rwandan','senegal',\
            'senegalese','seychelles','seychellois','sierra leone','sierra','leone',\
            'leonian','somalia','somali','africa','african','sudan','sudanese',\
            'swaziland','swazi','tanzania','tanzanian','togo','togolese','tunisia',\
            'tunisian','uganda','ugandan','zaire','zarean','zambia','zambian','zimbabwe',\
            'zimbabwean',"argentina",'argentinian','bahamas','bahamian',\
              'barbados','barbadian','belize','belizian','bolivia','bolivian',\
              'brazil','brazilian','canada','canadian','chile','chilean','colombia',\
              'colombian','costa rica','costa','cuban','cuba','dominica','dominican',\
              'ecuador','ecuadorean','grenada','grenadian','guatemala','guatemalan',\
              'guyana','guyanese','haiti','haitian','honduras','honduran','jamaica',\
              'jamaican','mexico','mexican','nicaragua','nicaraguan','panama','panamaian',\
              'paraguay','paraguayan','peru','peruvian','suriname','surinamese','surinamer',\
              'surinamese','trinidadd','tobago','trinidadian','USA','american','america',\
              'states','uruguay','uruguayan',"albania",'albanian','andorra','andorran','austria',\
            "austrian","belarus",'belarusian','belarusan','belgium',\
            'belgian','bosnia herzegovina','bosnian','britain','british','briton',\
            'bulgaria','bulgarian','bosnia','croatia','croat','croatian','cyprus',\
            'cypriot','czech','denmark','danish','dane','england','englishman',\
            'englishwoman','estonia','estonian','finland','finnish','finn','france',\
            'french','frenchman','frenchwoman','germany','german','greece','greek',\
            'holland','netherlands','dutch','dutchman','dutchwoman','hungary','hungarian',\
            'iceland','icelandic','icelander','ireland','irish','italy','italian','latvia',\
            'latvian','liechtenstein','liechtensteiner','lithuania','lithuanian','luxembourg',\
            'luxembourger','macedonia','macedonian','malta','maltese','moldova',\
            'moldovan','monaco','mongasque','monacan','montenegro','montenegrin',\
            'norway','norwegian','poland','polish','pole','portugal','portuguese',\
            'portuguese','romania','romanian','russia','russian','scotland','scottish',\
            'scot','serbia','serb','serbian','slovakia','slovak','slovenia','slovene',\
            'slovenian','spain','spanish','spaniard','sweden','swedish','swede',\
            'switzerland','Swiss','turkey','turkish','turk','turkmenistan','ukraine',\
            'ukrainian','kingdom','UK','vatican','venezuela','venezuelan','wales','welsh',\
            'yugoslavia','yugoslav','china','chinese',"australia",'australian','fiji','fijian','zealand','zealander',\
              'new zealand','papua new guinea','guinea',"guinean",'tuvaluan','tuvali','tuvalu',\
              'vanuatu','vanuatuan','samoa','samoan'
              ]

    words = []
    for word in text:
#         print(word)
#         print('----------------')
        if word in diease_Dic:
            words.append(word)
#             print(words)
#             print('-------------')
    return words

# 자연어 처리함수
def make_nlp() : 
    df_1 = pd.read_excel('data/aihub/corona_contest_data_0406/3-1. NewsList.xls')
    df_2 = pd.read_excel('data/aihub/corona_contest_data_0429/3-1. NewsList.xls')
    df_3 = pd.read_excel('data/aihub/corona_contest_data_0506/3-1. NewsList.xls')

    file_list_1 = glob.glob('data/aihub/corona_contest_data_0406/3-2. Contents/*')
    file_list_2 = glob.glob('data/aihub/corona_contest_data_0429/3-2. Contents/*')
    file_list_3 = glob.glob('data/aihub/corona_contest_data_0506/3-2. Contents/*')

    df1 = news_load(df_1,file_list_1)
    df2 = news_load(df_2,file_list_2)
    df3 = news_load(df_3,file_list_3)

    df_total = pd.concat([df1,df2,df3])
    df_total.to_csv('data/total_data.txt', index= False)
    
    df = pd.read_csv('data/total_data.txt')
    df['년도'] = df['게시일자'].str.split('-', expand=True)[0]
    df['월'] = df['게시일자'].str.split('-', expand=True)[1]
    df['일시'] = df['게시일자'].str.split('-', expand=True)[2]
    df['일'] = df['일시'].str.split(' ', expand=True)[0]
    df['날짜'] = df['게시일자'].str.split(' ', expand=True)[0]
    df.drop(['게시일자'], axis =1, inplace=True)
    df['result']=vader_polarity(df['내용'])
    df['채널명_trans']= trans_code(df['채널명'])

    global_df =df.drop(df.loc[df['채널명_trans'] != 'Global'].index)
    stop_words_2 = stopwords.words('english')
    # 불용어 리스트만들기
    stop_words_2.extend(['https','said','nan','font','com','http','date','human','case','people'])
    global_df['token'] = global_df['내용'].apply(lambda x: str(x).lower())
    global_df['token'] = global_df['token'].apply(lambda x: x.split())
    global_df['token'] = global_df['token'].apply(lambda x: [WordNetLemmatizer().lemmatize(word, pos='n') for word in x])
    global_df['token'] = global_df['token'].apply(lambda x: [w for w in x if not w in stop_words_2])
    global_df['word'] = global_df['token'].apply(lambda x : filt(x))
    global_df['word'] = global_df['word'].apply(lambda x : set(x))
    df_tmp = global_df[['내용','token','word']]
    df_tmp['cls_w'] = df_tmp['word'].apply(lambda x : classific_global(x))
    df_tmp['cls_w'] = df_tmp['cls_w'].apply(lambda x : trans_num(x))

    for i in range(df.shape[0]):
        if df['채널명_trans'][i] == 'Global':
            df['채널명_trans'][i] = df_tmp['cls_w'].loc[i]

    df['월'] = df['월'].astype(int)
    df['일'] = df['일'].astype(int)

    df_1=df.drop(df.loc[df['월'] != 1].index)
    df_2=df.drop(df.loc[df['월'] != 2].index)
    df_3=df.drop(df.loc[df['월'] != 3].index)
    df_4=df.drop(df.loc[df['월'] != 4].index)
    df_5=df.drop(df.loc[df['월'] != 5].index)

    # 2020 1월 일 분류
    df_2020_1_1 =df_1.drop(df_1.loc[df_1['일'] != 1].index)
    total_save(df_2020_1_1)
    df_2020_1_2 =df_1.drop(df_1.loc[df_1['일'] != 2].index)
    total_save(df_2020_1_2)
    df_2020_1_3 =df_1.drop(df_1.loc[df_1['일'] != 3].index)
    total_save(df_2020_1_3)
    df_2020_1_4 =df_1.drop(df_1.loc[df_1['일'] != 4].index)
    total_save(df_2020_1_4)
    df_2020_1_5 =df_1.drop(df_1.loc[df_1['일'] != 5].index)
    total_save(df_2020_1_5)
    df_2020_1_6 =df_1.drop(df_1.loc[df_1['일'] != 6].index)
    total_save(df_2020_1_6)
    df_2020_1_7 =df_1.drop(df_1.loc[df_1['일'] != 7].index)
    total_save(df_2020_1_7)
    df_2020_1_8 =df_1.drop(df_1.loc[df_1['일'] != 8].index)
    total_save(df_2020_1_8)
    df_2020_1_9 =df_1.drop(df_1.loc[df_1['일'] != 9].index)
    total_save(df_2020_1_9)
    df_2020_1_10 =df_1.drop(df_1.loc[df_1['일'] != 10].index)
    total_save(df_2020_1_10)
    df_2020_1_11 =df_1.drop(df_1.loc[df_1['일'] != 11].index)
    total_save(df_2020_1_11)
    df_2020_1_12 =df_1.drop(df_1.loc[df_1['일'] != 12].index)
    total_save(df_2020_1_12)
    df_2020_1_13 =df_1.drop(df_1.loc[df_1['일'] != 13].index)
    total_save(df_2020_1_13)
    df_2020_1_14 =df_1.drop(df_1.loc[df_1['일'] != 14].index)
    total_save(df_2020_1_14)
    df_2020_1_15 =df_1.drop(df_1.loc[df_1['일'] != 15].index)
    total_save(df_2020_1_15)
    df_2020_1_16 =df_1.drop(df_1.loc[df_1['일'] != 16].index)
    total_save(df_2020_1_16)
    df_2020_1_17 =df_1.drop(df_1.loc[df_1['일'] != 17].index)
    total_save(df_2020_1_17)
    df_2020_1_18 =df_1.drop(df_1.loc[df_1['일'] != 18].index)
    total_save(df_2020_1_18)
    df_2020_1_19 =df_1.drop(df_1.loc[df_1['일'] != 19].index)
    total_save(df_2020_1_19)
    df_2020_1_20 =df_1.drop(df_1.loc[df_1['일'] != 20].index)
    total_save(df_2020_1_20)
    df_2020_1_21 =df_1.drop(df_1.loc[df_1['일'] != 21].index)
    total_save(df_2020_1_21)
    df_2020_1_22 =df_1.drop(df_1.loc[df_1['일'] != 22].index)
    total_save(df_2020_1_22)
    df_2020_1_23 =df_1.drop(df_1.loc[df_1['일'] != 23].index)
    total_save(df_2020_1_23)
    df_2020_1_24 =df_1.drop(df_1.loc[df_1['일'] != 24].index)
    total_save(df_2020_1_24)
    df_2020_1_25 =df_1.drop(df_1.loc[df_1['일'] != 25].index)
    total_save(df_2020_1_25)
    df_2020_1_26 =df_1.drop(df_1.loc[df_1['일'] != 26].index)
    total_save(df_2020_1_26)
    df_2020_1_27 =df_1.drop(df_1.loc[df_1['일'] != 27].index)
    total_save(df_2020_1_27)
    df_2020_1_28 =df_1.drop(df_1.loc[df_1['일'] != 28].index)
    total_save(df_2020_1_28)
    df_2020_1_29 =df_1.drop(df_1.loc[df_1['일'] != 29].index)
    total_save(df_2020_1_29)
    df_2020_1_30 =df_1.drop(df_1.loc[df_1['일'] != 30].index)
    total_save(df_2020_1_30)
    df_2020_1_31 =df_1.drop(df_1.loc[df_1['일'] != 31].index)
    total_save(df_2020_1_31)

    # 2월 일 분류
    df_2020_2_1 =df_2.drop(df_2.loc[df_2['일'] != 1].index)
    total_save(df_2020_2_1)
    df_2020_2_2 =df_2.drop(df_2.loc[df_2['일'] != 2].index)
    total_save(df_2020_2_2)
    df_2020_2_3 =df_2.drop(df_2.loc[df_2['일'] != 3].index)
    total_save(df_2020_2_3)
    df_2020_2_4 =df_2.drop(df_2.loc[df_2['일'] != 4].index)
    total_save(df_2020_2_4)
    df_2020_2_5 =df_2.drop(df_2.loc[df_2['일'] != 5].index)
    total_save(df_2020_2_5)
    df_2020_2_6 =df_2.drop(df_2.loc[df_2['일'] != 6].index)
    total_save(df_2020_2_6)
    df_2020_2_7 =df_2.drop(df_2.loc[df_2['일'] != 7].index)
    total_save(df_2020_2_7)
    df_2020_2_8 =df_2.drop(df_2.loc[df_2['일'] != 8].index)
    total_save(df_2020_2_8)
    df_2020_2_9 =df_2.drop(df_2.loc[df_2['일'] != 9].index)
    total_save(df_2020_2_9)
    df_2020_2_10 =df_2.drop(df_2.loc[df_2['일'] != 10].index)
    total_save(df_2020_2_10)
    df_2020_2_11 =df_2.drop(df_2.loc[df_2['일'] != 11].index)
    total_save(df_2020_2_11)
    df_2020_2_12 =df_2.drop(df_2.loc[df_2['일'] != 12].index)
    total_save(df_2020_2_12)
    df_2020_2_13 =df_2.drop(df_2.loc[df_2['일'] != 13].index)
    total_save(df_2020_2_13)
    df_2020_2_14 =df_2.drop(df_2.loc[df_2['일'] != 14].index)
    total_save(df_2020_2_14)
    df_2020_2_15 =df_2.drop(df_2.loc[df_2['일'] != 15].index)
    total_save(df_2020_2_15)
    df_2020_2_16 =df_2.drop(df_2.loc[df_2['일'] != 16].index)
    total_save(df_2020_2_16)
    df_2020_2_17 =df_2.drop(df_2.loc[df_2['일'] != 17].index)
    total_save(df_2020_2_17)
    df_2020_2_18 =df_2.drop(df_2.loc[df_2['일'] != 18].index)
    total_save(df_2020_2_18)
    df_2020_2_19 =df_2.drop(df_2.loc[df_2['일'] != 19].index)
    total_save(df_2020_2_19)
    df_2020_2_20 =df_2.drop(df_2.loc[df_2['일'] != 20].index)
    total_save(df_2020_2_20)
    df_2020_2_21 =df_2.drop(df_2.loc[df_2['일'] != 21].index)
    total_save(df_2020_2_21)
    df_2020_2_22 =df_2.drop(df_2.loc[df_2['일'] != 22].index)
    total_save(df_2020_2_22)
    df_2020_2_23 =df_2.drop(df_2.loc[df_2['일'] != 23].index)
    total_save(df_2020_2_23)
    df_2020_2_24 =df_2.drop(df_2.loc[df_2['일'] != 24].index)
    total_save(df_2020_2_24)
    df_2020_2_25 =df_2.drop(df_2.loc[df_2['일'] != 25].index)
    total_save(df_2020_2_25)
    df_2020_2_26 =df_2.drop(df_2.loc[df_2['일'] != 26].index)
    total_save(df_2020_2_26)
    df_2020_2_27 =df_2.drop(df_2.loc[df_2['일'] != 27].index)
    total_save(df_2020_2_27)
    df_2020_2_28 =df_2.drop(df_2.loc[df_2['일'] != 28].index)
    total_save(df_2020_2_28)
    df_2020_2_29 =df_2.drop(df_2.loc[df_2['일'] != 29].index)
    total_save(df_2020_2_29)

    # 3월 일별 분류
    df_2020_3_1 =df_3.drop(df_3.loc[df_3['일'] != 1].index)
    total_save(df_2020_3_1)
    df_2020_3_2 =df_3.drop(df_3.loc[df_3['일'] != 2].index)
    total_save(df_2020_3_2)
    df_2020_3_3 =df_3.drop(df_3.loc[df_3['일'] != 3].index)
    total_save(df_2020_3_3)
    df_2020_3_4 =df_3.drop(df_3.loc[df_3['일'] != 4].index)
    total_save(df_2020_3_4)
    df_2020_3_5 =df_3.drop(df_3.loc[df_3['일'] != 5].index)
    total_save(df_2020_3_5)
    df_2020_3_6 =df_3.drop(df_3.loc[df_3['일'] != 6].index)
    total_save(df_2020_3_6)
    df_2020_3_7 =df_3.drop(df_3.loc[df_3['일'] != 7].index)
    total_save(df_2020_3_7)
    df_2020_3_8 =df_3.drop(df_3.loc[df_3['일'] != 8].index)
    total_save(df_2020_3_8)
    df_2020_3_9 =df_3.drop(df_3.loc[df_3['일'] != 9].index)
    total_save(df_2020_3_9)
    df_2020_3_10 =df_3.drop(df_3.loc[df_3['일'] != 10].index)
    total_save(df_2020_3_10)
    df_2020_3_11 =df_3.drop(df_3.loc[df_3['일'] != 11].index)
    total_save(df_2020_3_11)
    df_2020_3_12 =df_3.drop(df_3.loc[df_3['일'] != 12].index)
    total_save(df_2020_3_12)
    df_2020_3_13 =df_3.drop(df_3.loc[df_3['일'] != 13].index)
    total_save(df_2020_3_13)
    df_2020_3_14 =df_3.drop(df_3.loc[df_3['일'] != 14].index)
    total_save(df_2020_3_14)
    df_2020_3_15 =df_3.drop(df_3.loc[df_3['일'] != 15].index)
    total_save(df_2020_3_15)
    df_2020_3_16 =df_3.drop(df_3.loc[df_3['일'] != 16].index)
    total_save(df_2020_3_16)
    df_2020_3_17 =df_3.drop(df_3.loc[df_3['일'] != 17].index)
    total_save(df_2020_3_17)
    df_2020_3_18 =df_3.drop(df_3.loc[df_3['일'] != 18].index)
    total_save(df_2020_3_18)
    df_2020_3_19 =df_3.drop(df_3.loc[df_3['일'] != 19].index)
    total_save(df_2020_3_19)
    df_2020_3_20 =df_3.drop(df_3.loc[df_3['일'] != 20].index)
    total_save(df_2020_3_20)
    df_2020_3_21 =df_3.drop(df_3.loc[df_3['일'] != 21].index)
    total_save(df_2020_3_21)
    df_2020_3_22 =df_3.drop(df_3.loc[df_3['일'] != 22].index)
    total_save(df_2020_3_22)
    df_2020_3_23 =df_3.drop(df_3.loc[df_3['일'] != 23].index)
    total_save(df_2020_3_23)
    df_2020_3_24 =df_3.drop(df_3.loc[df_3['일'] != 24].index)
    total_save(df_2020_3_24)
    df_2020_3_25 =df_3.drop(df_3.loc[df_3['일'] != 25].index)
    total_save(df_2020_3_25)
    df_2020_3_26 =df_3.drop(df_3.loc[df_3['일'] != 26].index)
    total_save(df_2020_3_26)
    df_2020_3_27 =df_3.drop(df_3.loc[df_3['일'] != 27].index)
    total_save(df_2020_3_27)
    df_2020_3_28 =df_3.drop(df_3.loc[df_3['일'] != 28].index)
    total_save(df_2020_3_28)
    df_2020_3_29 =df_3.drop(df_3.loc[df_3['일'] != 29].index)
    total_save(df_2020_3_29)
    df_2020_3_30 =df_3.drop(df_3.loc[df_3['일'] != 30].index)
    total_save(df_2020_3_30)
    df_2020_3_31 =df_3.drop(df_3.loc[df_3['일'] != 31].index)
    total_save(df_2020_3_31)

    ## 4월분류
    df_2020_4_1 =df_4.drop(df_4.loc[df_4['일'] != 1].index)
    total_save(df_2020_4_1)
    df_2020_4_2 =df_4.drop(df_4.loc[df_4['일'] != 2].index)
    total_save(df_2020_4_2)
    df_2020_4_3 =df_4.drop(df_4.loc[df_4['일'] != 3].index)
    total_save(df_2020_4_3)
    df_2020_4_4 =df_4.drop(df_4.loc[df_4['일'] != 4].index)
    total_save(df_2020_4_4)
    df_2020_4_5 =df_4.drop(df_4.loc[df_4['일'] != 5].index)
    total_save(df_2020_4_5)
    df_2020_4_6 =df_4.drop(df_4.loc[df_4['일'] != 6].index)
    total_save(df_2020_4_6)
    df_2020_4_7 =df_4.drop(df_4.loc[df_4['일'] != 7].index)
    total_save(df_2020_4_7)
    df_2020_4_8 =df_4.drop(df_4.loc[df_4['일'] != 8].index)
    total_save(df_2020_4_8)
    df_2020_4_9 =df_4.drop(df_4.loc[df_4['일'] != 9].index)
    total_save(df_2020_4_9)
    df_2020_4_10 =df_4.drop(df_4.loc[df_4['일'] != 10].index)
    total_save(df_2020_4_10)
    df_2020_4_11 =df_4.drop(df_4.loc[df_4['일'] != 11].index)
    total_save(df_2020_4_11)
    df_2020_4_12 =df_4.drop(df_4.loc[df_4['일'] != 12].index)
    total_save(df_2020_4_12)
    df_2020_4_13 =df_4.drop(df_4.loc[df_4['일'] != 13].index)
    total_save(df_2020_4_13)
    df_2020_4_14 =df_4.drop(df_4.loc[df_4['일'] != 14].index)
    total_save(df_2020_4_14)
    df_2020_4_15 =df_4.drop(df_4.loc[df_4['일'] != 15].index)
    total_save(df_2020_4_15)
    df_2020_4_16 =df_4.drop(df_4.loc[df_4['일'] != 16].index)
    total_save(df_2020_4_16)
    df_2020_4_17 =df_4.drop(df_4.loc[df_4['일'] != 17].index)
    total_save(df_2020_4_17)
    df_2020_4_18 =df_4.drop(df_4.loc[df_4['일'] != 18].index)
    total_save(df_2020_4_18)
    df_2020_4_19 =df_4.drop(df_4.loc[df_4['일'] != 19].index)
    total_save(df_2020_4_19)
    df_2020_4_20 =df_4.drop(df_4.loc[df_4['일'] != 20].index)
    total_save(df_2020_4_20)
    df_2020_4_21 =df_4.drop(df_4.loc[df_4['일'] != 21].index)
    total_save(df_2020_4_21)
    df_2020_4_22 =df_4.drop(df_4.loc[df_4['일'] != 22].index)
    total_save(df_2020_4_22)
    df_2020_4_23 =df_4.drop(df_4.loc[df_4['일'] != 23].index)
    total_save(df_2020_4_23)
    df_2020_4_24 =df_4.drop(df_4.loc[df_4['일'] != 24].index)
    total_save(df_2020_4_24)
    df_2020_4_25 =df_4.drop(df_4.loc[df_4['일'] != 25].index)
    total_save(df_2020_4_25)
    df_2020_4_26 =df_4.drop(df_4.loc[df_4['일'] != 26].index)
    total_save(df_2020_4_26)
    df_2020_4_27 =df_4.drop(df_4.loc[df_4['일'] != 27].index)
    total_save(df_2020_4_27)
    df_2020_4_28 =df_4.drop(df_4.loc[df_4['일'] != 28].index)
    total_save(df_2020_4_28)
    df_2020_4_29 =df_4.drop(df_4.loc[df_4['일'] != 29].index)
    total_save(df_2020_4_29)
    df_2020_4_30 =df_4.drop(df_4.loc[df_4['일'] != 30].index)
    total_save(df_2020_4_30)

    # 5월
    df_2020_5_1 =df_5.drop(df_5.loc[df_5['일'] != 1].index)
    total_save(df_2020_5_1)
    df_2020_5_2 =df_5.drop(df_5.loc[df_5['일'] != 2].index)
    total_save(df_2020_5_2)
    df_2020_5_3 =df_5.drop(df_5.loc[df_5['일'] != 3].index)
    total_save(df_2020_5_3)
    df_2020_5_4 =df_5.drop(df_5.loc[df_5['일'] != 4].index)
    total_save(df_2020_5_4)
    df_2020_5_5 =df_5.drop(df_5.loc[df_5['일'] != 5].index)
    total_save(df_2020_5_5)

    file_list = glob.glob('data/df_global_rate/*')
    df_test = pd.read_csv('data/df_global_rate/2020-01-01_Africa')
    for i in file_list[1:]:
        name = os.path.basename(i)
        tmp = pd.read_csv('data/df_global_rate/{}'.format(name))
        df_test = pd.merge(df_test,tmp, on ='Unnamed: 0', how='left')

    df_test = df_test.drop('Unnamed: 0',axis =1)
    df_test= df_test.T
    df_test = df_test.set_index(0)
    df_test.rename(columns = {1:'대륙',2:'일편수',3:'대륙편수',4:'부정수' ,5:'긍정수'}, inplace =True)
    df_test.to_csv('data/P_N_rate.csv')
