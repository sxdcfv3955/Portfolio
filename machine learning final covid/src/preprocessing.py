import pandas as pd
import os.path, glob
import re

def Preprocessing_Confirm() :   #확진자 데이터 대륙별 전처리
    df = pd.read_csv("data/대륙데이터.csv")
    
    df['Date'] = df['Date'].apply( lambda x : int(x.replace('-', '')))
    
    China_df = df[ df['Continent'] == 'China' ]
    Asia_df = df[ df['Continent'] == 'Asia' ]
    Africa_df = df[ df['Continent'] == 'Africa' ]
    America_df = df[ df['Continent'] == 'America' ]
    Europe_df = df[ df['Continent'] == 'Europe' ]
    Oceania_df = df[ df['Continent'] == 'Oceania' ]
    
    
    China_group_df = China_df.groupby(China_df['Date']).sum()
    Asia_group_df = Asia_df.groupby(Asia_df['Date']).sum()
    Africa_group_df = Africa_df.groupby(Africa_df['Date']).sum()
    America_group_df = America_df.groupby(America_df['Date']).sum()
    Europe_group_df = Europe_df.groupby(Europe_df['Date']).sum()
    Oceania_group_df = Oceania_df.groupby(Oceania_df['Date']).sum()

    
    China_group_df.to_csv('data/Confirmer/China_group_df.csv')
    Asia_group_df.to_csv('data/Confirmer/Asia_group_df.csv')
    Africa_group_df.to_csv('data/Confirmer/Africa_group_df.csv')
    America_group_df.to_csv('data/Confirmer/America_group_df.csv')
    Europe_group_df.to_csv('data/Confirmer/Europe_group_df.csv')
    Oceania_group_df.to_csv('data/Confirmer/Oceania_group_df.csv')

    print('Preprocessing_Confirm')

def Preprocessing_Entry() : #해왜 유입 데이터 대륙별 전처리
    df = pd.read_excel('data/해외입국자.xlsx')
    
    df.columns = ['Date', 'Sum', 'China', 'Asia', 'Europe', 'America', 'Africa', 'Oceania', 'total' ]
    
    df['Date'] = df['Date'].apply(lambda x : int( str(x).replace('-','').replace(' 00:00:00','')))
    
    df.sort_index(ascending=False, inplace=True)
    
    China_df = df[ ['Date', 'China'] ]
    Asia_df = df[ [ 'Date', 'Asia' ] ]
    Europe_df = df[ [ 'Date', 'Europe' ] ]
    America_df = df[ [ 'Date', 'America' ] ]
    Africa_df = df[ [ 'Date', 'Africa' ] ]
    Oceania_df = df[ [ 'Date', 'Oceania' ] ]
    
    China_df.to_csv('data/Entry/China_group_df.csv')
    Asia_df.to_csv('data/Entry/Asia_group_df.csv')
    America_df.to_csv('data/Entry/America_group_df.csv')
    Africa_df.to_csv('data/Entry/Africa_group_df.csv')
    Europe_df.to_csv('data/Entry/Europe_group_df.csv')
    Oceania_df.to_csv('data/Entry/Oceania_group_df.csv')

    print('Preprocessing_Entry')

def ICAO_code( x ) : #공항 코드

    if ( x[-5] == 'A' or x[-5] == 'O' or x[-5] == 'R' or x[-5] == 'V' or x[-5] == 'W') : 
        return 'Asia' 

    elif ( x[-5] == 'B' or x[-5] == 'E' ) : 
        return 'Europe'

    elif ( x[-5] == 'D' or x[-5] == 'F' or x[-5] == 'H' ) : 
        return 'Africa'

    elif ( x[-5] == 'C' or x[-5] == 'K' or x[-5] == 'M') :
        return 'America' 
    
    elif x[-5] == 'Y' :
        return 'Oceania' 
    
    elif x[-5] == 'G' : 
        if x[-4] == 'C' or x[-4] == 'E': 
            return 'Europe'
        else :
            return 'Africa'
            
    elif x[-5] == 'L' : 
        if x[-4] == 'L' or x[-4] == 'V' : 
            return 'Asia'
        else :
            return 'Europe'
            
    elif x[-5] == 'N' : 
        if x[-4] == 'L' or x[-4] == 'W' or x[-4] == 'T' : 
            return 'Europe'
        else :
            return 'Oceania'
            
    elif x[-5] == 'P' : 
        if x[-4] == 'T' : 
            return 'Asia'
        else :
            return 'America'
            
    elif x[-5] == 'S' : 
        if x[-4] == 'F' or x[-4] == 'O' : 
            return 'Europe'
        else :
            return 'America'
            
    elif x[-5] == 'T' : 
        if x[-4] == 'F' or x[-4] == 'N' or x[-4] == 'Q' or x[-4] == 'R' or x[-4] == 'U' or x[-4] == 'X': 
            return 'Europe'
        else :
            return 'America'
    
    elif x[-5] == 'U' : 
        if x[-4] == 'A' or x[-4] == 'T' or x[-4] == 'B' or x[-4] == 'D' or x[-4] == 'G' or x[-4] == 'T': 
            return 'Asia'
        else :
            return 'Europe'
        
    elif x[-5] == 'Z' :
        if x[-4] == 'K' or x[-4] == 'M' : 
            return 'Asia'
        else :
            return 'China'
        
    else :
        return x


def Preprocessing_Flight() : #항공 데이터 대륙별 전처리
    column = ['공항', '노선', '항공사','운항_출발', '운항_도착', 
          '운항_계', '여객_출발', '여객_도착', '여객_계', '화물_출발', '화물_도착', '화물_계' ]
    
    df = pd.DataFrame(columns=column)
    
    airport_path_list = glob.glob( 'data/공항/*' )

    for airport in airport_path_list : 
        file_path_list = glob.glob(airport + '/*')

        for path in file_path_list : 
            file_list = glob.glob(path + '/*')

            for file in file_list : 
                filename = os.path.basename( file )

                tmp_df = pd.read_excel(file, header=3)
                tmp_df.drop( tmp_df.columns[0] , axis=1, inplace=True )
                tmp_df.columns = column

                p = re.compile('[^0-9]')
                date =  p.sub( '' , filename )
                tmp_df['날짜'] = date

                df = pd.concat([df,tmp_df])

        df.reset_index(inplace=True)
        df.drop(df.columns[0] , axis=1, inplace=True)
        df.to_csv('data/'+filename[:4]+'.csv', index=False)     
        df = pd.DataFrame(columns=column)
        
    df_Gimpo    = pd.read_csv("data/김포공항.csv")
    df_GimHae   = pd.read_csv("data/김해공항.csv")
    df_Daegu    = pd.read_csv("data/대구공항.csv")
    df_Muan     = pd.read_csv("data/무안공항.csv")
    df_Yangyang = pd.read_csv("data/양양공항.csv")
    df_Incheon  = pd.read_csv("data/인천공항.csv")
    df_Jeju     = pd.read_csv("data/제주공항.csv")
    df_Cheongju = pd.read_csv("data/청주공항.csv")
    
    df = pd.concat( [ df_Gimpo, df_GimHae, df_Daegu, df_Muan, 
                 df_Yangyang, df_Incheon, df_Jeju, df_Cheongju ] )
    
    df.reset_index(inplace=True)
    df.drop('공항', axis=1, inplace=True)
    df.drop('항공사', axis=1, inplace=True)
    
    df['노선'] = df['노선'].apply( lambda x : ICAO_code( x ) )
    df.drop('index', axis=1, inplace=True)
    
    df.columns = ['Flight_Country', 'Flight_departure', 'Flight_arrivals', 'Flight_total', 
                                  'Passenger_departure', 'Passenger_arrivals', 'Passenger_total',
                                  'Freight_departure', 'Freight_arrivals', 'Freight_total', 'Date']
    
    Asia_df    = df[ df['Flight_Country'] == 'Asia' ]
    China_df   = df[ df['Flight_Country'] == 'China' ]
    Europe_df  = df[ df['Flight_Country'] == 'Europe' ]
    America_df = df[ df['Flight_Country'] == 'America' ]
    Africa_df  = df[ df['Flight_Country'] == 'Africa' ]
    Oceania_df  = df[ df['Flight_Country'] == 'Oceania' ]
    
    Asia_df.drop('Flight_Country', axis=1, inplace=True)
    China_df.drop('Flight_Country', axis=1, inplace=True)
    Europe_df.drop('Flight_Country', axis=1, inplace=True)
    America_df.drop('Flight_Country', axis=1, inplace=True)
    Africa_df.drop('Flight_Country', axis=1, inplace=True)
    Oceania_df.drop('Flight_Country', axis=1, inplace=True)
    
    Asia_group_df    = Asia_df.groupby(Asia_df['Date']).sum()
    China_group_df   = China_df.groupby(China_df['Date']).sum()
    Europe_group_df  = Europe_df.groupby(Europe_df['Date']).sum()
    America_group_df = America_df.groupby(America_df['Date']).sum()
    Africa_group_df  = Africa_df.groupby(Africa_df['Date']).sum()
    Oceania_group_df  = Oceania_df.groupby(Oceania_df['Date']).sum()
    
    Asia_group_df.to_csv('data/Airport/Asia_group_df.csv')
    China_group_df.to_csv('data/Airport/China_group_df.csv')
    Europe_group_df.to_csv('data/Airport/Europe_group_df.csv')
    America_group_df.to_csv('data/Airport/America_group_df.csv')
    Africa_group_df.to_csv('data/Airport/Africa_group_df.csv')
    Oceania_group_df.to_csv('data/Airport/Oceania_group_df.csv')

    print('Preprocessing_Flight')

def Preprocessing_News() : #뉴스 데이터 대륙별 전처리
    df = pd.read_csv('data/P_N_rate.csv')

    df.columns = ['Date', 'News_Country', 'News_Daily_Total', 'News_Sum', 'News_Negative', 'News_Positive']

    df['Date'] = df['Date'].apply(lambda x : x.replace('-',''))

    China_df = df[ df['News_Country'] == 'China' ]
    Asia_df = df[ df['News_Country'] == 'Asia' ]
    America_df = df[ df['News_Country'] == 'America' ]
    Africa_df = df[ df['News_Country'] == 'Africa' ]
    Europe_df = df[ df['News_Country'] == 'Europe' ]
    Oceania_df = df[ df['News_Country'] == 'Oceania' ]
    
    China_group_df = China_df.groupby(China_df['Date']).sum()
    Asia_group_df = Asia_df.groupby(Asia_df['Date']).sum()
    America_group_df = America_df.groupby(America_df['Date']).sum()
    Africa_group_df = Africa_df.groupby(Africa_df['Date']).sum()
    Europe_group_df = Europe_df.groupby(Europe_df['Date']).sum()
    Oceania_group_df = Oceania_df.groupby(Oceania_df['Date']).sum()
    
    China_group_df.to_csv('data/News/China_group_df.csv')
    Asia_group_df.to_csv('data/News/Asia_group_df.csv')
    America_group_df.to_csv('data/News/America_group_df.csv')
    Africa_group_df.to_csv('data/News/Africa_group_df.csv')
    Europe_group_df.to_csv('data/News/Europe_group_df.csv')
    Oceania_group_df.to_csv('data/News/Oceania_group_df.csv')

    print('Preprocessing_News')

def code( x ) : # 항구 코드 
    China_port = ['XIAMEN','TAICANG','NINGBO','SHANGHAI','QINGDAO PT','CAOJING','BAYUQUAN','CHANGSHU','ZHENJIANG PT',
              'LIANYUNGANG','ZHANGJIAGANG','ZHAPU','QINGDAO','DANDONG PT','SHIDAO PT','YANTAI','YANTIAN PT',
              'TIANJIN','JINGTANG(TANGSHAN)','DALIAN','ZHOUSHAN PT','NANTONG PT','QINHUANGDAO PT','TAIXING','NANJING',
              'WEIHAI','JINZHOU PT','WAIGAOQIAO PT','LONGKOU PT','CHANGSHU PT','JIANGYIN PT','HUANGHUA PT','RUGAO PT',
              'CAOFEIDIAN PT','LANSHAN PT','ZHAPU PT','DONGYING PT','RIZHAO PT','TIANJIN XINGANG PT','BEIHAI PT','WEIFANG PT',
              'ZHANJIANG','SHEKOU PT','SHANTOU','NINGDE','DONGGUAN PT','NANSHA PT','LONGYAN PT','LAIZHOU PT','TAIZHOU',
              'YANTAI PT','WEIFANG','JINGJIANG','FUJIN','JIUZHOU PT','NINGBO PT','YINGKOU PT','JIANGYIN','SHANGHAI PT',
              'CHANGZHOU PT','JINGTANG PT','DA CHAN BAY','FUZHOU','Qidong Pt','XINGANG','PENGLAI','NANJING PT',
              'YANGZHOU PT','YANGSHAN','HUANGHUA','PANJIN','DONGYING','LAIZHOU','JINGJIANG PT','DAFENG PT','FUZHOU PT',
              'YIZHENG','ZHANGZHOU PT','HUANGPU PT','DAYAOWAN','CHANGZHOU, JIANGAU','DAGANG','DONGJIANGKOU','LU-HUA SHAN',
              'JIAXING','QUANZHOU PT','TAICANG PT','QINZHOU PT','JINSHAN','BAOSHAN PT','SHEKOU (CODE CHANGE CN SHK))',
              'HULUDAO PT','GUANGZHOU','DAFENG','TANGSHAN','XINHUI PT','PENGLAI PT','TIANJIN PT','SONGXIA PT','FANGCHENG PT',
              'QIANWAN','HAIKOU','RONGCHENG','TAIZHOU PT','WENZHOU PT','JIAXING PT','ZHANJIANG PT','XIAOHUDAO','CHENGXI',
              'LUSHUN NEW PT','HUIZHOU PT','LUANJIAKOU','MAANSHAN PT','CHINA/MACHONG','XIUYU','XIAMEN PT','MAOMING','BASUO',
              'CHENJIAGANG','GUANGZHOU PT','GULEI','DALIAN PT','WUHU PT','FUQING','WEIHAI PT','DANDONG','HUMEN PT','YANGPU PT',
              'PUTIAN','QUANZHOU','SHANTOU PT','ZHUHAI PT','SHENZHEN','SANBAIMEN','TONGLING PT','DEFENG','HAIYANG','WENZHOU',
              'HAIMEN','LUOYANG','ZHENHAI PT','YANGJIANG PT','JINGZHOU PT','CHONGMING','HUANGPU NEW PORT','TANGSHAN PT',
              'XINSHA','MAJI SHAN' ]

    Asia_port = ['NEGHISHI/YOKOHAMA','SHIMONOSEKI','KOBE','OITA','FUKUYAMA, HIROSHIMA','NANAO',
                 'AKITA','IMABARI','HAKATA/FUKUOKA','TOYAMA','MIZUSHIMA','KIKUMA','SENDAI, MIYAGI',
                 'NIIGATA','YOKOHAMA','OSAKA','IYOMISHIMA','WAKAMATSU/KITAKYUSHU','TSUKUMI','SAKAI',
                 'MOJI/KITAKYUSHU','TOYOHASHI','HIROSHIMA','TOKUYAMA','HIBIKINADA, FUKUOKA','SAKAIDE',
                 'WAKAYAMA','KUSHIRO','IZUHARA','HITAKATSU','YOKKAICHI','NAOSHIMA','SHIMOTSU',
                 'HIGASHIHARIMA','KINUURA','ISHIKARIWAN-SHINKO, HOKKAIDO','SHIMIZU','CHOFU','FUNABASHI',
                 'RUMOI','MATSUYAMA','MURORAN','NAGASAKI','TSURUGA','NAGOYA, AICHI','TOMAKOMAI',
                 'KAKOGAWA','KUROSAKI','HITACHINAKA','KUDAMATSU','HIGASHI-OGISHIMA','HACHINOHE',
                 'KANAZAWA','TOKYO','MISUMI, SHIMANE','IMARI','IWAKUNI','UBE','KASHIMAE','MITAJIRI',
                 'KAWASAKI','SAKATA','OKINAWA, OKINAWA','HOSOSHIMA','ITOZAKI','SAKAIMINATO','OTAKE'
                 'UWAJIMA','YATSUSHIRO','SUSAKI','SATSUMASENDAI','KIIRE','KOMENOTSU','ETAJIMA','ARIAKE, TOKYO',
                 'KASHIMA, IBARAKI','ISHIKARI','KIMITSU','NAHA, OKINAWA','HAKODATE','WAKAMATSU, NAGASAKI',
                 'HIMEKAWA','MUTSURE','OSHIMA, NAGASAKI','REIHOKU','MATSUURA, NAGASAKI','TOYAMASHINKO',
                 'SENZAKI','JAPAN ODAIBA','KURE, HIROSHIMA','OURA/ARIAKE','NIIHAMA','YAMAGUCHI','ONAHAMA',
                 'SHIKAMA','MATSUSHIMA, NAGASAKI','KATAKAMI','KASHIMA, SAGA','SAKAISENBOKU','HINASE',
                 'FUKUYAMA, KAGOSHIMA','SAIGO, SHIMANE','HAMADA','KAWANOE','NAOETSU','NADAHAMA',
                 'TOUYO','NAGOYA, OITA','HITACHI','YAWATA, FUKUOKA','SASEBO','ONOMICHI','NOSHIRO',
                 'HIRO','KUMAMOTO','KAGOSHIMA','MAIZURU','ISHINOMAKI','KOKURA','TAKASAGO','MISUMI', 
                 'KUMAMOTO','TAKUMA','ICHIHARA','SHIMABARA','FUSHIKI','KAJIKI','TAGONOURA','OMAEZAKI'
                 'NAKANOSEKI','SODEGAURA','MIIKE, TOKYO','HIMEJI','ICHIKAWA','TAMASHAIMA','SAGANOSEKI',
                 'SHIBUSHI','AOMORI','MISHIMA, KAWANOE','TOBATA, FUKUOKA','TACHIBANA','MIHARA','CHITA',
                 'OKI','KISHIWADA','MIYAKO, IWATE','ONODA','SENDAISHIOGAMA','NAMIKATA','SHINMOJI','MIYAZU',
                 'MATSUNAGA','KURE, KOCHI','SHIGEI','SAIKI','TOKUSHIMA','AMAGASAKI','MAKURAZAKI','KASADO',
                 'IWAGI,EHIME','TATSUGO','USUKI','TADOTSU','NAGAHAMA, EHIME','MIIKE, FUKUOKA','TAKAMATSU',
                 'HIROTA, IWATE','MIYAZAKI, MIYAZAKI','TSUSHIMA, NAGASAKI','TAHARA','AIOI','HIKARI','NAKAGUSUKU',
                 'YOKOSUKA','HIDAKA','TSURUMI, KANAGAWA','HIKOSHIMA','HIZENOHSHIMA','MATSUURA, KAGOSHIMA',
                 'HABU, HIROSHIMA','FUKUOKA, FUKUOKA','NUMAZU','KASHIWAZAKI','KITANADA','NIIGATAHIGASHI',
                 'KANDA, FUKUOKA','TAKAHAMA/AMAKUSA','NANYO, YAMAGUCH','SHIMOJISHIMA, OKINAWA',
                 'HIAGARI/KITAKIUSHU','ONISHI','TANIYAMA','JOETSU','SAKURAJIMA','HIROHATA','HIRARA','YUSU',
                 'USHIBUKA','HAKATASHIMA','FUTAJIMA, FUKUOKA','FUKUSHIMA, MIYAZAKI','NAGASU, KUMAMOTO',
                 'OHGISHIMA','YAWATAHAMA','NOBEOKA','MINAMATA','TSUNEISHI','ISHIGAKI','OHIGAWA','NANKO',
                 'KYOTO, KYOTO','ONOMICHIITOZAKI','KINOE','KINNAKAGUSUKU',
                 'MAI-LIAO','AN PING','SUAO','KAOHSIUNG','TAIPEI','TAICHUNG','KAINAN','KEELUNG (CHILUNG)','HUALIEN',
                 'SON DUONG','VUNG TAU','PHUOC LONG','CAI LAN','HO CHI MINH CITY','VAN PHONG','DA NANG'
                 'SAI GON PT','HONGAI','GO DAU A TERMINAL','PHU MY','DONG NAI','CAM PHA','HAIPHONG','NGHI SON',
                 'CHAN MAY PORT','CAI MEP INTERNATIONAL TERMINAL','VINH','HO CHI MINH, VICT','QUI NHON','FUKUI',
                 'CAMRANH','DUNG QUAT','GO DAU B TERMINAL','HONG KONG','VICTORIA',
                 'TARAKAN, KALIMANTAN','TANJUNG BARA, KL','BITUNG, SULAWESI','ANYER KIDUL','SAMARINDA, KALIMANTAN',
                 'BALIKPAPAN','AMAMAPARE, IJ','PADANG','TABONEO','JAKARTA, JAVA','ADANG BAY','PELABUHAN FUTONG',
                 'PANJANG','BONTANG, KL','LUWUK','GRESIK, JAVA','PENGGARANG/TANJ.PENGILEH','POSO, SULAWESI','MUARA PANTAI',
                 'BANJARMASIN','Bunati','BINTUNI','DUMAI, SUMATRA','TARJUN','CIGADING, JV','MUARA BERAU','MERAK, JAVA',
                 'PALEMBANG, SUMATRA','SURABAYA',"JAMBI, SUMATRA",'SATUI','TONDA','BANGGAI','KUMAI','KUALA ENOK',
                 'PONTIANAK, KALIMANTAN','CILEGON','BENOA, BALI','SUNGAI PAKNING, SUMATRA','TANJONG BIN',
                 'DAVAO, MINDANAO','BATANGAS/LUZON','ROXAS/PUERTO PRINCESA','LIMAY/BATAAN','MANILA SOUTH HARBOUR'
                 'MANILA','BATAAN, MARIVELES','BALOGO/BATANGAS','ILIGAN, MINDANAO','PORO','CULAO','CALAPAN/BATANGAS'
                 'ALBUERA','PAMPLONA/APARRI','CAVITE, LUZON','BACON/LEGASPI','HIBI','SUBIC BAY','GENERAL SANTOS',
                 'CAGAYAN DE ORO, MINDANAO','CEBU','BOGO/CAGAYAN DE ORO','Calaca','LEGASPI APT, LUZON','JASAAN/CAGAYAN DE ORO',
                 'BACOLOD, NEGROS','BASRA','UMM QASR','GALLE','COLOMBO','RAS TANURA',
                 'YANBU AL-BAHR','RAS AL KHAIR', 'JUAYMAH TERMINAL','AD DAMMAM','JUBAIL',
                 'QALHAT','MIN-AL-FAHAL','SALALAH',	'SINGAPORE','JURONG','AL FUJAYRAH','RUWAIS','KHOR AL FAKKAN',
                 'DAS ISLAND','JEBEL ALI','ZURKU ISLAND','OFFSHORE FUJAIRAH','RAS LAFFAN','LAHAD DATU, SABAH',
                 'LUMUT','LABUAN, SABAH','LINGGA, SARAWAK','PORTKELANG','BINTULU, SARAWAK','TANJUNG PELEPAS',
                 'TAWAU, SABAH','WESTPORT/PORT KLANG','KERTEH TERMINAL','SANDAKAN, SABAH','KUNAK, SABAH',
                 'SUNGAI RENGIT','KIMANIS, SABAH','MALACCA','PASIR GUDANG, JOHOR',"MIRI, SARAWAK",'KEMAMAN',
                 'KOTA KINABALU, SABAH','SERIA','TANJUNG LANGSAT','MAKASSAR','MINA AL AHMADI','MINA ABD ALLAH',
                 'KUWAIT','SITRAH','PHITSANULOK','LAEM CHABANG','KHANOM','KOH SICHANG','SATTAHIP','SIAM BANGKOK PORT','RAYONG',
                 'BANGKOK','BAN MAP TA PHUT','SHARK BAY','SRIRACHA','PARADIP GARH','VISAKHAPATNAM','KOCHI',
                 'COCHIN','CHENNAI (EX MADRAS)','SIKA','NIPAH','NEW MANGALORE','TUTICORIN','PIPAVAV (VICTOR) PORT',
                 'KANDLA','VIZAGAPATANAM','MUMBAI (EX BOMBAY)','MUARA']

    Oceania_port=['KOROR','POHNPEI (EX PONAPE)','LAUTOKA','SUVA','VUDA','PORT MORESBY','RABAUL','NAKETY','NOUMEA','TEOUDIE',
                  'NEPOUI','KOUAOUA','TARAWA','FUNAFUTI','NORO, NEW GEORGIA','HONIARA, GUADALCANAL IS','TIMARU','TAURANGA',
                  'PICTON','BLUFF','DUNEDIN','NEDERLAND, CO','MARSDEN POINT','ASHBURTON','NAPIER','WELLINGTON','PORT CHALMERS',
                  'AUCKLAND','BRISBANE','GLADSTONE','DARWIN','PORT HEDLAND','BARROW ISLAND','GROOTE EYLANDT','WYNDHAM',
                  'PORT WALCOTT','BOTANY BAY','ABBOT POINT','CAIRNS','ONSLOW','DAMPIER','KWINANA','GEELONG','GISBORNE',
                  'USELESS LOOP','MACKAY','FREMANTLE','HAY POINT','MATSUURA, OITA','GERALDTON','NELSON',
                  'ISABEL','SUNRISEBEACH','DALRYMPLE ISLET','ALBANY','DEVONPORT','WESTERNPORT','CAPE FLATTERY','BURNIE',
                  'PORT DALRYMPLE','KIMBE','BARROW ISLAND, WA','BING BONG','PORT KEMBLA','GOVE','CAPE CUVIER',
                  'MASCOT','MOURILYAN','BUNBURY','SYDNEY','MELBOURNE','NEWCASTLE','MAJURO','KWAJALEIN','EBEYE','MARSHALL']

    Europe_port = ['PAPEETE','BERGEN','CONSTANTA',
                   'NOVOROSSIYSK', 'VLADIVOSTOK', 'NAKHODKA', "BUKHTA OL'GA", 'PETROPAVLOVSK-KAMCHATSKIY','KHOLMSK',
                   'VOSTOCHNYY PORT','ZARUBINO','VANINO','SLAVYANKA','DE-KASTRI','PRIGORODNOYE',"YUZHNO-KURIL'SK",'PLASTUN',
                   'OKHOTSK','KORSAKOV','KOZMINO PORT','MAGADAN','TUAPSE','POSYET','SEVERO-KURILSK','MAGADANSKY, PORT',
                   'SOVETSKAYA GAVAN','KAVKAZ','SHAKHTERSK' ]

    America_port = ['OCEAN DISTRICT','BALBOA','SEATTLE','BEAUMONT, TX','ROBERTS BANK','CRISTOBAL','VANCOUVER','OAKLAND, CA',
                    'LONGBEACH','PORTLAND, OR','SANDIEGO','HONOLULU','CAYO ARCAS TERMINAL','MANZANILLO','PORT MELLON','BAHIA BLANCA',
                    'NORTH PACIFIC OCEAN','TROIS-RIVIERES (THREE RIVERS)','LOSANGELES','TACOMA',
                    'CALLAO','FREDERICKTOWN','MATANE','CANAL','ANTOFAGASTA','CLATSKANIE','CORPUSCHRISTI','ALBANY, NY','GALVESTON',
                    'WOODRIVER','PANAMA, CIUDAD DE','KALTAG','OREGON','LIRQUEN','NECOCHEA','LA LIBERTAD','PORTMANATEE','HOUSTON, TX',
                    'PONTA DA MADEIRA','TOWNSVILLE','MATARANI','GRAYSHARBORCITY','POINT LISAS','ITAGUAI','ANCHORAGE','RODMAN','PISCO',
                    'MINE','STEWART','COOSBAY','LAZARO CARDENAS','PORTHUENEME','DONALDSONVILLE','PORTLAND, IN','SANFRANCISCO',
                    'CALETA COLOSO','BEARCREEK','BRUNSWICK, GA','ASTORIA','NEWORLEANS','LONGVIEW','MAZATLAN','BATONROUGE',
                    'CHARLESTON, SC','SAN NICOLAS','NEW WESTMINSTER','SAN ANTONIO','MORRO REDONDO','FERNDALE, WA','COLLEGEVILLE, MN',
                    'PLAQUEMINE','MEJILLONES','MEXICO /OTHER-PORT/','BENICIA','FREEPORT, TX','PRINCE RUPERT','ENSENADA','PORTANGELES',
                    'PANAMACITY','RICHMOND, CA','OLYMPIA','LAKECHARLES','GRAMERCY','GEISMAR','VALDEZ','PITTSBURG, CA',
                    'GUAM','SALVADOR','MAMONAL','WESTHAMPTONBEACH','ACAJUTLA','ECUADOR /OTHER-PORT/','PORTO ALEGRE','NANAIMO',
                    'NEDERLAND, TX','HOUSTON, PA','PORT MOODY','PUERTO QUETZAL','ALBANY','PUNTA LOBITOS','PHILADELPHIA',
                    'SANTOS','HUASCO','ELLISVILLE, MS','ROSARITO TERMINAL','COLON','IQUIQUE',
                    'ANGRA DOS REIS','COLUMBUS, MO','SANTO DOMINGO','GUAYMAS', 'SABINE','KINGSTON' ,'DUTCHHARBOR','SAIPAN']

    Africa_port = ['RICHARDS BAY','PORT LOUIS','EL SUWEIS' , 'PORT SAID','CAPE TOWN','KRIBI','SUEZ','PORT ELIZABETH',
                   'GAMBA','BONNY','EL ISKANDARIYA (ALEXANDRIA)','PORT TEWFIK','SALDANHA BAY','CAP LOPEZ','BRASS','EGYPT /OTHER-PORT/']

    
    if x in China_port :
        return "China"
    
    elif x in Asia_port :
        return "Asia"
    
    elif x in America_port :
        return "America"
    
    elif x in Africa_port :
        return "Africa"
    
    elif x in Europe_port :
        return "Europe"
    
    elif x in Oceania_port :
        return "Oceania"
    
    else :
        return "etc"


def Preprocessing_Ship() : #선박 데이터 대륙별 전처리
    column = ['항명', '호출부호', '선명', '입항횟수', '입항횟수.1', '구분', '외내', '입출', '총톤수', '국제톤수',
       '징수톤수', '입항일시', '출항일시', 'CIO수속일자', '수리일시', '항해구분', 'MRN 번호', '국적',
       '국적.1', '계선장소', '계선장소.1', '계선장소.2', '차항지', '전출항지', '선박용도', '승무원1',
       '승무원2', '승객', '예선', '도선', '부선호출부호1', '부선호출부호2']
    
    df = pd.DataFrame(columns=column)
    
    ship_path_list = glob.glob( 'data/선박/*' )

    for file in ship_path_list : 

        #filename = os.path.basename( file )

        tmp_df = pd.read_excel(file, header=12)
        tmp_df.columns = column
        df = pd.concat([df,tmp_df])

    df.reset_index(inplace=True)
    df.drop(df.columns[0] , axis=1, inplace=True)
    df.to_csv('data/입항.csv', index=False)     

    df = pd.read_csv('data/입항.csv')
    
    df.drop( ['호출부호', '선명', '외내', '입출', '국제톤수', '징수톤수', 'CIO수속일자', '수리일시', '항해구분', 'MRN 번호', '국적.1', '계선장소', '계선장소.1', '계선장소.2', 
         '차항지', '부선호출부호1', '부선호출부호2' , '예선', '도선'], axis=1, inplace=True)
    
    
    df = df[ df['구분']=='최종' ]
    
    korea_ship = [ '기타항', '동해', '인천', '울산', '제주', '대산', '고현', '광양', '여천항', '완도',
       '옥계항', '군산', '여수', '부산', '포항', '옥포', '목포', '평택.당진', '온산', '당진',
       '묵호', '서귀포', '속초', '진해', '삼천포', '포항신항', '마산', '보령', '삼척', '대불',
       '감천', '장항', '영일만항', '하동화력', '호산항', '통영', '태안', '거문도', '장승포', '서울',
       '경인', '부산 신항', '남항', '목포 북항', '칼리오랑' ]
    
    
    mask = df['전출항지'].apply( lambda x : False if x in korea_ship else True )
    
    df = df[ mask ]
    
    df.drop([ '구분', '항명'], axis = 1, inplace=True)
    
    df.fillna(0, inplace=True)
    
    
    df.columns = [ 'Ship_year', 'Ship_count', 'Ship_Total_tonnage', 'Ship_arrival', 'Ship_departure', 'Ship_Nation', 'Ship_Prev_port', 
              'Ship_purpose', 'Ship_crew(korea)', 'Ship_crew(foreign)', 'Ship_passenger']
    
    df['Ship_Prev_port'] = df['Ship_Prev_port'].apply( lambda x : code( x ) )
    
    df.drop( [ 'Ship_departure', 'Ship_Nation', 'Ship_purpose'], axis=True, inplace=True)
    
    df['Ship_arrival'] = df['Ship_arrival'].apply( lambda x : x[:10])
    df['Ship_arrival'] = df['Ship_arrival'].apply( lambda x : int(x.replace('-', '')))
    
    df.rename(columns={"Ship_arrival":"Date"}, inplace=True)
    
    china_df = df[ df['Ship_Prev_port'] == 'China' ]
    asia_df = df[ df['Ship_Prev_port'] == 'Asia' ]
    america_df = df[ df['Ship_Prev_port'] == 'America' ]
    africa_df = df[ df['Ship_Prev_port'] == 'Africa' ]
    europe_df = df[ df['Ship_Prev_port'] == 'Europe' ]
    oceania_df = df[ df['Ship_Prev_port'] == 'Oceania' ]
    
    china_group_df = china_df.groupby(china_df['Date']).sum()
    asia_group_df = asia_df.groupby(asia_df['Date']).sum()
    america_group_df = america_df.groupby(america_df['Date']).sum()
    africa_group_df = africa_df.groupby(africa_df['Date']).sum()
    europe_group_df = europe_df.groupby(europe_df['Date']).sum()
    oceania_group_df = oceania_df.groupby(europe_df['Date']).sum()
    
    china_group_df.to_csv('data/Ship/China_group_df.csv')
    asia_group_df.to_csv('data/Ship/Asia_group_df.csv')
    america_group_df.to_csv('data/Ship/America_group_df.csv')
    africa_group_df.to_csv('data/Ship/Africa_group_df.csv')
    europe_group_df.to_csv('data/Ship/Europe_group_df.csv')
    oceania_group_df.to_csv('data/Ship/Oceania_group_df.csv')

    print('Preprocessing_Ship')


def Concat_All() :  #데이터 합치기
    
    Preprocessing_Flight()
    Preprocessing_Ship()
    Preprocessing_Confirm()
    Preprocessing_News()
    
    China_Confirmer_group_df = pd.read_csv('data/Confirmer/China_group_df.csv')
    Asia_Confirmer_group_df = pd.read_csv('data/Confirmer/Asia_group_df.csv')
    Europe_Confirmer_group_df = pd.read_csv('data/Confirmer/Europe_group_df.csv')
    America_Confirmer_group_df = pd.read_csv('data/Confirmer/America_group_df.csv')
    Africa_Confirmer_group_df = pd.read_csv('data/Confirmer/Africa_group_df.csv')
    Oceania_Confirmer_group_df = pd.read_csv('data/Confirmer/Oceania_group_df.csv')
    
    China_Airport_group_df = pd.read_csv('data/Airport/China_group_df.csv')
    Asia_Airport_group_df = pd.read_csv('data/Airport/Asia_group_df.csv')
    Europe_Airport_group_df = pd.read_csv('data/Airport/Europe_group_df.csv')
    America_Airport_group_df = pd.read_csv('data/Airport/America_group_df.csv')
    Africa_Airport_group_df = pd.read_csv('data/Airport/Africa_group_df.csv')
    Oceania_Airport_group_df = pd.read_csv('data/Airport/Oceania_group_df.csv')
    
    China_Ship_group_df = pd.read_csv('data/Ship/China_group_df.csv')
    Asia_Ship_group_df = pd.read_csv('data/Ship/Asia_group_df.csv')
    Europe_Ship_group_df = pd.read_csv('data/Ship/Europe_group_df.csv')
    America_Ship_group_df = pd.read_csv('data/Ship/America_group_df.csv')
    Africa_Ship_group_df = pd.read_csv('data/Ship/Africa_group_df.csv')
    Oceania_Ship_group_df = pd.read_csv('data/Ship/Oceania_group_df.csv')

    China_News_group_df = pd.read_csv('data/News/China_group_df.csv')
    Asia_News_group_df = pd.read_csv('data/News/Asia_group_df.csv')
    Europe_News_group_df = pd.read_csv('data/News/Europe_group_df.csv')
    America_News_group_df = pd.read_csv('data/News/America_group_df.csv')
    Africa_News_group_df = pd.read_csv('data/News/Africa_group_df.csv')
    Oceania_News_group_df = pd.read_csv('data/News/Oceania_group_df.csv')
    
    China_Entry_group_df = pd.read_csv('data/Entry/China_group_df.csv')
    Asia_Entry_group_df = pd.read_csv('data/Entry/Asia_group_df.csv')
    Europe_Entry_group_df = pd.read_csv('data/Entry/Europe_group_df.csv')
    America_Entry_group_df = pd.read_csv('data/Entry/America_group_df.csv')
    Africa_Entry_group_df = pd.read_csv('data/Entry/Africa_group_df.csv')
    Oceania_Entry_group_df = pd.read_csv('data/Entry/Oceania_group_df.csv')
    
    China_Confirmer_group_df.set_index('Date', inplace=True)
    Asia_Confirmer_group_df.set_index('Date', inplace=True)
    Europe_Confirmer_group_df.set_index('Date', inplace=True)
    America_Confirmer_group_df.set_index('Date', inplace=True)
    Africa_Confirmer_group_df.set_index('Date', inplace=True)
    Oceania_Confirmer_group_df.set_index('Date', inplace=True)
    
    China_Airport_group_df.set_index('Date', inplace=True)
    Asia_Airport_group_df.set_index('Date', inplace=True)
    Europe_Airport_group_df.set_index('Date', inplace=True)
    America_Airport_group_df.set_index('Date', inplace=True)
    Africa_Airport_group_df.set_index('Date', inplace=True)
    Oceania_Airport_group_df.set_index('Date', inplace=True)
    
    China_Ship_group_df.set_index('Date', inplace=True)
    Asia_Ship_group_df.set_index('Date', inplace=True)
    Europe_Ship_group_df.set_index('Date', inplace=True)
    America_Ship_group_df.set_index('Date', inplace=True)
    Africa_Ship_group_df.set_index('Date', inplace=True)
    Oceania_Ship_group_df.set_index('Date', inplace=True)
    
    China_News_group_df.set_index('Date', inplace=True)
    Asia_News_group_df.set_index('Date', inplace=True)
    Europe_News_group_df.set_index('Date', inplace=True)
    America_News_group_df.set_index('Date', inplace=True)
    Africa_News_group_df.set_index('Date', inplace=True)
    Oceania_News_group_df.set_index('Date', inplace=True)
    
    China_Entry_group_df.set_index('Date', inplace=True)
    Asia_Entry_group_df.set_index('Date', inplace=True)
    Europe_Entry_group_df.set_index('Date', inplace=True)
    America_Entry_group_df.set_index('Date', inplace=True)
    Africa_Entry_group_df.set_index('Date', inplace=True)
    Oceania_Entry_group_df.set_index('Date', inplace=True)
    
    China_concat = pd.concat([China_Confirmer_group_df, China_Airport_group_df, China_Ship_group_df, China_News_group_df, China_Entry_group_df], axis=1)
    Asia_concat = pd.concat([Asia_Confirmer_group_df, Asia_Airport_group_df, Asia_Ship_group_df, Asia_News_group_df, Asia_Entry_group_df], axis=1)
    Europe_concat = pd.concat([Europe_Confirmer_group_df, Europe_Airport_group_df, Europe_Ship_group_df, Europe_News_group_df, Europe_Entry_group_df], axis=1)
    America_concat = pd.concat([America_Confirmer_group_df, America_Airport_group_df, America_Ship_group_df, America_News_group_df, America_Entry_group_df], axis=1)
    Africa_concat = pd.concat([Africa_Confirmer_group_df, Africa_Airport_group_df, Africa_Ship_group_df, Africa_News_group_df, Africa_Entry_group_df], axis=1)
    Oceania_concat = pd.concat([Oceania_Confirmer_group_df, Oceania_Airport_group_df, Oceania_Ship_group_df, Oceania_News_group_df, Oceania_Entry_group_df], axis=1)
    
    China_concat.fillna(0, inplace=True)
    Asia_concat.fillna(0, inplace=True)
    Europe_concat.fillna(0, inplace=True)
    America_concat.fillna(0, inplace=True)
    Africa_concat.fillna(0, inplace=True)
    Oceania_concat.fillna(0, inplace=True)

    China_concat.to_csv('data/Concat/China_concat.csv')
    Asia_concat.to_csv('data/Concat/Asia_concat.csv')
    Europe_concat.to_csv('data/Concat/Europe_concat.csv')
    America_concat.to_csv('data/Concat/America_concat.csv')
    Africa_concat.to_csv('data/Concat/Africa_concat.csv')
    Oceania_concat.to_csv('data/Concat/Oceania_concat.csv')

    print('Concat_All')
