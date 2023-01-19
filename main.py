import webbrowser
from Tmall import *

data = pd.read_csv("tmall_order_report.csv")
data.columns = data.columns.str.strip(' ')  # 列名去空格
data['收货地址'] = data['收货地址'].str.replace('自治区|省|壮族|维吾尔|回族', '')  # 去除后缀
data['订单创建时间'] = pd.to_datetime(data['订单创建时间'])
data['订单付款时间'] = pd.to_datetime(data['订单付款时间'])


opt = input("*******************\n"
            "请选择功能：\n"
            "1.表格\n"
            "2.订单地区分布\n"
            "3.订单日期分布\n"
            "4.订单24小时分布\n")

if opt == '1':
    get_table(data)
    file = 'table.html'

elif opt == '2':
    get_citys(data)
    file = 'citys.html'

elif opt == '3':
    get_days(data)
    file = 'days.html'

elif opt == '4':
    get_hours(data)
    file = 'hours.html'

else:
    file = 'error.html'

webbrowser.open(file, new=0, autoraise=True)


