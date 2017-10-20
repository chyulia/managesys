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
function drawPredictBrokenLineChart(data,figure_name,method){
    if(figure_name != "predict_figure"){
        figure_name = method;
    }
    var pridict_result_json = {
        "linear_regression":"线性回归",
        "random_forest":"随机森林",
        "elm":"超限学习机elm",
        "svm":"支持向量机svm",
        "BP":"BP神经网络",
    }
    var myChart = echarts.init(document.getElementById(figure_name));
    option = {
        title: {
            text: pridict_result_json[method] + '预测图',
            subtext: '评分：'+data.score,
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
        var startTime = +new Date();
        var true_his = data.true_value.slice(0,-300);
        var final_value = data.true_value.slice(-302,-300);
        var predict_new = data.predict_value.slice(-300);
        var predict_new = final_value.concat(predict_new);
        var fill_his = Array(predict_new.length).fill('-');
        var fill_new = Array(true_his.length).fill('-');
        option.series[0].data = true_his.concat(fill_his) ;
        option.series[1].data = fill_new.concat(predict_new);
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

function drawBrokenLineChart(data,figure_name){
    var myChart = echarts.init(document.getElementById(figure_name));
    option = {
        title: {
            text: '折线图堆叠'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['邮件营销','联盟广告','视频广告','直接访问','搜索引擎']
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
            data: ['周一','周二','周三','周四','周五','周六','周日']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'邮件营销',
                type:'line',
                stack: '总量',
                data:[120, 132, 101, 134, 90, 230, 210]
            },
            {
                name:'联盟广告',
                type:'line',
                stack: '总量',
                data:[220, 182, 191, 234, 290, 330, 310]
            },
            {
                name:'视频广告',
                type:'line',
                stack: '总量',
                data:[150, 232, 201, 154, 190, 330, 410]
            },
            {
                name:'直接访问',
                type:'line',
                stack: '总量',
                data:[320, 332, 301, 334, 390, 330, 320]
            },
            {
                name:'搜索引擎',
                type:'line',
                stack: '总量',
                data:[820, 932, 901, 934, 1290, 1330, 1320]
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
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
    var params = {
                    "steel_type":steel_type,
                    "steeltype":steeltype,
	                "tradeno":tradeno,
	                "delivery":delivery,
	                "specification":specification,
	                "factory":factory,
	                "typestr":typestr,
	                "timeScale":timeScale
                 }
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
$(function(){

})
