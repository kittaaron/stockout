var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        ranking_pe_list: [],
        cur: 1,
        all: 100,
        page_size: 200,
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_ranking_pe_list();
    },
    components: {
        // 引用组件
        'vue-pagination': Vue.Pagination
    },
    methods: {
        get_ranking_pe_list: function(currpage) {
            var that = this;
            $.ajax({
                type: "GET",
                data: {'page_size': that.page_size, 'page': that.cur - 1},
                url: "/get_ranking_pe",
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    that.all = data.total_page;
                    that.ranking_pe_list = list_data;
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },
        listen: function (data) {
            console.log("当前页: ", data);
            this.cur = data;
            this.get_ranking_pe_list();
        }
    }
})