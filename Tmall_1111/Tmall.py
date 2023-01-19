import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Bar, Line
from pyecharts.components import Table


data = pd.read_csv("tmall_order_report.csv")
data.columns = data.columns.str.strip(' ')  # 列名去空格
data['收货地址'] = data['收货地址'].str.replace('自治区|省|壮族|维吾尔|回族', '')  # 去除后缀
data['订单创建时间'] = pd.to_datetime(data['订单创建时间'])
data['订单付款时间'] = pd.to_datetime(data['订单付款时间'])

#返回统计表格
def get_table(data):
    result = {}
    result['总订单数'] = data['订单编号'].count()
    result['已完成订单数'] = data['订单编号'][data['订单付款时间'].notnull()].count()
    result['未付款订单数'] = data['订单编号'][data['订单付款时间'].isnull()].count()
    result['退款订单数'] = data['订单编号'][data['退款金额'] > 0].count()
    result['总付款金额'] = data['买家实际支付金额'].sum()
    result['总退款金额'] = data['退款金额'].sum()

    table = Table()
    headers = ['总订单数', '已完成订单数', '总付款金额', '退款订单数', '总退款金额', '成交率', '退款率']
    row = [
        [
            result['总订单数'], result['已完成订单数'], f"{result['总付款金额'] / 10000:.2f}万",
            result['退款订单数'], f"{result['总退款金额'] / 10000:.2f}万",
            f"{result['已完成订单数'] / result['总订单数']:.2%}",
            f"{result['退款订单数'] / result['总订单数']:.2%}"
        ]
    ]
    table.add(headers, row)

    return table.render('table.html')


'''
result2 = data[data['订单付款时间'].notnull()].groupby('收货地址').agg({'订单编号': 'count'})
result21 = result2.to_dict()['订单编号']
c = (
    Map()
    .add("订单量", [*result21.items()], "china", is_map_symbol_show=False)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='地区分布'),
        visualmap_opts=opts.VisualMapOpts(max_=1000),
    )
)
'''

#各城市订单统计排序
def get_citys(data):
    city_orders = data[data['订单付款时间'].notnull()].groupby('收货地址', as_index=False).agg({'订单编号': 'count'})
    city_orders = city_orders.sort_values(by=['订单编号'], ascending=False)

    bar = (
        Bar()
        .add_xaxis(city_orders['收货地址'].tolist())
        .add_yaxis('订单数量', city_orders['订单编号'].tolist(), category_gap=10)
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
                         title_opts=opts.TitleOpts(title='各城市订单数量降序'))
    )

    return bar.render('citys.html')

#每日订单趋势
def get_days(data):
    day_orders = data[['订单创建时间', '订单编号']]
    day_orders['订单创建时间'] = day_orders['订单创建时间'].apply(lambda x: x.date())
    day_orders = day_orders.groupby('订单创建时间', as_index=False).agg({'订单编号': 'count'})

    l = (
        Line()
        .add_xaxis(day_orders['订单创建时间'].tolist())
        .add_yaxis('订单量', day_orders['订单编号'].tolist())
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
                         title_opts=opts.TitleOpts(title='每日订单量趋势'))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值")
                ]
            ),
        )
    )

    return l.render('days.html')

#每小时订单趋势
def get_hours(data):
    hour_orders = data[['订单创建时间', '订单编号']]
    hour_orders['订单创建时间'] = hour_orders['订单创建时间'].apply(lambda x: x.strftime('%H'))
    hour_orders = hour_orders.groupby('订单创建时间', as_index=False).agg({'订单编号': 'count'})

    h = (
        Line()
        .add_xaxis(hour_orders['订单创建时间'].tolist())
        .add_yaxis('订单量', hour_orders['订单编号'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="每小时订单量趋势"))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name='最大值'),
                    opts.MarkPointItem(type_="min", name='最小值')
                ]
            )
        )
    )

    return h.render('hours.html')

