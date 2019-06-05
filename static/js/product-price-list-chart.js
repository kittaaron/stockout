(function($) {
  'use strict';

  var get_product_price_hist = function() {
     $.ajax({
         type: "GET",
         url: "../../../get_product_price_list",
         //data: {username:$("#username").val(), content:$("#content").val()},
         dataType: "json",
         success: function(data) {
            var grouped_datas = data.data
            var legend_arr = []
            var xAxis_data = []
            var price_list_map = {}


            var series = []

            var xAxis_data_fulled = false
            for(var k in grouped_datas){
                var price_list = grouped_datas[k]
                // 叶酸
                if (k.indexOf('_') == -1) {
                    renderXXPriceChart(k, price_list, k.toLowerCase()+'_price_chart', k, [k])
                } else {
                    var prefix = k.substr(0, k.indexOf('_'))
                    renderXXPriceChart(prefix, price_list, prefix.toLowerCase()+'_price_chart', prefix, [prefix])
                }
                legend_arr.push(k)
                price_list_map[k] = []
                // 后端返回的数据结构，需要处理成只有价格的列表
                var backend_price_list = grouped_datas[k]
                for (var e in price_list) {
                    if (!xAxis_data_fulled) {
                        xAxis_data.push(price_list[e].date)
                    }
                    price_list_map[k].push(price_list[e].price)
                }

                var series_i = {
                    name: k,
                    type:'line',
                    stack: k,
                    data:price_list_map[k]
                }
                series.push(series_i)
                xAxis_data_fulled = true
            }

            renderPriceChart(legend_arr, xAxis_data, series)
         },
         error: function(data) {
            alert("获取数据失败");
         }

     });
  }

  var renderPriceChart = function(legend_arr, xAxis_data, series) {
    var myChart = echarts.init(document.getElementById('product_price_chart'));
        if (!xAxis_data) {
            alert("获取数据失败.")
            return;
        }

        // 线图
        var option = {
            title: {
                text: ''
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: legend_arr
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
            series: series
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
  }

  var renderXXPriceChart = function(xx, pricedatas, dom_id, title, legend_data) {
    var xAxis_data = []
    var prices = []
    for (var i in pricedatas) {
        var obj = pricedatas[i]
        xAxis_data.push(obj.date)
        prices.push(obj.price)
    }
    var series = [
        {
            name:xx,
            type:'line',
            stack: '平均',
            data:prices
        }
    ]

    renderChart(dom_id, title, legend_data, xAxis_data, series)
  }

  var renderChart  = function(dom_id, title, legend_data, xAxis_data, series) {
    var dom_obj = document.getElementById(dom_id)
    if (!dom_obj) {
        console.log(dom_id + '对象不存在')
        return
    }
    var myChart = echarts.init(dom_obj);

        // 线图
        var option = {
            title: {
                text: title
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: legend_data
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
            series: series
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
  }

  $(function() {
        get_product_price_hist();
  });
})(jQuery);