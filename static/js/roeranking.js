var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        ranking_pe_list: [],
        ranking_wroe_list: [],
        cur: 1,
        all: 100,
        page_size: 500,
        searchCode: null,
        market_time_in: null,
        in_years: [{'val': null, 'desc': '不限'},{'val': 1, 'desc': '1年内'},{'val': 3, 'desc': '3年内'},{'val': 5, 'desc': '5年内'}]
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_ranking_wroe_list();
    },
    components: {
        // 引用组件
        'vue-pagination': Vue.Pagination
    },
    methods: {
        get_ranking_wroe_list: function() {
            var that = this;
            var params = {'page_size': that.page_size, 'page': that.cur - 1};
            if (!!that.searchCode) {
                params.code = that.searchCode;
            }
            if (!!that.market_time_in) {
                params.market_time_in = that.market_time_in;
            }
            $.ajax({
                type: "GET",
                data: params,
                url: "../../../get_ranking_wroe",
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    that.all = data.total_page;
                    that.ranking_wroe_list = list_data;
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
        select_market_time_in: function(select_market_time_in) {

        },
        search: function() {
            var searchCode = this.searchCode;
        },
        listen: function (data) {
            console.log("当前页: ", data);
            this.cur = data;
            this.get_ranking_wroe_list();
        }
    }
})