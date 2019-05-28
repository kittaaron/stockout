(function($) {
  'use strict';

  var get_sh_market_data = function() {
     $.ajax({
         type: "GET",
         url: "../get_market_data/sh",
         //data: {username:$("#username").val(), content:$("#content").val()},
         dataType: "json",
         success: function(data) {
            var list_data = data.data
            var xAxis_data = []
            var profitRate_data = [];
            var trdAmt_data = [];
            var exchangeRate_data = [];
            var marketValue_data = [];
            $.each(list_data, function(index, value) {
                xAxis_data.push(value.date)
                profitRate_data.push(value.profitRate)
                trdAmt_data.push(value.trdAmt)
                exchangeRate_data.push(value.exchangeRate)
                marketValue_data.push(value.marketValue)
            });
            var pe_lt_cnt = 0;
            var latest_pe = profitRate_data[profitRate_data.length - 1];
            $.each(profitRate_data, function(index, value){
                if (value <= latest_pe) {
                    pe_lt_cnt+=1;
                }
            })
            var hist_pos = (pe_lt_cnt * 100 / profitRate_data.length).toFixed(2)
            renderShMarketChart(xAxis_data, profitRate_data, trdAmt_data, exchangeRate_data, marketValue_data, hist_pos)
         },
         error: function(data) {
            alert("获取数据失败");
         }

     });
  }

  var renderShMarketChart = function(xAxis_data, profitRate_data, trdAmt_data, exchangeRate_data, marketValue_data, hist_pos) {
    var myChart = echarts.init(document.getElementById('sh_market_data_chart'));
        if (!xAxis_data) {
            alert("获取数据失败.")
            return;
        }

        // 线图
        var option = {
            title: {
                text: '上证大盘指标历史图\n\r(历史分位' + hist_pos + ')'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['市盈率','成交金额(亿元)','换手率','市值(亿)']
            },
            xAxis: {
                type: 'category',
                interval: 10,
                data: xAxis_data
            },
            dataZoom:[
                {
                    xAxisIndex: [0]
                },
            ],
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name:'市盈率',
                    type:'line',
                    stack: '平均',
                    data:profitRate_data
                },
                {
                    name:'成交金额(亿元)',
                    type:'line',
                    stack: '总量',
                    data:trdAmt_data
                },
                {
                    name:'换手率',
                    type:'line',
                    stack: '平均',
                    data:exchangeRate_data
                },
                {
                    name:'市值(亿)',
                    type:'line',
                    stack: '总量',
                    data:marketValue_data
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
  }

  var get_sz_market_data = function() {
     $.ajax({
         type: "GET",
         url: "../get_market_data/sz",
         //data: {username:$("#username").val(), content:$("#content").val()},
         dataType: "json",
         success: function(data) {
            var list_data = data.data
            var xAxis_data = []
            var profitRate_data = [];
            var trdAmt_data = [];
            var exchangeRate_data = [];
            var marketValue_data = [];
            $.each(list_data, function(index, value) {
                if ($.inArray(value.date, xAxis_data) < 0) {
                    xAxis_data.push(value.date);
                }
                if (value.zbtype == 14) {
                    profitRate_data.push(value.brsz)
                } else if (value.zbtype == 7) {
                    trdAmt_data.push(value.brsz)
                } else if (value.zbtype == 15) {
                    exchangeRate_data.push(value.brsz)
                } else if (value.zbtype == 10) {
                    marketValue_data.push(value.brsz)
                }
            });
            var pe_lt_cnt = 0;
            var latest_pe = profitRate_data[profitRate_data.length - 1];
            $.each(profitRate_data, function(index, value){
                if (value <= latest_pe) {
                    pe_lt_cnt+=1;
                }
            })
            var hist_pos = (pe_lt_cnt * 100 / profitRate_data.length).toFixed(2)
            renderSZMarketChart(xAxis_data, profitRate_data, trdAmt_data, exchangeRate_data, marketValue_data,hist_pos)
         },
         error: function(data) {
            alert("获取数据失败");
         }

     });
  }

  var renderSZMarketChart = function(xAxis_data, profitRate_data, trdAmt_data, exchangeRate_data, marketValue_data,hist_pos) {
    var myChart = echarts.init(document.getElementById('sz_market_data_chart'));
        if (!xAxis_data) {
            alert("获取数据失败.")
            return;
        }

        // 线图
        var option = {
            title: {
                text: '深证大盘指标历史图\n\r(历史分位' + hist_pos + ')'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['市盈率','成交金额(亿元)','换手率','市值(亿)']
            },
            xAxis: {
                type: 'category',
                interval: 10,
                data: xAxis_data
            },
            dataZoom:[
                {
                    xAxisIndex: [0]
                },
            ],
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name:'市盈率',
                    type:'line',
                    stack: '平均',
                    data:profitRate_data
                },
                {
                    name:'成交金额(亿元)',
                    type:'line',
                    stack: '总量',
                    data:trdAmt_data
                },
                {
                    name:'换手率',
                    type:'line',
                    stack: '平均',
                    data:exchangeRate_data
                },
                {
                    name:'市值(亿)',
                    type:'line',
                    stack: '总量',
                    data:marketValue_data
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
  }

  $(function() {
        get_sh_market_data();
        get_sz_market_data();
  });
})(jQuery);