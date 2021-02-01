import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

#####################
#manipulate data
df_order = pd.read_csv('/kaggle/input/logistics/delivery_orders_march.csv')
df_sla = pd.read_excel(r'/kaggle/input/logistics/SLA_matrix.xlsx')
#read_excel needs openpyxl xlrd
temp_order = df_order
city = ['metro manila','luzon','visayas','mindanao']
for i in city:
    temp_order.buyeraddress[df_order.buyeraddress.apply(lambda p: i.lower() in p.lower())] = i.lower()
for i in city:
    temp_order.selleraddress[df_order.selleraddress.apply(lambda p: i.lower() in p.lower())] = i.lower()
#######################
#find workday
holidays = ['2020-03-08','2020-03-25','2020-03-30','2020-03-31']
def findworkday(start,end):
    result = pd.bdate_range(start= start, end = end
              ,weekmask='Mon Tue Wed Thu Fri Sat'
               ,holidays = holidays,freq='C').size -1
    return result
#######################
#find workday between city
def findsendday(des_buy,des_sell):
    if des_buy == 'metro manila' and des_sell == 'metro manila':
        return 3
    elif des_buy == 'metro manila' and des_sell == 'luzon':
        return 5
    elif des_buy == 'luzon' and des_sell == 'metro manila':
        return 5
    elif des_buy == 'luzon' and des_sell == 'luzon':
        return 5
    else:
        return 7
########################
#logistic analyse late or not
listlate = []
for i in range(temp_order.index.size):
    if not pd.isnull(temp_order['2nd_deliver_attempt'][i]):
        workdays = findworkday(temp_order['1st_deliver_attempt'][i].date()
                               ,temp_order['2nd_deliver_attempt'][i].date())
        if workdays > 3:
            listlate.append(1)
        else:
            listlate.append(0)            
    else:
        workdays = findworkday(temp_order['pick'][i].date()
                               ,temp_order['1st_deliver_attempt'][i].date())
        properdays = findsendday(temp_order.buyeraddress[i]
                                 ,temp_order.selleraddress[i])
        if workdays <= properdays:
            listlate.append(0)
        else:
            listlate.append(1)
########################
#create output
summit = pd.DataFrame({'orderid':temp_order.orderid,'is_late':listlate})
summit.to_csv('submission.csv',index=False)