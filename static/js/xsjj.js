var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        xsjj_list: [],
        cur: 1,
        all: 100,
        page_size: 200,
        month_from: 1,
        month_to: 1,
        month_froms: [{'val': 1, 'desc': '前1个月'},{'val': 2, 'desc': '前2个月'},{'val': 3, 'desc': '前3个月'},{'val': 6, 'desc': '前6个月'}],
        month_tos: [{'val': 1, 'desc': '后1个月'},{'val': 2, 'desc': '后2个月'},{'val': 3, 'desc': '后3个月'},{'val': 6, 'desc': '后6个月'},{'val': 12, 'desc': '后12个月'}]
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_xsjj_list();
    },
    components: {
        // 引用组件
        'vue-pagination': Vue.Pagination
    },
    methods: {
        get_xsjj_list: function() {
            var that = this;
            var params = {'page_size': that.page_size, 'page': that.cur - 1, 'month_from': that.month_from, 'month_to': that.month_to};
            $.ajax({
                type: "GET",
                data: params,
                url: "/get_xsjj_list",
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    that.all = data.total_page;
                    that.xsjj_list = list_data;
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },
        to_detail: function(code) {
            detail_page = "detail.html#/?code=" + code;
            window.open(detail_page, '_blank');
        },
        search: function() {
        },
        listen: function (data) {
            console.log("当前页: ", data);
            this.cur = data;
            this.get_xsjj_list();
        }
    }
})