(function($) {
  'use strict';

  var get_steel_price_hist = function() {
     $.ajax({
         type: "GET",
         url: "/get_steel_price_hist",
         //data: {username:$("#username").val(), content:$("#content").val()},
         dataType: "json",
         success: function(data) {
            var list_data = data.data
            var xAxis_data = []
            var priceHist_data = [];
            $.each(list_data, function(index, value) {
                xAxis_data.push(value.date)
                priceHist_data.push(value.price)
            });
            renderSteelPriceChart(xAxis_data, priceHist_data)
         },
         error: function(data) {
            alert("获取数据失败");
         }

     });
  }

  var renderSteelPriceChart = function(xAxis_data, priceHist_data) {
    var myChart = echarts.init(document.getElementById('steel_price_chart'));
        if (!xAxis_data) {
            alert("获取数据失败.")
            return;
        }

        // 线图
        var option = {
            title: {
                text: '杭州市场价格：螺纹钢：HRB400E(元/吨)'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['钢铁价格(元/吨)']
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
                    name:'钢铁价格',
                    type:'line',
                    stack: '平均',
                    data:priceHist_data
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
  }

  $(function() {
        get_steel_price_hist();
  });
})(jQuery);