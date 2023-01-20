from cosmetic import *

data = pd.read_csv("cosmetic.csv")

data.drop_duplicates(inplace=True)   #数据去重
data.reset_index(drop=True, inplace=True)   #索引重置
data.fillna(0, inplace=True)    #空数据填充
data['update_time'] = pd.to_datetime(data['update_time']).apply(lambda x: x.strftime("%Y-%m-%d"))
data['sale_amount'] = data['sale_count'] * data['price']    #新增“销售额”列


opt = input("********************\n"
            "请选择功能：\n"
            "1.每日订单量趋势\n"
            "2.各品牌销量占比\n"
            "3.各品牌销售额占比\n")

if opt == '1':
    day_orders(data)
elif opt == '2':
    brand_sale_count(data)
elif opt == '3':
    brand_sale_amount(data)
else:
    webbrowser.open('error.html', new=0, autoraise=True)
