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



select b.*,s.industry,s.industry_classified,s.mktcap,s.timeToMarket,rpe.pe1,rpe.price,rpe.eval_price,rpe.eval_price_ratio,rpe.std_devi from buffett b
	join stockinfo s on b.code = s.code
 join realtime_pe_eps rpe on b.code = rpe.code
  where rpe.eval_price_ratio > 1 and rpe.std_devi <= 200 and s.industry != '银行' and s.industry not like '%地产%'
	order by rpe.eval_price_ratio desc;

select rpe.*,s.industry, s.industry_classified from realtime_pe_eps rpe join stockinfo s on rpe.code = s.code where rpe.pe1 > 0 and rpe.koufei_pe > 0 and rpe.koufei_pe <= 25  and s.industry != '银行' and s.industry not like '%地产%' order by rpe.koufei_pe asc;

select count(*) from realtime_pe_eps where eval_price_ratio > 1;

select * from realtime_pe_eps where eval_price_ratio > 1 and std_devi <= 100 order by eval_price_ratio desc;