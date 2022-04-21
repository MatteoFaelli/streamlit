import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import time
import streamlit as st

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     df_codes = pd.read_excel(uploaded_file)
     st.write(df_codes)
     
     list_departure = [x for x in df_codes.iloc[:,0]]
     list_arrival = [x for x in df_codes.iloc[:,1]]

     list_url = ["https://www.world-airport-codes.com/distance/?a1=" + x + "&a2=" + y + "&code=IATA" for x,y in zip(list_departure,list_arrival)]

     list_distances = []

     hdr = {'User-Agent': 'Mozilla/5.0'}

     #It takes approximately 3 seconds per query
     c=1
     for url in list_url:
        t1 = time.time()
        req = Request(url,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page)
        data = soup.p
        txt = data.text
        #st.write(txt)
        st.write("Progress: " + str(c) + "/" + str(len(list_arrival)))
        c+=1
        t2 = time.time()
        #print("Time to extract data:",round(t2-t1,2),"s")
        try:
            distance = float(re.findall(r'\d+', txt)[0:2][0])
        except IndexError:
            distance = -1
        list_distances.append(distance)    
        
     df_results = pd.DataFrame({'Departure':list_departure,'Arrival':list_arrival,'Distance (km)':list_distances})
     st.write(df_results)

     @st.cache
     def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

     csv = convert_df(df_results)

     st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name='airport_distance_scrap_results.csv',
        mime='text/csv',
     )