var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        sorted_fhsgs: [],
        cur: 1,
        all: 1000,
        page_size: 1000,
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_sorted_fhsg();
    },
    components: {
        // 引用组件
        'vue-pagination': Vue.Pagination
    },
    methods: {
        get_sorted_fhsg: function() {
            var that = this;
            date_str = '20181231'
            var params = {'page_size': that.page_size, 'page': that.cur - 1, 'date_str': date_str};
            $.ajax({
                type: "GET",
                data: params,
                url: "../../../get_sorted_fhrate",
                dataType: "json",
                async: false,
                success: function(data) {
                    var sorted_fhsgs = data.data;
                    that.sorted_fhsgs = sorted_fhsgs
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },
        listen: function (data) {
            console.log("当前页: ", data);
            this.cur = data;
            this.get_xsjj_list();
        }
    }
})