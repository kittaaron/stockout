var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        ranking_pb_list: [],
        sortFields:
            [
                {'desc': '按PB排序', 'val': 'pb'},
                {'desc': '按负债率排序', 'val': 'liab_ratio'},
                {'desc': '按非流动负债率排序', 'val': 'non_current_liab_ratio'}
            ],
        sort_by: 'pb',
        cur: 1,
        all: 100,
        page_size: 200,
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_ranking_pb_list();
    },
    methods: {
        get_ranking_pb_list: function() {
            var that = this;
            console.log(that.sort_by);
            var params = {
                'page_size': that.page_size,
                'page': that.cur - 1,
                'sort_by': that.sort_by
            };
            $.ajax({
                type: "GET",
                url: "../../../get_ranking_pb",
                data: params,
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    that.all = data.total_page;
                    that.ranking_pb_list = list_data;
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },
        changeSort: function() {
            this.get_ranking_pb_list();
        },
        listen: function (data) {
            console.log("当前页: ", data);
            this.cur = data;
            this.get_ranking_pb_list();
        }
    }
})