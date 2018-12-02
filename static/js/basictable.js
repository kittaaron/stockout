var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        ranking_pe_list: [],
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_ranking_pe_list();
    },
    methods: {
        get_ranking_pe_list: function() {
            var that = this;
            $.ajax({
                type: "GET",
                url: "/get_ranking_pe",
                dataType: "json",
                async: false,
                success: function(data) {
                    var list_data = data.data;
                    that.ranking_pe_list = list_data;
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        }
    }
})