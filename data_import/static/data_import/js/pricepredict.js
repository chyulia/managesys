function drawHistoryPriceBrokenLineChart(data){
        var myChart = echarts.init(document.getElementById('history_figure'));
        var line_mark = data.timeline[1];
        console.log(line_mark);
        option = {
            title: {
                text: '钢材价格走势折线图',
                x: 'center',
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['特钢价格历史走势'],
                x: 'right',
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data.timeline,
            },
            yAxis: {
                type: 'value',
                axisLabel : {
                    formatter: '¥{value} '
                },
                splitLine: {
                    show: true
                }
            },
            series: [
                {
                    name:'特钢价格历史走势',
                    type:'line',
                    stack: '总量',
                    data: data.price,
                    markLine : {
                        lineStyle: {
                            normal: {
                                type: 'solid'
                            }
                        },
                        data : [
                            {type : 'average', name: '平均值'},
                            [
                                {coord: ['2016-05-1', 3000]},{coord: ['2016-05-31', 3000]}
                            ]
                        ]
                    },
                },
            ],
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }
function drawPredictBrokenLineChart(data, figure_name, method){
    if(figure_name != "predict_figure"){
        figure_name = method;
    }

    var pridict_result_json = {
        "RandomForest":"随机森林",
        "ExtremeLM":"超限学习机elm",
        "SVR_":"支持向量回归svr",
    }
    var myChart = echarts.init(document.getElementById(figure_name));
    option = {
        title: {
            text: pridict_result_json[method] + '预测图',
//            subtext: '评分：'+data.score,
            x: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['真实值','预测值'],
            x: 'right'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.timeline
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'真实值',
                type:'line',
                stack: '总量',
                data:[]
            },
            {
                name:'预测值',
                type:'line',
                stack: '总量',
                data:[]
            },
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    if (option && typeof option === "object") {
//        var startTime = +new Date();
//        var true_his = data.true_value.slice(0,-300);
//        var final_value = data.true_value.slice(-302,-300);
//        var predict_new = data.predict_value.slice(-300);
//        var predict_new = final_value.concat(predict_new);
//        var fill_his = Array(predict_new.length).fill('-');
//        var fill_new = Array(true_his.length).fill('-');
//        option.series[0].data = true_his.concat(fill_his) ;
//        option.series[1].data = fill_new.concat(predict_new);
//        myChart.setOption(option, true);

        var true_his = data.true_value.slice(0, -30);
        var concat_value = data.true_value.slice(-32, -30); //使两段曲线能够连接起来
        var predict = data.predict_value.slice(-30);
//        var concat_value = data.true_value.slice(-32, -30); //使两段曲线能够连接起来
//        var predict = data.true_value.slice(-30);
        var predict_concat = concat_value.concat(predict)
        var fill_his = Array(predict_concat.length).fill('-');
        var fill_predict = Array(true_his.length).fill('-');
        option.series[0].data = true_his.concat(fill_his);
        option.series[1].data = fill_predict.concat(predict_concat);
        myChart.setOption(option, true);
    }
}

function history_query(){
    $("#dataerror").addClass("hide");
    var steel_type = $("#steel_type").val();
    var steeltype = $("#steeltype").val();
    var tradeno = $("#tradeno").val();
    var delivery = $("#delivery").val();
    var specification = $("#specification").val();
    var region = $("#region").val();
    var factory = $("#factory").val();
    var history_begin =$("#history_begin").val();
    var history_end =$("#history_end").val();
    var params = {
                    "history_begin":history_begin,
                    "history_end":history_end,
                    "steel_type":steel_type,
                    "steeltype":steeltype,
	                "tradeno":tradeno,
	                "delivery":delivery,
	                "specification":specification,
	                "factory":factory,
	                "region":region,
                 }
    console.log(JSON.stringify(params));
    $.ajax({
        type: "post",
        url:  "/price_history",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            console.log(data);
            if(data.state == 100002){
                $("#dataerror").removeClass("hide");
                $("#ele_info").html(data.ele_info)
                $("#dataerror").html(data.his_warnning);
                $("#history_figure").addClass("hide");
            }
            else if (data.state == 0){
                $("#history_figure").removeClass("hide");
                $("#ele_info").html(data.ele_info)
                drawHistoryPriceBrokenLineChart(data);
            }

        }
    })
}

var protfolio_sec_height = $("#protfolio_sec").height()

function layouttest(){
    /*
    * 测试动态布局
    */
    $("#figures").empty();
    $("#protfolio_sec").height(protfolio_sec_height);
    var pridict_result_json = {
        "linear_regression":"线性回归",
        "random_forest":"随机森林",
        "elm":"超限学习机elm",
        "svm":"支持向量机svm",
        "BP":"BP神经网络",
    }
    var selected_rs = {}
    var types = typestr.split(',');
    for(var key in types){
        index = types[key];
        selected_rs[index] = pridict_result_json[index];
    }


    console.log(selected_rs);
    console.log(pridict_result_json);
    var len = 0;
    for(var item in selected_rs)len++;
    console.log(len);
    var num = 0;
    $.each(selected_rs,function(name,value) {
        if(num ==0){
            figure_name = "predict_figure";
            drawPredictBrokenLineChart(value,figure_name,name);
            num = num + 1;
        }
        $("#protfolio_sec").height($("#protfolio_sec").height() + 400);
        $("#figures").append("<div id='"+ name +"' style='width: 500px;height:400px;'></div>")
        drawPredictBrokenLineChart(value,"",name);
    });
}

// 钢材价格预测
function predict_query(){
    $("#waitwarning").removeClass("hide");
    var timeScale = $("#time_scale_predict").val();
    console.log(timeScale);
    var type_array=new Array();
    $('input[name="predict_method"]:checked').each(function(){
        type_array.push($(this).val());//向数组中添加元素
    });
    var typestr=type_array.join(',');//将数组元素连接起来以构建一个字符串
    console.log(typestr);
    var steel_type = $("#steel_type_predict").val();
    var steeltype = $("#steeltype_predict").val();
    var tradeno = $("#tradeno_predict").val();
    var delivery = $("#delivery_predict").val();
    var specification = $("#specification_predict").val();
    var factory = $("#factory_predict").val();
    var region = $("#region_predict").val();
    var params = {
                    "steel_type":steel_type,
                    "steeltype":steeltype,
	                "tradeno":tradeno,
	                "delivery":delivery,
	                "specification":specification,
	                "factory":factory,
	                "typestr":typestr,
	                "region":region,
	                "timeScale":timeScale
                 };
    console.log(steel_type);
    console.log(JSON.stringify(params));

    $.ajax({
        type: "post",
        url:  "/price_predict",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            $("#waitwarning").addClass("hide");
            $("#figures").empty();
            $("#protfolio_sec").height(protfolio_sec_height);
            var pridict_result_json = data.result;
            console.log(pridict_result_json);
            var len = 0;
            for(var item in pridict_result_json)len++;
            console.log(len);
            var num = 0;
            timeline = data.timeline
            $.each(pridict_result_json,function(name,value) {
                if(num ==0){
                    figure_name = "predict_figure";
                    drawPredictBrokenLineChart(value,figure_name,name);
                    num = num + 1;
                }else{
                    $("#protfolio_sec").height($("#protfolio_sec").height() + 400);
                    $("#figures").append("<div id='"+ name +"' style='width: 500px;height:400px;'></div>")
                    drawPredictBrokenLineChart(value,"",name);
                }

            });
        }
    })

}

function iron_history_query(){
    $("#dataerror").addClass("hide");
    var history_begin =$("#history_begin").val();
    var history_end =$("#history_end").val();
    var yinsu_type =$("#yinsu_type").val();
    var params = {
        "history_begin":history_begin,
        "history_end":history_end,
        "yinsu_type":yinsu_type
        }
    console.log(JSON.stringify(params));
    $.ajax({
        type: "post",
        url:  "/stone_price_history",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            console.log(data);
            if(data.state == 100002){
                $("#dataerror").removeClass("hide");
                $("#ele_info").html(data.ele_info)
                $("#dataerror").html(data.his_warnning);
                $("#history_figure").addClass("hide");
            }
            else if (data.state == 0){
                $("#history_figure").removeClass("hide");
                $("#ele_info").html(data.ele_info)
                drawHistoryPriceBrokenLineChart(data);
            }
        }
    })
}

//绘制预测图
function drawIronPredictBrokenLineChart(data, figure_name, method){
    if(figure_name != "predict_figure"){
        figure_name = method;
    }
    var myChart = echarts.init(document.getElementById(figure_name));
    var pridict_result_json = {
        "logistic_regression":"逻辑回归",
        "random_forest":"随机森林",
        "elm":"超限学习机elm",
        "svm":"支持向量机svm",
    }
    option = {
        title: {
            text: pridict_result_json[method] + '预测图'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['历史值','预测值']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data:data.timeline
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'历史值',
                type:'line',
                stack: '总量',
                data:data.true_value
            },
            {
                name:'预测值',
                type:'line',
                stack: '总量',
                data:data.predict_value
            },
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

//铁矿石价格预测
function iron_predict_query(){
    var steelType = $("#iron_type").val();
    console.log(steelType);
    var timeScale = $("#time_scale").val();
    console.log(time_scale);
    var type_array=new Array();
    $('input[name="predict_method"]:checked').each(function(){
        type_array.push($(this).val());//向数组中添加元素
    });
    var typestr=type_array.join(',');//将数组元素连接起来以构建一个字符串
    console.log(typestr);
    var params = {"steelType":steelType,"typestr":typestr,"timeScale":timeScale}
    console.log(params);
    $.ajax({
        type: "post",
        url:  "/stone_price_predict",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            $("#figures").empty();
            $("#protfolio_sec").height(protfolio_sec_height);
            var pridict_result_json = data.result;
            console.log(pridict_result_json);
            var len = 0;
            for(var item in pridict_result_json)len++;
            console.log(len);
            var num = 0;
            timeline = data.timeline
            $.each(pridict_result_json,function(name,value) {
                if(num ==0){
                    figure_name = "predict_figure";
                    drawIronPredictBrokenLineChart(value, figure_name, name);
                    num = num + 1;
                }else{
                    $("#protfolio_sec").height($("#protfolio_sec").height() + 400);
                    $("#figures").append("<div id='"+ name +"' style='width: 500px;height:400px;'></div>")
                    drawIronPredictBrokenLineChart(value, "", name);
                }

            });
//            console.log(data);
//            drawPredictBrokenLineChart(data.result.zhi)
        }
    })
}
$(function(){

})
