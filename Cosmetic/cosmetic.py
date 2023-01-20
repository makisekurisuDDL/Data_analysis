import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Bar, Line, Pie
import webbrowser


# 每日订单趋势
def day_orders(data):
    result_day = data.groupby('update_time', as_index=False).agg({'sale_count': 'count'})
    days = (
        Line()
        .add_xaxis(result_day['update_time'].tolist())
        .add_yaxis('订单量', result_day['sale_count'].tolist())
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
                         title_opts=opts.TitleOpts(title='每日订单量趋势'))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_='max', name='最大值'),
                    opts.MarkPointItem(type_='min', name='最小值')
                ]
            )
        )
    )

    days.render('days.html')
    webbrowser.open('days.html', new=0, autoraise=True)

    return 0


# 各品牌销量占比
def brand_sale_count(data):
    result_brand = data.groupby('店名', as_index=False).agg({'sale_count': 'sum'})
    result_brand = result_brand.sort_values(by=['sale_count'], ascending=False)
    others = result_brand[8:]
    others = others['sale_count'].sum()
    result_brand = result_brand[0:8]
    result_brand['sale_count'] = result_brand['sale_count'] / 10000
    result_brand.loc[len(result_brand)] = ['其他', others / 10000]

    brand = (
        Pie()
        .add('销量', [list(z) for z in zip(result_brand['店名'], result_brand['sale_count'])])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}万"))
        .set_global_opts(title_opts=opts.TitleOpts(title='各品牌销量占比'))
    )

    brand.render('brand_count.html')
    webbrowser.open('brand_count.html', new=0, autoraise=True)

    return 0


# 各品牌销售额占比
def brand_sale_amount(data):
    result_brand = data.groupby('店名', as_index=False).agg({'sale_amount': 'sum'})
    result_brand = result_brand.sort_values(by=['sale_amount'], ascending=False)
    others = result_brand[8:]
    others = others['sale_amount'].sum()
    result_brand = result_brand[0:8]
    result_brand['sale_amount'] = result_brand['sale_amount'] / 100000000
    result_brand.loc[len(result_brand)] = ['其他', others / 100000000]
    result_brand['sale_amount'] = result_brand['sale_amount'].apply(lambda x: ("%.2f") % x)

    brand = (
        Pie()
        .add('销售额', [list(z) for z in zip(result_brand['店名'], result_brand['sale_amount'])])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}亿"))
        .set_global_opts(title_opts=opts.TitleOpts(title='各品牌销售额占比'))
    )

    brand.render('brand_amount.html')
    webbrowser.open('brand_amount.html', new=0, autoraise=True)
    return 0
