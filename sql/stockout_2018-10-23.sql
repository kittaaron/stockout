# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.22)
# Database: stockout
# Generation Time: 2018-10-23 07:20:11 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table broker_tops
# ------------------------------------------------------------

CREATE TABLE `broker_tops` (
  `broker` text,
  `count` bigint(20) DEFAULT NULL,
  `bamount` double DEFAULT NULL,
  `bcount` bigint(20) DEFAULT NULL,
  `samount` double DEFAULT NULL,
  `scount` bigint(20) DEFAULT NULL,
  `top3` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table cap_tops
# ------------------------------------------------------------

CREATE TABLE `cap_tops` (
  `code` text,
  `name` text,
  `count` bigint(20) DEFAULT NULL,
  `bamount` double DEFAULT NULL,
  `samount` double DEFAULT NULL,
  `net` double DEFAULT NULL,
  `bcount` bigint(20) DEFAULT NULL,
  `scount` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table cwbbzy
# ------------------------------------------------------------

CREATE TABLE `cwbbzy` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL,
  `name` varchar(8) NOT NULL,
  `date` varchar(10) NOT NULL,
  `revenue` decimal(16,2) NOT NULL COMMENT '营业收入',
  `oper_cost` decimal(16,2) NOT NULL COMMENT '营业成本 ',
  `oper_income` decimal(16,2) NOT NULL COMMENT '营业利润',
  `profit_before_tax` decimal(16,2) NOT NULL COMMENT '利润总额',
  `income_tax` decimal(16,2) NOT NULL COMMENT '所得税',
  `net_profit` decimal(16,2) NOT NULL COMMENT '净利润',
  `eps` decimal(16,2) NOT NULL COMMENT '基本每股收益',
  `moneytory_funds` decimal(16,2) NOT NULL COMMENT '货币资金',
  `cash_receivable` decimal(16,2) NOT NULL COMMENT '应收账款',
  `inventories` decimal(16,2) NOT NULL COMMENT '存货',
  `tca` decimal(16,2) NOT NULL COMMENT '流动资产合计',
  `fixed_assets` decimal(16,2) NOT NULL COMMENT '固定资产',
  `total_assets` decimal(16,2) NOT NULL COMMENT '资产总计',
  `total_current_liabi` decimal(16,2) NOT NULL COMMENT '流动负债',
  `total_not_current_liabi` decimal(16,2) NOT NULL COMMENT '非流动负债',
  `total_liabi` decimal(16,2) NOT NULL COMMENT '负债合计',
  `sh_eq` decimal(16,2) NOT NULL COMMENT '股东权益合计',
  `oper_balance` decimal(16,2) NOT NULL COMMENT 'operating balance of cash and cash equivalence',
  `net_cash_f_oper` decimal(16,2) NOT NULL COMMENT '经营活动产生的现金流量净额(net cash from operation activites)',
  `net_cash_f_invest` decimal(16,2) NOT NULL COMMENT '投资活动产生的现金流量净额(net cash from investment activites)',
  `net_cash_f_finance` decimal(16,2) NOT NULL COMMENT '筹资活动产生的现金流量净额(net cash from financing activites)',
  `net_increase` decimal(16,2) NOT NULL COMMENT '现金及现金等价物增加额net increase in cash and cash equivalents',
  `closing_balance` decimal(16,2) NOT NULL COMMENT 'closing balance of cash and cash equivalence',
  PRIMARY KEY (`id`),
  KEY `idx_code` (`code`),
  KEY `idx_name` (`name`),
  KEY `idx_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table dd
# ------------------------------------------------------------

CREATE TABLE `dd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(16) DEFAULT '',
  `name` varchar(16) DEFAULT '',
  `date` varchar(12) DEFAULT '' COMMENT '日期',
  `time` varchar(12) DEFAULT '' COMMENT '交易时间. 例:14:58:10',
  `price` double DEFAULT NULL COMMENT '当前价格',
  `volume` bigint(20) DEFAULT NULL COMMENT '成交手',
  `preprice` double DEFAULT NULL COMMENT '上一笔价格',
  `type` varchar(4) DEFAULT '' COMMENT '买卖类型【买盘、卖盘、中性盘】',
  PRIMARY KEY (`id`),
  KEY `idx_code_date` (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='大单交易数据明细';



# Dump of table dd_sts
# ------------------------------------------------------------

CREATE TABLE `dd_sts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(16) DEFAULT '',
  `name` varchar(16) DEFAULT '',
  `date` varchar(12) DEFAULT '' COMMENT '日期',
  `b_volume` bigint(20) DEFAULT NULL COMMENT '买盘总成交手',
  `s_volume` bigint(20) DEFAULT NULL COMMENT '卖盘总成交手',
  `net` bigint(20) DEFAULT NULL COMMENT '总净值(b_volume - s_volume)',
  `lhh_b_volume` bigint(20) DEFAULT NULL COMMENT 'last_half_hour最后半小时买盘总成交手',
  `lhh_s_volume` bigint(20) DEFAULT NULL COMMENT '最后半小时卖盘总成交手',
  `lhh_net` bigint(20) DEFAULT NULL COMMENT '最后半小时总净值(b_volume - s_volume)',
  `ratio` decimal(16,4) DEFAULT NULL COMMENT 'net_占总股本比率',
  `lhh_ratio` decimal(16,4) DEFAULT NULL COMMENT 'lhh_net_占总股本比率',
  `fhh_b_volume` bigint(20) DEFAULT NULL COMMENT 'first_half_hour前半小时买盘总成交手',
  `fhh_s_volume` bigint(20) DEFAULT NULL COMMENT '前半小时卖盘总成交手',
  `fhh_net` bigint(20) DEFAULT NULL COMMENT '前半小时总净值(b_volume - s_volume)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code_date` (`code`,`date`),
  KEY `date` (`date`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='大单交易数据统计';



# Dump of table extra_zb
# ------------------------------------------------------------

CREATE TABLE `extra_zb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(8) NOT NULL,
  `name` varchar(12) NOT NULL,
  `date` varchar(10) NOT NULL,
  `acid_ratio` decimal(16,2) DEFAULT NULL COMMENT '速动比率',
  `liquidity_ratio` decimal(16,2) DEFAULT NULL COMMENT '流动比率',
  `por_yoy` decimal(16,2) DEFAULT NULL COMMENT '主营业务收入同比',
  `pop_yoy` decimal(16,2) DEFAULT NULL COMMENT '主营业务利润同比',
  `net_yoy` decimal(16,2) DEFAULT NULL COMMENT '净利润同比',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table fpya
# ------------------------------------------------------------

CREATE TABLE `fpya` (
  `code` text,
  `name` text,
  `year` bigint(20) DEFAULT NULL,
  `report_date` text,
  `divi` double DEFAULT NULL,
  `shares` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table good_stock
# ------------------------------------------------------------

CREATE TABLE `good_stock` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(8) NOT NULL DEFAULT '',
  `name` varchar(16) NOT NULL DEFAULT '',
  `industry_top` varchar(64) DEFAULT '' COMMENT '优秀的原因',
  `industry_classified_top` varchar(64) DEFAULT NULL COMMENT 'industry_classified排名',
  `blue_chip` varchar(64) DEFAULT NULL COMMENT '蓝筹信息',
  `industry` varchar(64) DEFAULT '' COMMENT '行业',
  `industry_classified` varchar(64) DEFAULT NULL COMMENT '行业(另一维度)',
  `notice` varchar(64) DEFAULT NULL COMMENT '蓝筹信息',
  PRIMARY KEY (`id`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table hist_data
# ------------------------------------------------------------

CREATE TABLE `hist_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(16) NOT NULL,
  `name` varchar(16) NOT NULL,
  `date` varchar(10) NOT NULL DEFAULT '' COMMENT '日期',
  `open` decimal(16,3) DEFAULT NULL COMMENT '开盘价',
  `high` decimal(16,3) DEFAULT NULL COMMENT '高点',
  `close` decimal(16,3) DEFAULT NULL COMMENT '收盘价',
  `low` decimal(16,3) DEFAULT NULL COMMENT '最低价',
  `volume` decimal(16,2) DEFAULT NULL COMMENT '成交量',
  `price_change` decimal(16,2) DEFAULT NULL COMMENT '价格变动',
  `p_change` decimal(16,2) DEFAULT NULL COMMENT '涨跌幅',
  `ma5` decimal(16,3) DEFAULT NULL COMMENT '5日均价',
  `ma10` decimal(16,3) DEFAULT NULL COMMENT '10日均价',
  `ma20` decimal(16,3) DEFAULT NULL COMMENT '20日均价',
  `v_ma5` decimal(16,2) DEFAULT NULL COMMENT '5日均量',
  `v_ma10` decimal(16,2) DEFAULT NULL COMMENT '10日均量',
  `v_ma20` decimal(16,2) DEFAULT NULL COMMENT '20日均量',
  `turnover` decimal(16,2) DEFAULT NULL COMMENT '换手率',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code_date` (`code`,`date`),
  KEY `idx_name` (`name`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table holiday
# ------------------------------------------------------------

CREATE TABLE `holiday` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `holiday_date` varchar(10) NOT NULL DEFAULT '' COMMENT 'yyyy-mm-dd格式的日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table index_data
# ------------------------------------------------------------

CREATE TABLE `index_data` (
  `code` text,
  `name` text,
  `change` double DEFAULT NULL,
  `open` double DEFAULT NULL,
  `preclose` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `volume` bigint(20) DEFAULT NULL,
  `amount` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table inst_detail
# ------------------------------------------------------------

CREATE TABLE `inst_detail` (
  `code` text,
  `name` text,
  `date` text,
  `bamount` double DEFAULT NULL,
  `samount` double DEFAULT NULL,
  `type` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table inst_tops
# ------------------------------------------------------------

CREATE TABLE `inst_tops` (
  `code` text,
  `name` text,
  `bamount` double DEFAULT NULL,
  `bcount` bigint(20) DEFAULT NULL,
  `samount` double DEFAULT NULL,
  `scount` bigint(20) DEFAULT NULL,
  `net` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table jjcg
# ------------------------------------------------------------

CREATE TABLE `jjcg` (
  `code` text,
  `name` text,
  `date` text,
  `nums` text,
  `nlast` text,
  `count` text,
  `clast` text,
  `amount` text,
  `ratio` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table lhb
# ------------------------------------------------------------

CREATE TABLE `lhb` (
  `code` text,
  `name` text,
  `pchange` text,
  `amount` text,
  `buy` text,
  `sell` text,
  `reason` text,
  `bratio` text,
  `sratio` text,
  `date` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table lrb
# ------------------------------------------------------------

CREATE TABLE `lrb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL,
  `name` varchar(10) NOT NULL,
  `date` varchar(10) NOT NULL,
  `revenue` decimal(16,2) NOT NULL COMMENT '营业收入',
  `interest_revenue` decimal(16,2) NOT NULL COMMENT '利息收入',
  `other_revenue` decimal(16,2) NOT NULL COMMENT '其他业务收入',
  `oper_cost` decimal(16,2) NOT NULL COMMENT '营业总成本',
  `sales_expense` decimal(16,2) NOT NULL COMMENT '销售费用',
  `manage_expense` decimal(16,2) NOT NULL COMMENT '管理费用',
  `finalcial_expense` decimal(16,2) NOT NULL COMMENT '财务费用',
  `asset_derease` decimal(16,2) NOT NULL COMMENT '资产减值',
  `fair_val_change_income` decimal(16,2) NOT NULL COMMENT '公允价值变动收益',
  `invest_income` decimal(16,2) NOT NULL COMMENT '投资收益',
  `oper_profit` decimal(16,2) NOT NULL COMMENT '营业利润',
  `non_biz_income` decimal(16,2) NOT NULL COMMENT '营业外收入',
  `non_biz_expense` decimal(16,2) NOT NULL COMMENT '营业外支出',
  `profit` decimal(16,2) NOT NULL COMMENT '利润总额',
  `tax` decimal(16,2) NOT NULL COMMENT '所得税费用',
  `net_profit` decimal(16,2) NOT NULL COMMENT '净利润',
  `net_profit_t_p` decimal(16,2) NOT NULL COMMENT '归属于母公司的净利润',
  `net_profit_b_m` decimal(16,2) NOT NULL COMMENT '被合并方在合并前实现净利润',
  `minority_equity` decimal(16,2) NOT NULL COMMENT '少数股东损益',
  `eps` decimal(16,2) NOT NULL COMMENT '基本每股收益',
  `dilute_eps` decimal(16,2) NOT NULL COMMENT '稀释每股收益',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `name` (`name`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table new_stocks
# ------------------------------------------------------------

CREATE TABLE `new_stocks` (
  `code` text,
  `xcode` text,
  `name` text,
  `ipo_date` text,
  `issue_date` text,
  `amount` bigint(20) DEFAULT NULL,
  `markets` bigint(20) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `pe` double DEFAULT NULL,
  `limit` double DEFAULT NULL,
  `funds` double DEFAULT NULL,
  `ballot` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table por_yoy_sts
# ------------------------------------------------------------

CREATE TABLE `por_yoy_sts` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) DEFAULT NULL,
  `name` varchar(16) DEFAULT NULL,
  `por_grow_cnt` int(11) DEFAULT NULL,
  `por_grow_10_cnt` int(11) DEFAULT NULL,
  `por_grow_20_cnt` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_grow_cnt` (`por_grow_cnt`),
  KEY `idx_grow_10_cnt` (`por_grow_10_cnt`),
  KEY `idx_grow_20_cnt` (`por_grow_20_cnt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table realtime_pe
# ------------------------------------------------------------

CREATE TABLE `realtime_pe` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(8) NOT NULL DEFAULT '',
  `name` varchar(16) NOT NULL DEFAULT '',
  `pe` decimal(16,2) NOT NULL DEFAULT '0.00',
  `eps` decimal(16,2) NOT NULL,
  `price` decimal(16,2) NOT NULL,
  `date` varchar(10) NOT NULL DEFAULT '',
  `pe2` decimal(16,2) NOT NULL DEFAULT '0.00',
  `eps2` decimal(16,2) NOT NULL,
  `pe3` decimal(16,2) NOT NULL DEFAULT '0.00',
  `eps3` decimal(16,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table realtime_pe_eps
# ------------------------------------------------------------

CREATE TABLE `realtime_pe_eps` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(8) DEFAULT '',
  `name` varchar(16) DEFAULT '',
  `koufei_pe` decimal(16,2) NOT NULL COMMENT '扣非PE',
  `pe1` decimal(16,2) DEFAULT NULL COMMENT '最近一次季报计算',
  `pe2` decimal(16,2) DEFAULT NULL COMMENT '上一年度报表计算',
  `pe3` decimal(16,2) DEFAULT NULL COMMENT '上二年度报表计算',
  `pe4` decimal(16,2) DEFAULT NULL COMMENT '上二年度报表计算',
  `koufei_eps` decimal(16,2) NOT NULL COMMENT '扣非每股收益',
  `eps1` decimal(16,2) DEFAULT NULL COMMENT '最近一次季报计算的每股收益',
  `eps2` decimal(16,2) DEFAULT NULL,
  `eps3` decimal(16,2) DEFAULT NULL,
  `eps4` decimal(16,2) DEFAULT NULL,
  `price` decimal(16,2) NOT NULL COMMENT '价格',
  `date` varchar(10) NOT NULL DEFAULT '' COMMENT '某日期的价格',
  `latest_report_date` varchar(10) NOT NULL DEFAULT '' COMMENT '最近的财报日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table report_data
# ------------------------------------------------------------

CREATE TABLE `report_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL DEFAULT '',
  `name` varchar(32) NOT NULL DEFAULT '',
  `year` int(11) NOT NULL COMMENT '年份',
  `season` tinyint(3) NOT NULL COMMENT '季度(1,2,3,4)',
  `eps` decimal(16,2) DEFAULT NULL COMMENT '每股收益',
  `eps_yoy` decimal(16,2) DEFAULT NULL COMMENT '每股收益同比(%)',
  `bvps` decimal(16,2) DEFAULT NULL COMMENT '每股净资产',
  `roe` decimal(16,2) DEFAULT NULL COMMENT '净资产收益率(%)',
  `epcf` decimal(16,2) DEFAULT NULL COMMENT '每股现金流量(元)',
  `net_profits` decimal(16,2) DEFAULT NULL COMMENT '净利润(万元)',
  `profits_yoy` decimal(16,2) DEFAULT NULL COMMENT '净利润同比(%)',
  `distrib` varchar(128) DEFAULT '' COMMENT '分配方案',
  `report_date` varchar(12) NOT NULL DEFAULT '',
  `net_profit_ratio` decimal(16,2) DEFAULT NULL COMMENT '净利率(%)',
  `gross_profit_rate` decimal(16,4) DEFAULT NULL COMMENT '毛利率(%)',
  `business_income` decimal(16,4) DEFAULT NULL COMMENT '营业收入(百万元)',
  `bips` decimal(16,4) DEFAULT NULL COMMENT '每股主营业务收入(元)',
  `arturnover` decimal(16,4) DEFAULT NULL COMMENT '应收账款周转率(次)',
  `arturndays` decimal(16,4) DEFAULT NULL COMMENT '应收账款周转天数(天)',
  `inventory_turnover` decimal(16,4) DEFAULT NULL COMMENT '存货周转率(次)',
  `inventory_days` decimal(16,4) DEFAULT NULL COMMENT '存货周转天数(天)',
  `currentasset_turnover` decimal(16,4) DEFAULT NULL COMMENT '流动资产周转率(次)',
  `currentasset_days` decimal(16,4) DEFAULT NULL COMMENT '流动资产周转天数(天)',
  `mbrg` decimal(16,2) DEFAULT NULL COMMENT '主营业务收入增长率(%)',
  `nprg` decimal(16,2) DEFAULT NULL COMMENT '净利润增长率(%)',
  `nav` decimal(16,4) DEFAULT NULL COMMENT '净资产增长率',
  `targ` decimal(16,4) DEFAULT NULL COMMENT '总资产增长率',
  `epsg` decimal(16,4) DEFAULT NULL COMMENT '每股收益增长率',
  `seg` decimal(16,4) DEFAULT NULL COMMENT '股东权益增长率',
  `currentratio` decimal(16,4) DEFAULT NULL COMMENT '流动比率',
  `quickratio` decimal(16,4) DEFAULT NULL COMMENT '速动比率',
  `cashratio` decimal(16,4) DEFAULT NULL COMMENT '现金比率',
  `icratio` decimal(16,4) DEFAULT NULL COMMENT '利息支付倍数',
  `sheqratio` decimal(16,4) DEFAULT NULL COMMENT '股东权益比率',
  `adratio` decimal(16,4) DEFAULT NULL COMMENT '股东权益增长率',
  `cf_sales` decimal(16,4) DEFAULT NULL COMMENT '经营现金净流量对销售收入比率',
  `rateofreturn` decimal(16,4) DEFAULT NULL COMMENT '资产的经营现金流量回报率',
  `cf_nm` decimal(16,4) DEFAULT NULL COMMENT '经营现金净流量与净利润的比率',
  `cf_liabilities` decimal(16,4) DEFAULT NULL COMMENT '经营现金净流量对负债比率',
  `cashflowratio` decimal(16,4) DEFAULT NULL COMMENT '现金流量比率',
  PRIMARY KEY (`id`),
  KEY `idx_code_year` (`code`,`year`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table rzrq_total
# ------------------------------------------------------------

CREATE TABLE `rzrq_total` (
  `rzmre` bigint(20) DEFAULT NULL,
  `rzye` bigint(20) DEFAULT NULL,
  `rqmcl` bigint(20) DEFAULT NULL,
  `rqyl` bigint(20) DEFAULT NULL,
  `rqye` bigint(20) DEFAULT NULL,
  `rzrqye` bigint(20) DEFAULT NULL,
  `opDate` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table select
# ------------------------------------------------------------

CREATE TABLE `select` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL DEFAULT '',
  `name` varchar(12) NOT NULL DEFAULT '',
  `cc` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否持仓',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table select_candidate
# ------------------------------------------------------------

CREATE TABLE `select_candidate` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL DEFAULT '',
  `name` varchar(12) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table stockinfo
# ------------------------------------------------------------

CREATE TABLE `stockinfo` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(64) NOT NULL DEFAULT '' COMMENT '股票名称',
  `industry` varchar(64) DEFAULT '' COMMENT '股票行业',
  `industry_classified` varchar(64) DEFAULT '' COMMENT '行业名称',
  `concept_classified` varchar(64) DEFAULT '' COMMENT '概念名称',
  `area` varchar(64) NOT NULL DEFAULT '' COMMENT '股票地区',
  `pe` decimal(16,2) NOT NULL COMMENT '市盈率(市价P/盈利Earning比率)',
  `pb` decimal(16,2) NOT NULL COMMENT '市净率(市价P/Book value净资产)',
  `outstanding` decimal(16,2) NOT NULL COMMENT '流通股本(亿)',
  `totals` decimal(16,2) NOT NULL COMMENT '总股本(亿)',
  `totalAssets` decimal(16,2) NOT NULL COMMENT '总资产(万)',
  `liquidAssets` decimal(16,2) NOT NULL COMMENT '流动资产',
  `fixedAssets` decimal(16,2) NOT NULL COMMENT '固定资产',
  `reserved` decimal(16,2) NOT NULL COMMENT '公积金',
  `reservedPerShare` decimal(16,2) NOT NULL COMMENT '每股公积金',
  `esp` decimal(16,4) NOT NULL COMMENT '每股收益',
  `bvps` decimal(16,2) NOT NULL COMMENT '每股净资',
  `timeToMarket` varchar(16) NOT NULL DEFAULT '' COMMENT '上市日期',
  `undp` decimal(16,2) NOT NULL COMMENT '未分利润',
  `perundp` decimal(16,2) NOT NULL COMMENT '每股未分配',
  `rev` decimal(16,2) NOT NULL COMMENT '收入同比(%)',
  `profit` decimal(16,2) NOT NULL COMMENT '利润同比(%)',
  `gpr` decimal(16,2) NOT NULL COMMENT '毛利率(%)',
  `npr` decimal(16,2) NOT NULL COMMENT '净利润率(%)',
  `holders` int(11) NOT NULL COMMENT '股东人数',
  `issz50` tinyint(3) NOT NULL DEFAULT '0' COMMENT '是否上证50股',
  `iszz500` tinyint(3) NOT NULL DEFAULT '0' COMMENT '是否中证500',
  `mktcap` decimal(16,2) NOT NULL COMMENT '总市值',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`),
  KEY `idx_industry_classified` (`industry_classified`),
  KEY `idx_concept_classified` (`concept_classified`),
  KEY `idx_industry` (`industry`),
  KEY `idx_concept` (`concept_classified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table stockweight
# ------------------------------------------------------------

CREATE TABLE `stockweight` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(10) NOT NULL DEFAULT '' COMMENT '名称',
  `date` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `weight` decimal(16,2) NOT NULL COMMENT '权重',
  PRIMARY KEY (`id`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table tick_data
# ------------------------------------------------------------

CREATE TABLE `tick_data` (
  `time` text,
  `price` double DEFAULT NULL,
  `pchange` text,
  `change` double DEFAULT NULL,
  `volume` bigint(20) DEFAULT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `type` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table today_all
# ------------------------------------------------------------

CREATE TABLE `today_all` (
  `code` text,
  `name` text,
  `changepercent` double DEFAULT NULL,
  `trade` double DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `settlement` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `turnoverratio` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `per` double DEFAULT NULL,
  `pb` double DEFAULT NULL,
  `mktcap` double DEFAULT NULL,
  `nmc` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table today_data
# ------------------------------------------------------------

CREATE TABLE `today_data` (
  `index` bigint(20) DEFAULT NULL,
  `code` text,
  `name` text,
  `changepercent` double DEFAULT NULL COMMENT '涨跌幅',
  `trade` double DEFAULT NULL COMMENT '现价',
  `open` double DEFAULT NULL COMMENT '开盘价',
  `high` double DEFAULT NULL COMMENT '最高价',
  `low` double DEFAULT NULL COMMENT '最低价',
  `settlement` double DEFAULT NULL COMMENT '昨日收盘价',
  `volume` double DEFAULT NULL COMMENT '成交量',
  `turnoverratio` double DEFAULT NULL COMMENT '换手率',
  `amount` double DEFAULT NULL COMMENT '成交量',
  `per` double DEFAULT NULL COMMENT '市盈率',
  `pb` double DEFAULT NULL COMMENT '市净率',
  `mktcap` double DEFAULT NULL COMMENT '总市值',
  `nmc` double DEFAULT NULL COMMENT '流通市值',
  KEY `ix_today_data_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table xjllb
# ------------------------------------------------------------

CREATE TABLE `xjllb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL,
  `name` varchar(10) NOT NULL,
  `date` varchar(10) NOT NULL,
  `cash_receive_f_s_s` decimal(16,2) NOT NULL COMMENT '销售商品、提供劳务收到的现金\\n\\nCash received from sales of goods and services',
  `deposit_increase` decimal(16,2) NOT NULL COMMENT ' 客户存款和同业存放款项净增加额(万元)',
  `cash_in_oper` decimal(16,2) NOT NULL COMMENT ' 经营活动现金流入小计(万元)',
  `cash_paid_f_g_s` decimal(16,2) NOT NULL COMMENT ' 购买商品、接受劳务支付的现金(万元)\nCash paid for goods and services',
  `cash_paid_f_w_e` decimal(16,2) NOT NULL COMMENT ' 支付给职工以及为职工支付的现金(万元)Cash paid to workers and employees',
  `cash_out_oper` decimal(16,2) NOT NULL COMMENT '经营活动现金流出小计(万元)',
  `cash_net_oper` decimal(16,2) NOT NULL COMMENT ' 经营活动产生的现金流量净额(万元)',
  `cash_reveive_f_i_r` decimal(16,2) NOT NULL COMMENT ' 取得投资收益所收到的现金(万元)',
  `cash_in_investment` decimal(16,2) NOT NULL COMMENT ' 投资活动现金流入小计(万元)',
  `cash_paid_f_f_i_l` decimal(16,2) NOT NULL COMMENT ' 支付给职工以及为职工支付的现金(万元)Cash paid to workers and employeesCash paid for the purchase of fixed assets, intangible assets and other long-term assets',
  `cash_paid_f_investment` decimal(16,2) NOT NULL COMMENT ' 投资所支付的现金(万元)',
  `cash_receive_f_sub` decimal(16,2) NOT NULL COMMENT ' 取得子公司及其他营业单位支付的现金净额(万元)',
  `cash_out_investment` decimal(16,2) NOT NULL COMMENT ' 投资活动现金流出小计(万元)',
  `cash_net_investment` decimal(16,2) NOT NULL COMMENT ' 投资活动产生的现金流量净额(万元)',
  `cash_in_finance` decimal(16,2) NOT NULL COMMENT ' 筹资活动现金流入小计(万元)',
  `cash_out_finance` decimal(16,2) NOT NULL COMMENT ' 筹资活动现金流出小计(万元)',
  `cash_net_finance` decimal(16,2) NOT NULL COMMENT ' 筹资活动产生的现金流量净额(万元)',
  `net_incre_cash_equi` decimal(16,2) NOT NULL COMMENT ' 现金及现金等价物净增加额(万元)',
  `cash_equi_beginning` decimal(16,2) NOT NULL COMMENT '期初现金及现金等价物余额',
  `cash_equi_end` decimal(16,2) NOT NULL COMMENT '期初现金及现金等价物余额',
  `net` decimal(16,2) NOT NULL COMMENT ' 净利润(万元)',
  `minority_interest` decimal(16,2) NOT NULL COMMENT ' 少数股东损益(万元',
  `financial_cost` decimal(16,2) NOT NULL COMMENT ' 财务费用(万元)',
  `investment_losses` decimal(16,2) NOT NULL COMMENT ' 投资损失(万元)',
  `inventories_decre` decimal(16,2) NOT NULL COMMENT ' 存货的减少(万元)',
  `others` decimal(16,2) NOT NULL COMMENT ' 其他(万元)',
  `cash_end` decimal(16,2) NOT NULL COMMENT ' 现金的期末余额(万元)',
  `cash_beginning` decimal(16,2) NOT NULL COMMENT ' 现金的期初余额(万元)',
  `cash_equi_incre` decimal(16,2) NOT NULL COMMENT ' 现金及现金等价物的净增加额(万元)',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `name` (`name`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table xsjj
# ------------------------------------------------------------

CREATE TABLE `xsjj` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL DEFAULT '',
  `name` varchar(16) NOT NULL DEFAULT '',
  `date` varchar(10) DEFAULT '',
  `count` decimal(16,2) DEFAULT NULL COMMENT '解禁数量(万股)',
  `ratio` decimal(16,4) DEFAULT NULL COMMENT '占总股比例',
  PRIMARY KEY (`id`),
  KEY `idx_code` (`code`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table yjyg
# ------------------------------------------------------------

CREATE TABLE `yjyg` (
  `code` text,
  `name` text,
  `type` text,
  `report_date` text,
  `pre_eps` double DEFAULT NULL,
  `range` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table zcfzb
# ------------------------------------------------------------

CREATE TABLE `zcfzb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL,
  `name` varchar(8) NOT NULL,
  `date` varchar(10) NOT NULL DEFAULT '',
  `moneytory_funds` decimal(10,0) NOT NULL COMMENT '货币资金',
  `note_receivable` decimal(16,2) NOT NULL COMMENT '应收票据',
  `cash_receivable` decimal(16,2) NOT NULL COMMENT '应收账款',
  `ats` decimal(16,2) NOT NULL COMMENT '预付货款advances to suppliers',
  `interest_receivable` decimal(16,2) NOT NULL COMMENT '应收利息',
  `other_receivables` decimal(16,2) NOT NULL COMMENT '其他应收款',
  `inventories` decimal(16,2) NOT NULL COMMENT '存货',
  `prepaid_expence` decimal(16,2) NOT NULL COMMENT '待摊费用',
  `oca` decimal(16,2) NOT NULL COMMENT '其他流动资产other current assets',
  `tca` decimal(16,2) NOT NULL COMMENT '流动资产合计total current assets',
  `fixed_assets_cost` decimal(16,2) NOT NULL COMMENT '固定资产原价',
  `acc_depre` decimal(10,0) NOT NULL COMMENT '累计折旧',
  `fixed_assets_disposal` decimal(16,2) NOT NULL COMMENT '固定资产清理',
  `fixed_assets` decimal(16,2) NOT NULL COMMENT '固定资产',
  `cig` decimal(16,2) NOT NULL COMMENT '在建工程consturction in progress',
  `intan_assets` decimal(16,2) NOT NULL COMMENT '无形资产 intangible assets',
  `shangyu` decimal(16,2) NOT NULL COMMENT '负债和股东权益合计',
  `deferred_taxes` decimal(16,2) NOT NULL COMMENT '递延所得税',
  `total_n_c_a` decimal(16,2) NOT NULL COMMENT '非流动资产合计',
  `total_assets` decimal(16,2) NOT NULL COMMENT '总资产',
  `short_term_loans` decimal(16,2) NOT NULL COMMENT '短期借款',
  `notes_payable` decimal(16,2) NOT NULL COMMENT '应付票据',
  `accounts_payable` decimal(16,2) NOT NULL COMMENT '应付账款',
  `a_f_c` decimal(16,2) NOT NULL COMMENT '预收账款advances from customers',
  `total_current_liabi` decimal(16,2) NOT NULL COMMENT '流动负债合计',
  `total_not_current_liabi` decimal(16,2) NOT NULL COMMENT '非流动负债合计',
  `total_liabi` decimal(16,2) NOT NULL COMMENT '负债合计',
  `paid_in_capital` decimal(16,2) NOT NULL COMMENT '实收资本',
  `capital_reserve` decimal(16,2) NOT NULL COMMENT '资本公积',
  `capital_surplus` decimal(16,2) NOT NULL COMMENT '盈余资本公积',
  `un_dis_profit` decimal(16,2) NOT NULL COMMENT '未分配利润',
  `b_p_c_sh_eq` decimal(16,2) NOT NULL COMMENT '归属于母公司股东权益合计(万元)',
  `minor_equity` decimal(16,2) NOT NULL COMMENT '少数股东权益',
  `sh_eq` decimal(16,2) NOT NULL COMMENT '股东权益合计',
  `sheq_liabi_sum` decimal(16,2) NOT NULL COMMENT '负债和股东权益合计',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `name` (`name`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table zycwzb
# ------------------------------------------------------------

CREATE TABLE `zycwzb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `name` varchar(10) NOT NULL,
  `date` varchar(10) NOT NULL DEFAULT '',
  `eps` decimal(16,2) DEFAULT NULL COMMENT '基本每股收益(元)',
  `bvps` decimal(16,2) DEFAULT NULL COMMENT '每股净资产',
  `epcf` decimal(16,2) DEFAULT NULL COMMENT '每股经营活动产生的现金流量净额(元)',
  `por` decimal(16,2) DEFAULT NULL COMMENT '主营业务收入(万元)Prime operating revenue',
  `pop` decimal(16,2) DEFAULT NULL COMMENT '主营业务利润(万元)principal operations profit',
  `profit` decimal(16,2) DEFAULT NULL COMMENT '营业利润(万元)',
  `invest_income` decimal(16,2) DEFAULT NULL COMMENT '投资收益(万元)',
  `non_op_income` decimal(16,2) DEFAULT NULL COMMENT '营业外收支净额(万元)',
  `total_profit` decimal(16,2) DEFAULT NULL COMMENT '利润总额(万元)',
  `net_profit` decimal(16,2) DEFAULT NULL COMMENT '净利润(万元)',
  `npad` decimal(16,2) DEFAULT NULL COMMENT '净利润(扣除非经常性损益后)(万元)Net profit after deduction of non',
  `cffoa` decimal(16,2) DEFAULT NULL COMMENT '经营活动产生的现金流量净额(万元)经营活动产生的现金流量净额(万元)经营活动产生的现金流量净额(万元)经营活动产生的现金流量净额(万元)cash flows from operation activities',
  `niicce` decimal(16,2) DEFAULT NULL COMMENT '现金及现金等价物净增加额(万元)经营活动产生的现金流量净额(万元)net increase in cash and cash equivalents',
  `total_assets` decimal(16,2) DEFAULT NULL COMMENT '总资产(万元)',
  `flow_assets` decimal(16,2) DEFAULT NULL COMMENT '流动资产(万元)',
  `total_debts` decimal(16,2) DEFAULT NULL COMMENT '总负债(万元)',
  `flow_debts` decimal(16,2) DEFAULT NULL COMMENT '流动负债(万元)',
  `sheq` decimal(16,2) DEFAULT NULL COMMENT '股东权益不含少数股东权益(万元)',
  `wroe` decimal(16,2) DEFAULT NULL COMMENT '净资产收益率加权(%)',
  `net_yoy` decimal(16,2) DEFAULT NULL COMMENT '净利润同比',
  `por_yoy` decimal(16,2) DEFAULT NULL COMMENT '主营业务收入同比',
  `pop_yoy` decimal(16,2) DEFAULT NULL COMMENT '主营业务利润同比',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code_date` (`code`,`date`),
  KEY `idx_code` (`code`),
  KEY `idx_name` (`name`),
  KEY `idx_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
