CREATE TABLE `stockinfo` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(64) NOT NULL DEFAULT '' COMMENT '股票名称',
  `industry` varchar(64) NOT NULL DEFAULT '' COMMENT '股票行业',
  `industry_classified` varchar(64) NOT NULL DEFAULT '' COMMENT '行业名称',
  `concept_classified` varchar(64) NOT NULL DEFAULT '' COMMENT '概念名称',
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`),
  KEY `idx_industry_classified` (`industry_classified`),
  KEY `idx_concept_classified` (`concept_classified`)
) ENGINE=InnoDB AUTO_INCREMENT=4744 DEFAULT CHARSET=utf8;

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
  `net_profit_ratio` decimal(16,2) NOT NULL COMMENT '净利率(%)',
  `gross_profit_rate` decimal(16,4) NOT NULL COMMENT '毛利率(%)',
  `business_income` decimal(16,4) NOT NULL COMMENT '营业收入(百万元)',
  `bips` decimal(16,4) NOT NULL COMMENT '每股主营业务收入(元)',
  `arturnover` decimal(16,4) NOT NULL COMMENT '应收账款周转率(次)',
  `arturndays` decimal(16,4) NOT NULL COMMENT '应收账款周转天数(天)',
  `inventory_turnover` decimal(16,4) NOT NULL COMMENT '存货周转率(次)',
  `inventory_days` decimal(16,4) NOT NULL COMMENT '存货周转天数(天)',
  `currentasset_turnover` decimal(16,4) NOT NULL COMMENT '流动资产周转率(次)',
  `currentasset_days` decimal(16,4) NOT NULL COMMENT '流动资产周转天数(天)',
  `mbrg` decimal(16,4) NOT NULL COMMENT '主营业务收入增长率(%)',
  `nprg` decimal(16,4) NOT NULL COMMENT '净利润增长率(%)',
  `nav` decimal(16,4) NOT NULL COMMENT '净资产增长率',
  `targ` decimal(16,4) NOT NULL COMMENT '总资产增长率',
  `epsg` decimal(16,4) NOT NULL COMMENT '每股收益增长率',
  `seg` decimal(16,4) NOT NULL COMMENT '股东权益增长率',
  `currentratio` decimal(16,4) NOT NULL COMMENT '流动比率',
  `quickratio` decimal(16,4) NOT NULL COMMENT '速动比率',
  `cashratio` decimal(16,4) NOT NULL COMMENT '现金比率',
  `icratio` decimal(16,4) NOT NULL COMMENT '利息支付倍数',
  `sheqratio` decimal(16,4) NOT NULL COMMENT '股东权益比率',
  `adratio` decimal(16,4) NOT NULL COMMENT '股东权益增长率',
  `cf_sales` decimal(16,4) NOT NULL COMMENT '经营现金净流量对销售收入比率',
  `rateofreturn` decimal(16,4) NOT NULL COMMENT '资产的经营现金流量回报率',
  `cf_nm` decimal(16,4) NOT NULL COMMENT '经营现金净流量与净利润的比率',
  `cf_liabilities` decimal(16,4) NOT NULL COMMENT '经营现金净流量对负债比率',
  `cashflowratio` decimal(16,4) NOT NULL COMMENT '现金流量比率',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3454 DEFAULT CHARSET=utf8;

CREATE TABLE `index_data` (
  `index` bigint(20) DEFAULT NULL,
  `code` text COMMENT '指数代码',
  `name` text COMMENT '指数名称',
  `change` double DEFAULT NULL COMMENT '涨跌幅',
  `open` double DEFAULT NULL COMMENT '开盘点位',
  `preclose` double DEFAULT NULL COMMENT '昨日收盘点位',
  `close` double DEFAULT NULL COMMENT '收盘点位',
  `high` double DEFAULT NULL COMMENT '最高点位',
  `low` double DEFAULT NULL COMMENT '最低点位',
  `volume` bigint(20) DEFAULT NULL COMMENT '成交量(手)',
  `amount` double DEFAULT NULL COMMENT '成交金额（亿元）',
  KEY `ix_index_data_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `stockweight` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(10) NOT NULL DEFAULT '' COMMENT '名称',
  `date` varchar(64) NOT NULL DEFAULT '' COMMENT '日期',
  `weight` decimal(16,2) NOT NULL COMMENT '权重',
  PRIMARY KEY (`id`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `today_data` (
  `index` bigint(20) DEFAULT NULL,
  `code` text COMMENT '',
  `name` text COMMENT '',
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

CREATE TABLE `rzrq_total` (
  `rzmre` bigint(20) DEFAULT NULL COMMENT '融资买入额',
  `rzye` bigint(20) DEFAULT NULL COMMENT '融资余额',
  `rqmcl` bigint(20) DEFAULT NULL COMMENT '融券卖出额',
  `rqyl` bigint(20) DEFAULT NULL COMMENT '融券余量',
  `rqye` bigint(20) DEFAULT NULL COMMENT '融券余量(元)',
  `rzrqye` bigint(20) DEFAULT NULL COMMENT '融资融券余额(元)',
  `opDate` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '融资融券汇总';

CREATE TABLE `fpya` (
  `code` text,
  `name` text,
  `year` bigint(20) DEFAULT NULL,
  `report_date` text,
  `divi` double DEFAULT NULL COMMENT '分红金额（每10股）',
  `shares` double DEFAULT NULL  COMMENT '转增和送股数（每10股）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '分配预案';

CREATE TABLE `yjyg` (
  `code` text,
  `name` text,
  `type` text COMMENT '业绩变动类型【预增、预亏等】',
  `report_date` text COMMENT '发布日期',
  `pre_eps` double DEFAULT NULL COMMENT '上年同期每股收益',
  `range` text COMMENT '业绩变动范围'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '业绩预告';

CREATE TABLE `xsjj` (
  `code` text,
  `name` text,
  `date` text COMMENT '解禁日期',
  `count` text COMMENT '解禁数量（万股）',
  `ratio` text COMMENT '占总盘比率'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '限售解禁';

CREATE TABLE `jjcg` (
  `code` text,
  `name` text,
  `date` text,
  `nums` text COMMENT '基金家数',
  `nlast` text COMMENT '与上期相比（增加或减少了）',
  `count` text COMMENT '基金持股数（万股）',
  `clast` text COMMENT '与上期相比',
  `amount` text COMMENT '基金持股市值',
  `ratio` text COMMENT '占流通盘比率'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '基金持股';

CREATE TABLE `new_stocks` (
  `code` text,
  `xcode` text,
  `name` text,
  `ipo_date` text COMMENT '上网发行日期',
  `issue_date` text COMMENT '上市日期',
  `amount` bigint(20) DEFAULT NULL COMMENT '发行数量(万股)',
  `markets` bigint(20) DEFAULT NULL COMMENT '上网发行数量(万股)',
  `price` double DEFAULT NULL COMMENT '发行价格(元)',
  `pe` double DEFAULT NULL COMMENT '发行市盈率',
  `limit` double DEFAULT NULL COMMENT '个人申购上限(万股)',
  `funds` double DEFAULT NULL COMMENT '募集资金(亿元)',
  `ballot` double DEFAULT NULL COMMENT '网上中签率(%)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '新股';

CREATE TABLE `lhb` (
  `code` text,
  `name` text,
  `pchange` text COMMENT '当日涨跌幅',
  `amount` text COMMENT '龙虎榜成交额(万)',
  `buy` text COMMENT '买入额(万)',
  `sell` text COMMENT '卖出额(万)',
  `reason` text COMMENT '上榜原因',
  `bratio` text COMMENT '买入占总成交比例',
  `sratio` text COMMENT '卖出占总成交比例',
  `date` text COMMENT '日期'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '龙虎榜';

CREATE TABLE `cap_tops` (
  `code` text,
  `name` text,
  `count` bigint(20) DEFAULT NULL COMMENT '上榜次数(默认5日内)',
  `bamount` double DEFAULT NULL COMMENT '累积购买额(万)',
  `samount` double DEFAULT NULL COMMENT '累积卖出额(万)',
  `net` double DEFAULT NULL COMMENT '净额(万)',
  `bcount` bigint(20) DEFAULT NULL COMMENT '买入席位数',
  `scount` bigint(20) DEFAULT NULL COMMENT '卖出席位数'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '个股上榜统计数据 获取近5、10、30、60日个股上榜统计数据';

CREATE TABLE `broker_tops` (
  `broker` text,
  `count` bigint(20) DEFAULT NULL COMMENT '上榜次数',
  `bamount` double DEFAULT NULL COMMENT '累积购买额(万)',
  `bcount` bigint(20) DEFAULT NULL COMMENT '买入席位数',
  `samount` double DEFAULT NULL COMMENT '累积卖出额(万)',
  `scount` bigint(20) DEFAULT NULL COMMENT '卖出席位数',
  `top3` text COMMENT '买入前三股票'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '获取营业部近5、10、30、60日上榜次数、累积买卖等情况';

CREATE TABLE `inst_tops` (
  `code` text,
  `name` text,
  `bamount` double DEFAULT NULL COMMENT '累积买入额(万)',
  `bcount` bigint(20) DEFAULT NULL COMMENT '买入次数',
  `samount` double DEFAULT NULL COMMENT '累积卖出额(万)',
  `scount` bigint(20) DEFAULT NULL COMMENT '卖出次数',
  `net` double DEFAULT NULL COMMENT '净额(万)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '机构席位追踪: 获取机构近5、10、30、60日累积买卖次数和金额等情况';

CREATE TABLE `inst_detail` (
  `code` text,
  `name` text,
  `date` text COMMENT '交易日期',
  `bamount` double DEFAULT NULL COMMENT '机构席位买入额(万)',
  `samount` double DEFAULT NULL COMMENT '机构席位卖出额(万)',
  `type` text COMMENT '类型'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(16) DEFAULT '',
  `name` varchar(16) DEFAULT '' COMMENT '',
  `date` varchar(4) DEFAULT '' COMMENT '日期',
  `time` varchar(12) DEFAULT '' COMMENT '交易时间. 例:14:58:10',
  `price` double DEFAULT NULL COMMENT '当前价格',
  `volume` bigint(20) DEFAULT NULL COMMENT '成交手',
  `preprice` double DEFAULT NULL COMMENT '上一笔价格',
  `type` varchar(4) DEFAULT '' COMMENT '买卖类型【买盘、卖盘、中性盘】',
  PRIMARY KEY (`id`),
  KEY `idx_code_date` (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '大单交易数据明细';

CREATE TABLE `dd_sts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(16) DEFAULT '',
  `name` varchar(16) DEFAULT '' COMMENT '',
  `date` varchar(4) DEFAULT '' COMMENT '日期',
  `b_volume` bigint(20) DEFAULT NULL COMMENT '买盘总成交手',
  `s_volume` bigint(20) DEFAULT NULL COMMENT '卖盘总成交手',
  `net` bigint(20) DEFAULT NULL COMMENT '总净值(b_volume - s_volume)',
  `lhh_b_volume` bigint(20) DEFAULT NULL COMMENT 'last_half_hour最后半小时买盘总成交手',
  `lhh_s_volume` bigint(20) DEFAULT NULL COMMENT '最后半小时卖盘总成交手',
  `lhh_net` bigint(20) DEFAULT NULL COMMENT '最后半小时总净值(b_volume - s_volume)',
  PRIMARY KEY (`id`),
  KEY `idx_code_date` (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '大单交易数据统计';

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
  UNIQUE KEY `idx_code_date` (`code`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=698 DEFAULT CHARSET=utf8 COMMENT '历史数据';