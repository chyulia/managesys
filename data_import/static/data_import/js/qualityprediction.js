function drawHistoryPriceBrokenLineChart(data){
        var myChart = echarts.init(document.getElementById('history_figure'));
        option = {
            title: {
                text: '影响因素走势折线图'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['历史走势',]
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
                    name:'波罗的海指数',
                    type:'line',
                    stack: '总量',
                    data: data.price
                },
            ]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }
function drawPredictBrokenLineChart(data){
    var myChart = echarts.init(document.getElementById('predict_figure'));
    option = {
        title: {
            text: '预测图'
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
function history_query(){
    var ltype = $("#lftype").val();

    var rcsj =$("#rcsj").val();
    var ylzq =$("#ylzq").val();
    var jzwd =$("#jzwd").val();
    var dh =$("#dh").val();
    var zsdsj =$("#zsdsj").val();
    var alshl =$("#alshl").val();
    var althl =$("#althl").val();
    var chl =$("#chl").val();
    var mnhl =$("#mnhl").val();
    var shl =$("#shl").val();
    var phl =$("#phl").val();
    var wdc =$("#wdc").val();
    var wdcs =$("#wdcs").val();
    var tdcs =$("#tdcs").val();
    var jlcs =$("#jlcs").val();
    var hjwl =$("#hjwl").val();
    var fjswl =$("#fjswl").val();
    alert(ltype)
    // var history_end =$("#history_end").val();
    // var yinsu_type =$("#yinsu_type").val();
    var params = {"ltype":ltype,"rcsj":rcsj,"ylzq":ylzq,"jzwd":jzwd,"dh":dh,"zsdsj":zsdsj,"alshl":alshl,
                    "althl":althl,"chl":jzwd,"mnhl":mnhl,"shl":shl,"phl":phl,
                    "wdc":wdc,"wdcs":wdcs,"tdcs":tdcs,"jlcs":jlcs,"hjwl":hjwl,"fjswl":fjswl}
    console.log(JSON.stringify(params));
    $.ajax({
        type: "post",
        url:  "/lf_quality_history",
        data: params,
        error: function() {
            alert('456');
            console.log("404");
        },
        success: function(data) {
            alert('123');
            console.log(data);
            drawHistoryPriceBrokenLineChart(data);
        }
    })
}
function predict_query(){
    var lftype = $("#lf_type").val();
    console.log(lftype);
    var heatno = $("#heatno").val();
    console.log(heatno);
    var params = {"lftype":lftype,"heatno":heatno}
    console.log(params);
    $.ajax({
        type: "post",
        url:  "/lf_quality_predict",
        data: params,
        error: function() {
            alert('11');
            console.log("404");
        },
        success: function(data) {
            console.log(data);
            $(".number_ture").empty();
            $(".number_predict").empty();
            $(".number_ture").append(data.result.zhi.data_ture);
            $(".number_predict").append(data.result.zhi.data_predict);
        }
    })
}
$(function(){

})