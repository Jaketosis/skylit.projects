import os
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from PIL import Image
import requests
import pandas as pd
from io import StringIO
import psycopg2
import numpy as np
import csv
from psycopg2 import sql, connect


#clear out the imagelinks table to avoid duplicates

df=pd.DataFrame(columns=["/sourcelink","/imglink","/posttitle","/postdate","/mainpostedited","/pictureindex"])

targetPages=['https://geekhack.org/index.php?board=132.0',
             'https://geekhack.org/index.php?board=132.50',
             'https://geekhack.org/index.php?board=70.0',
             'https://geekhack.org/index.php?board=70.0']

for targetPage in targetPages:
            
            req = requests.get(targetPage)
            soup = BeautifulSoup(req.text,"lxml")
            print(soup.title.string)
            
            i=0
            table = soup.find("table",{"class","table_grid"}).find("tbody").findAll("tr")#.findAll("td",{"class":"subject windowbg2"})
            for row in table:
                
                rowElement = row.findAll("td",{"class":"subject windowbg2"})
                
                for subElement in rowElement: 
                    
                    spans = subElement.find_all("span")
                    if str(str(spans)[11:15])=='msg_':
                        #.contents[0])
                        print('############\n')
                        # print(i,True)
                        # print(str(spans).find('href=\"'))
                        # print(str(spans).find('\"',27))
                        # print(str(spans)[33:str(spans).find('\"',33)])
                        # i=i+1
                        # print(str(spans).find('>',str(spans).find('>')+1))
                        print(str(spans)[str(spans).find('>',str(spans).find('>')+1)+1:-12])
                        inner_req=requests.get(str(spans)[33:str(spans).find('\"',33)])
                        inner_soup=BeautifulSoup(inner_req.text,"lxml")
                        
                        post_dates=inner_soup.findAll("div",{"class":"smalltext"})
                        



                        postingDateStr=str(post_dates[0])[str(post_dates[0]).find(
                                                                '>',
                                                                str(post_dates[0]).find(
                                                                                    '>',
                                                                                    str(post_dates[0]).find('>')+1
                                                                                    )+1
                                                                )+2#+2 for space removal lol
                                                                                    
                                                                                    
                                            :-8]

                        post_dates_modified=inner_soup.findAll("div",{"class":"smalltext modified"})

                        postDateModStr=str(post_dates_modified[0])[str(post_dates_modified[0]).find('>',str(post_dates_modified[0]).find('>')+1)+1:str(post_dates_modified[0]).find('<',str(post_dates_modified[0]).find('<',str(post_dates_modified[0]).find('<')+1)+1)]

                        # for j in post_dates:
                        #     print('\n')
                        #     if str(j)[21:22]=='\"':print(str(j),'\n')
                        #     # print(str(j)[21:22])
                        #     # print('\n')
                        #     # print('zzzzzzzzzz')
                        #     # print('\n')

                        
                        pictures=inner_soup.findAll("a",{"class":"highslide"})
                        counterQ=0
                        for i in pictures:
                            print('___\n')
                            print('i:',i)
                            print(str(i)[27:str(i).find('\"',27)])
                            
                            # ImageLink.objects.create(source=str(spans)[33:str(spans).find('\"',33)],imgLink=str(i)[27:str(i).find('\"',27)],postTitle=str(spans)[str(spans).find('>',str(spans).find('>')+1)+1:str(spans).find('<',str(spans).find('<',str(spans).find('<')+1)+1)],postDate=postingDateStr,mainPostEdited=postDateModStr,pictureIndex=counterQ)
                            df=df.append({"/sourcelink":"/"+str(spans)[33:str(spans).find('\"',33)],
                                        "/imglink":"/"+str(i)[27:str(i).find('\"',27)],
                                        "/posttitle":"/"+str(spans)[str(spans).find('>',str(spans).find('>')+1)+1:str(spans).find('<',str(spans).find('<',str(spans).find('<')+1)+1)],
                                        "/postdate":"/"+postingDateStr,
                                        "/mainpostedited":"/"+postDateModStr,
                                        "/pictureindex":"/"+str(counterQ)
                                        },
                                    ignore_index=True)

                            print('___\n')
                            counterQ=counterQ+1
                        print('############\n')


#########dataframe should be finished


########write the dataframe to the postgres server

df=df.append({"/sourcelink":"/Test_sourcelink",
            "/imglink":"/Test",
            "/posttitle":"/Test",
            "/postdate":"/Test",
            "/mainpostedited":"/Test",
            "/pictureindex":"/Test"
            },
        ignore_index=True)

for index, row in df.head().iterrows():
    print(index,row)

df.to_csv('meme.csv',index=False)

conn = None

print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(host="database-2.c2xa1utqjm6r.us-east-2.rds.amazonaws.com",database="postgres",user="jakemarsh",password="Sephiroth!1")

columns=[]
cursor = conn.cursor()
col_names_str = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
col_names_str += "table_name = '{}';".format( 'ghlinks' )
print ("\ncol_names_str:", col_names_str)

try:
        sql_object = sql.SQL(
            # pass SQL statement to sql.SQL() method
            col_names_str
        ).format(
            # pass the identifier to the Identifier() method
            psycopg2.sql.Identifier( 'ghlinks' )
        )
        # execute the SQL string to get list with col names in a tuple
        cursor.execute( sql_object )

        # get the tuple element from the liast
        col_names = ( cursor.fetchall() )

        # print list of tuples with column names
        print ("\ncol_names:", col_names)
         # iterate list of tuples and grab first element
        for tup in col_names:

            # append the col name string to the list
            columns += [ tup[0] ]
           
        # close the cursor object to prevent memory leaks
        for j in col_names:
            print(j)
        for i in columns:
            print(i) 

except Exception as err:
        print ("get_columns_names ERROR:", err)

query = """INSERT INTO ghlinks(sourcelink, imglink, posttitle, postdate, mainpostedited,pictureindex) VALUES(%s, %s, %s, %s, %s, %s)"""
try:
    
    cursor.execute("DROP TABLE IF EXISTS ghlinks")
    
    cursor.execute("CREATE TABLE ghlinks(sourcelink TEXT,imglink TEXT,posttitle TEXT, postdate TEXT, mainpostedited TEXT, pictureindex TEXT)")
    conn.commit()



    
    with open(r'meme.csv', 'r',encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader) # This skips the 1st row which is the header.
        cursor.executemany(query, reader)
        conn.commit()
except (Exception, psycopg2.Error) as e:
    print('fucked up','\n')
    print(e)
finally:
    if (conn):
        cursor.close()
        conn.close()
        print("Connection closed.")





# with conn:
#     cur=conn.cursor()
#     cur.execute("DROP TABLE IF EXISTS ghlinks")
#     cur.execute("CREATE TABLE ghlinks(sourcelink TEXT,imglink TEXT,posttitle TEXT, postdate TEXT, mainpostedited TEXT, pictureindex TEXT)")
	
#     query = """INSERT INTO ghlinks(sourcelink, imglink, posttitle, postdate, mainpostedited,pictureindex) VALUES(%s, %s, %s, %s, %s, %s)"""
#     cur.executemany(query,tuple(df.itertuples(index=False, name=None)))
#     conn.commit()
 
# s = ""
# s += "SELECT"
# s += " table_schema"
# s += ", table_name"
# s += " FROM information_schema.tables"
# s += " WHERE"
# s += " ("
# s += " table_schema = 'public'"
# s += " )"
# s += " ORDER BY table_schema, table_name;"
# db_cursor=conn.cursor()
# db_cursor.execute(s)
# list_tables = db_cursor.fetchall()

# for t_name_table in list_tables:
#     for i in t_name_table:
#         print(i + "\n")

# df.to_csv('meme.csv')
# sio = StringIO()
# sio.write(df.to_csv(index=None, header=None))
# sio.seek(0)
# with conn.cursor() as c:
#     c.copy_from(sio, "ghlinks", columns=df.columns, sep=',')
#     conn.commit()
# conn.close()


# class Command(BaseCommand):
    
#     def handle(self, *args, **options):
#         ImageLink.objects.all().delete()
#         for targetPage in targetPages:
#             req = requests.get(targetPage)
#             soup = BeautifulSoup(req.text,"lxml")
#             print(soup.title.string)
            
#             i=0
#             table = soup.find("table",{"class","table_grid"}).find("tbody").findAll("tr")#.findAll("td",{"class":"subject windowbg2"})
#             for row in table:
                
#                 rowElement = row.findAll("td",{"class":"subject windowbg2"})
                
#                 for subElement in rowElement: 
                    
#                     spans = subElement.find_all("span")
#                     if str(str(spans)[11:15])=='msg_':
#                         #.contents[0])
#                         print('############\n')
#                         # print(i,True)
#                         # print(str(spans).find('href=\"'))
#                         # print(str(spans).find('\"',27))
#                         # print(str(spans)[33:str(spans).find('\"',33)])
#                         # i=i+1
#                         # print(str(spans).find('>',str(spans).find('>')+1))
#                         print(str(spans)[str(spans).find('>',str(spans).find('>')+1)+1:-12])
#                         inner_req=requests.get(str(spans)[33:str(spans).find('\"',33)])
#                         inner_soup=BeautifulSoup(inner_req.text,"lxml")
                        
#                         post_dates=inner_soup.findAll("div",{"class":"smalltext"})
                        



#                         postingDateStr=str(post_dates[0])[str(post_dates[0]).find(
#                                                                 '>',
#                                                                 str(post_dates[0]).find(
#                                                                                     '>',
#                                                                                     str(post_dates[0]).find('>')+1
#                                                                                     )+1
#                                                                 )+2#+2 for space removal lol
                                                                                    
                                                                                    
#                                             :-8]

#                         post_dates_modified=inner_soup.findAll("div",{"class":"smalltext modified"})

#                         postDateModStr=str(post_dates_modified[0])[str(post_dates_modified[0]).find('>',str(post_dates_modified[0]).find('>')+1)+1:str(post_dates_modified[0]).find('<',str(post_dates_modified[0]).find('<',str(post_dates_modified[0]).find('<')+1)+1)]

#                         # for j in post_dates:
#                         #     print('\n')
#                         #     if str(j)[21:22]=='\"':print(str(j),'\n')
#                         #     # print(str(j)[21:22])
#                         #     # print('\n')
#                         #     # print('zzzzzzzzzz')
#                         #     # print('\n')

                        
#                         pictures=inner_soup.findAll("a",{"class":"highslide"})
#                         counterQ=0
#                         for i in pictures:
#                             print('___\n')
#                             print('i:',i)
#                             print(str(i)[27:str(i).find('\"',27)])
#                             ImageLink.objects.create(source=str(spans)[33:str(spans).find('\"',33)],imgLink=str(i)[27:str(i).find('\"',27)],postTitle=str(spans)[str(spans).find('>',str(spans).find('>')+1)+1:str(spans).find('<',str(spans).find('<',str(spans).find('<')+1)+1)],postDate=postingDateStr,mainPostEdited=postDateModStr,pictureIndex=counterQ)
#                             print('___\n')
#                             counterQ=counterQ+1
#                         print('############\n')
                
            
        