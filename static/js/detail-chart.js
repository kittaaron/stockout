const router = new VueRouter({
  routes: [
    { path: '/detail-chart.html:code' }
  ]
})

var vm = new Vue({
  // 选项
    el: '#content',
    router,
    data: {
        code: null,
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.code = this.$route.query.code
    },
    methods: {
        get_price_list: function() {
            var that = this;
            $.ajax({
                type: "GET",
                data: {"code": that.code},
                url: "/get_price_list",
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    alert(list_data.length);
                    xAxis_data = []
                    price_data = []
                    list_data.forEach(v=>{
                        xAxis_data.push(v.date);
                        price_data.push(v.close);
                    });
                    that.render_chart(xAxis_data, price_data);
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },

        render_chart: function(xAxis_data, price_data) {
            var myChart = echarts.init(document.getElementById('price_chart'));
            if (!xAxis_data) {
                alert("获取数据失败.")
                return;
            }

            // 线图
            var option = {
                title: {
                    text: '历史价格图标'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data:['价格']
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
                        name:'价格',
                        type:'line',
                        stack: '平均',
                        data:price_data
                    }
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    }
})