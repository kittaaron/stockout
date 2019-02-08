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
        this.code = this.$route.query.code;
        report_list = [];
        this.get_price_list();
        this.get_report_chart_list();
    },
    methods: {
        get_report_chart_list: function() {
            var that = this;
            $.ajax({
                type: "GET",
                data: {"code": that.code},
                url: "/get_report_list",
                dataType: "json",
                async: false,
                success: function(data) {
                    that.report_list = data.data;
                    var xAxis_data = [];
                    var por_data = [];
                    var net_profit_data = [];
                    var npad_data = [];
                    var net_yoy_data = [];
                    var por_yoy_data = [];
                    var report_length = that.report_list.length;
                    for (i = report_length -1; i >= 0; i--) {
                        var v = that.report_list[i];
                        xAxis_data.push(v.date);
                        por_data.push(v.por);
                        net_profit_data.push(v.net_profit);
                        npad_data.push(v.npad);
                        net_yoy_data.push(v.net_yoy * 100 - 100);
                        por_yoy_data.push(v.por_yoy * 100 - 100);
                    }
                    that.render_report_chart(xAxis_data, por_data, net_profit_data, npad_data);
                    that.render_yoy_chart(xAxis_data, net_yoy_data, por_yoy_data);
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },
        get_price_list: function() {
            var that = this;
            $.ajax({
                type: "GET",
                data: {},
                url: "/get_price_list/" + that.code,
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    xAxis_data = []
                    price_data = []
                    static_pe8 = []
                    static_pe12 = []
                    static_pe16 = []
                    static_pe20 = []
                    dynamic_pe8 = []
                    dynamic_pe12 = []
                    dynamic_pe16 = []
                    dynamic_pe20 = []
                    list_data.forEach(v=>{
                        xAxis_data.push(v.date);
                        price_data.push(v.close);
                        static_pe8.push(v.static_pe8);
                        static_pe12.push(v.static_pe12);
                        static_pe16.push(v.static_pe16);
                        static_pe20.push(v.static_pe20);
                        dynamic_pe8.push(v.dynamic_pe8);
                        dynamic_pe12.push(v.dynamic_pe12);
                        dynamic_pe16.push(v.dynamic_pe16);
                        dynamic_pe20.push(v.dynamic_pe20);
                    });
                    that.render_price_chart(xAxis_data, price_data, static_pe8, static_pe12, static_pe12, static_pe16, dynamic_pe8, dynamic_pe12, dynamic_pe16, dynamic_pe20);
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },

        render_price_chart: function(xAxis_data, price_data, static_pe8, static_pe12, static_pe12, static_pe16, dynamic_pe8, dynamic_pe12, dynamic_pe16, dynamic_pe20) {
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
                    data:['价格', '静态8pe', '静态12pe', '静态16pe', '静态20pe', '动态8pe', '动态12pe', '动态16pe', '动态20pe'],
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
                yAxisIndex: 1,
                series: [
                    {
                        name:'价格',
                        type:'line',
                        stack: '平均',
                        data:price_data
                    },
                    {
                        name:'静态8pe',
                        type:'line',
                        stack: '静态8pe',
                        data:static_pe8
                    },
                    {
                        name:'静态12pe',
                        type:'line',
                        stack: '静态12pe',
                        data:static_pe12
                    },
                    {
                        name:'静态16pe',
                        type:'line',
                        stack: '静态16pe',
                        data:static_pe16
                    },
                    {
                        name:'静态20pe',
                        type:'line',
                        stack: '静态20pe',
                        data:static_pe20
                    },
                    {
                        name:'动态8pe',
                        type:'line',
                        stack: '动态8pe',
                        data:dynamic_pe8
                    },
                    {
                        name:'动态12pe',
                        type:'line',
                        stack: '动态12pe',
                        data:dynamic_pe12
                    },
                    {
                        name:'动态16pe',
                        type:'line',
                        stack: '动态16pe',
                        data:dynamic_pe16
                    },
                    {
                        name:'动态20pe',
                        type:'line',
                        stack: '动态20pe',
                        data:dynamic_pe20
                    }
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },

        render_report_chart: function(xAxis_data, por_data, net_profit_data, npad_data) {
            var myChart = echarts.init(document.getElementById('report_chart'));
            if (!xAxis_data) {
                alert("获取报表数据失败.")
                return;
            }

            // 线图
            var option = {
                title: {
                    text: '报表图标'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data:['主营收入', '净利润', '扣非净利润']
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
                yAxis: [
                    {
                        name: '万元',
                        type: 'value'
                    },
                    {
                        name: '万元',
                        type: 'value'
                    }
                ],
                yAxisIndex: 1,
                series: [
                    {
                        name:'主营收入',
                        type:'line',
                        stack: '主营收入',
                        data: por_data,
                        yAxisIndex: 0,
                    },
                    {
                        name:'净利润',
                        type:'line',
                        stack: '净利润',
                        data: net_profit_data,
                        yAxisIndex: 1,
                    },
                    {
                        name:'扣非净利润',
                        type:'line',
                        stack: '扣非净利润',
                        data: npad_data,
                        yAxisIndex: 1,
                    }
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },


        render_yoy_chart: function(xAxis_data, net_yoy_data, por_yoy_data) {
            var myChart = echarts.init(document.getElementById('yoy_chart'));
            if (!xAxis_data) {
                alert("获取报表数据失败.")
                return;
            }

            // 线图
            var option = {
                title: {
                    text: '报表图标'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data:['净利润同比', '主营收入同比']
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
                yAxis: [
                    {
                        name: '百分比',
                        type: 'value'
                    }
                ],
                yAxisIndex: 1,
                series: [
                    {
                        name:'净利润同比',
                        type:'line',
                        stack: '净利润同比',
                        data: net_yoy_data,
                        yAxisIndex: 0,
                    },
                    {
                        name:'主营收入同比',
                        type:'line',
                        stack: '主营收入同比',
                        data: por_yoy_data,
                        yAxisIndex: 0,
                    }
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    }
})