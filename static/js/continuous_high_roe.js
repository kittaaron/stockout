var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        result_list: [],
        continuous_year: 4,
        roe_threshold: 15,
        total_cnt: 0,
        continuous_years: [{'val': 4, 'desc': '4'},{'val': 3, 'desc': '3'}],
        roe_thresholds: [{'val': 10, 'desc': '10'},{'val': 15, 'desc': '15'},{'val': 20, 'desc': '20'}],
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_data_list();
    },
    components: {
        // 引用组件
    },
    methods: {
        get_data_list: function() {
            var that = this;
            var params = {"continuous_years": that.continuous_year, "roe_threshold": that.roe_threshold};
            $.ajax({
                type: "GET",
                data: params,
                url: "../../../get_continuous_high_roe",
                dataType: "json",
                async: false,
                success: function(data) {
                    var result_list = data.data
                    that.result_list = result_list
                    that.total_cnt = result_list.length
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        }
    }
})