const router = new VueRouter({
  routes: [
    { path: '/detail.html:code' }
  ]
})

var vm = new Vue({
  // 选项
    el: '#content',
    router,
    data: {
        report_list: [],
        code: null,
        stockname: null
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.code = this.$route.query.code
        this.get_report_list();
    },
    methods: {
        get_report_list: function() {
            var that = this;
            $.ajax({
                type: "GET",
                data: {"code": that.code},
                url: "/get_report_list",
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    if (!!list_data && !!list_data[0].name) {
                        that.stockname = list_data[0].name
                    }
                    that.report_list = list_data;
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        }
    }
})