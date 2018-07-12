# 按日期查询当天股票大单数据总统计排名前100的
select ds.*,h.open,h.close,h.p_change from (select * from dd_sts where date = '2018-07-11' order by net desc limit 100) ds left join hist_data h on ds.code = h.code and ds.date = h.date;
# 按日期查询当天股票大单数据最后半小时统计排名前100的
select ds.*,h.open,h.close,h.p_change from (select * from dd_sts where date = '2018-07-11' order by lhh_net desc limit 100)  ds left join hist_data h on ds.code = h.code and ds.date = h.date;
# 按日期查询当天股票大单数据占总市值比率统计排名前100的
select ds.*,h.open,h.close,h.p_change from (select * from dd_sts where date = '2018-07-11' order by ratio desc limit 100) ds left join hist_data h on ds.code = h.code and ds.date = h.date;


# 查询某股票大单某日期统计数据，并且显示当日涨跌情况
select ds.*,h.open,h.close,h.p_change from (select * from dd_sts where date in ('2018-07-12') and code in ('300090')) ds left join hist_data h on ds.code = h.code and ds.date = h.date;

# 查询某日某股票大单明细
select * from dd where date in ('2018-07-12') and code in ('300090')