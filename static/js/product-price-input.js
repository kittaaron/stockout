var vm = new Vue({
  // 选项
    el: '#content',
    data: {
        category0List: [],
        category1List: [],
        selCategory0: '',
        batchSelCategory0: '',
        selCategory1: '',
        date: '',
        price: 0,
        batch_disable: false,
        batchSelDate: ''
    },
    // 页面加载完执行，用vue的create或者mounted函数
    mounted: function() {
        this.get_category0_def_list();
    },
    components: {
        // 引用组件
        //'vue-pagination': Vue.Pagination
    },
    methods: {
        get_category0_def_list: function() {
            var that = this;
            $.ajax({
                type: "GET",
                data: {},
                url: "../../../get_category0_def_list",
                dataType: "json",
                async: false,
                success: function(data) {
                    that.category0List = data.data;
                    //that.selVal = that.category0List[0].id
                    if (!that.category0List) {
                        return;
                    }
                    var c0_id = that.category0List[0].id
                    that.selCategory0 = c0_id
                    that.get_category1_def_list(c0_id)
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },
        get_category1_def_list: function(c0_id) {
            var that = this;
            var url = "../../../get_category1_def_list/" + c0_id
            $.ajax({
                type: "GET",
                data: {},
                url: url,
                dataType: "json",
                async: false,
                success: function(data) {
                    that.category1List = data.data;
                    if (!that.category1List) {
                        return;
                    }
                    var c1_id = that.category1List[0].id
                    that.selCategory1 = c1_id
                },
                error: function(data) {
                    alert("获取数据失败");
                }
            });
        },
        add_price: function() {
            param = {
                c0: this.selCategory0,
                c1: this.selCategory1,
                date: this.date,
                price: this.price
            }
            $.ajax({
                type: "POST",
                data: param,
                url: "../../../save_product_price",
                dataType: "json",
                async: false,
                success: function(data) {
                    if (data.code == 0) {
                        alert("保存成功")
                    }
                    console.log(data)
                },
                error: function(data) {
                    alert("保存失败");
                }
            });
        },
        listen: function (data) {
            //
        },
        onSubmit: function() {
            console.log("c0: %s, c1:%s, date:%s, price:%s", this.selCategory0, this.selCategory1, this.date, this.price)
            this.add_price();
        },
        onBatchSubmit: function() {
            //alert("batchSubmit");
            var nameList = []
            var valList = []
            for (var i = 0; i < this.category1List.length; i++) {
                nameList.push(this.category1List[i].name)
                var valI = $("input[name='vet_" + i + "']").val()
                valList.push(valI)
            }
            var joinedNames = nameList.join(",")
            var joinedPrices = valList.join(",")

            param = {
                c0: this.batchSelCategory0,
                joinedNames: joinedNames,
                date: this.batchSelDate,
                joinedPrices: joinedPrices
            }
            $.ajax({
                type: "POST",
                data: param,
                url: "../../../batch_save_product_price",
                dataType: "json",
                async: false,
                success: function(data) {
                    if (data.code == 0) {
                        alert("保存成功")
                    }
                    console.log(data)
                },
                error: function(data) {
                    alert("保存失败");
                }
            });
        },
        c0change: function(e) {
            //this.selVal = this.category0List[e.target.selectedIndex].id
        },
        batchc0change: function(e) {
        },
        setName: function(i) {
            return "vet_" + i
        },
        switchInput: function(e) {
            this.batch_disable = !this.batch_disable
        }
    }
})