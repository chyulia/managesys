
//地图----中国地图
function drawMapChartChina(data,tradeNo,aspect_name,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,unite){
    // echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));
    
        // 指定图表的配置项和数据
    option = {
        title : {
            text: module_name + '——' + aspect_name + '（' + space_name + '）',
            subtext: sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name,
            x:'center'
        },
        tooltip: {
            trigger: 'item',
            formatter : function (params) {
                //console.log(params);
                if (typeof params.value =='object'){
                   return aspect_name + '<br/>' + params.name + ' : 总销量为0，无法计算退货率！';
                }else{
                    return aspect_name + '<br/>' + params.name + ' : ' + params.value + unite;
                }
            }
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:[tradeNo]
        },
        dataRange: {
            min: 0,
            max:  (maxValue + 1),
            x: 'left',
            y: 'bottom',
            text:['高','低'],           // 文本，默认为数值文本
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
            //color: ['red','lightgray']
        },
        toolbox: {
            show: true,
            orient : 'vertical',
            x: 'right',
            y: 'center',
            feature : {
                //mark : {show: true},
                // dataView : {show: true, readOnly: false},
                //restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        roamController: {
            show: true,
            x: 'right',
            mapTypeControl: {
                'china': true
            }
        },
        series: [
            {
                name: tradeNo,
                type: 'map',
                mapType: 'china',
                roam: false,
                itemStyle:{
                    normal:{
                        label:{show:true},
                    },
                    emphasis:{label:{show:true}}

                },
                data: data
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//地图----中国地图 ---- 市场容量分析
function drawMapChartChina_ratio(all_dictionary,data,startYear,startMonth,endYear,endMonth){
    // echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));

    //console.log(data)
    //console.log(all_dictionary)
    //console.log(all_dictionary[0].name)
    //获取月/日的数据
    for (var i=0;i<8;i++)
    {
        //console.log(all_dictionary[i]);
        if(all_dictionary[i].name == '市场容量字典'){
            salesWeight_dictionary = all_dictionary[i].value;
            //console.log(salesWeight_dictionary);
        }else if (all_dictionary[i].name == '全部信息list'){
            all_list = all_dictionary[i].value;
        }else if (all_dictionary[i].name == '比例字典'){
            ratio_dictionary = all_dictionary[i].value;
        }else if(all_dictionary[i].name == '青钢销量字典'){
            qdisSalesWeight_dictionary = all_dictionary[i].value;
        }else if(all_dictionary[i].name == '饼图比例字典'){
            pie_ratio = all_dictionary[i].value;
        }else if(all_dictionary[i].name == '饼图市场容量字典'){
            pie_salesWeigh = all_dictionary[i].value;
        }else if(all_dictionary[i].name == '饼图青钢销量字典'){
            pie_qdisSalesWeight = all_dictionary[i].value;
        }else if(data[i].name == '饼图省份名称'){
            pie_nameList = data[i].value;
        }else {
            ratio_rst = all_dictionary[i].value;
        }
    }
    

        // 指定图表的配置项和数据
    option = {
        title : {
            text: "市场容量分析",
            subtext: startYear + "年" + startMonth + "月至" + endYear + "年" + endMonth + "月内，全国各省份市场容量及占比",
            x:'center'
        },
        tooltip: {
            trigger: 'item',
            formatter : function (params) {
                console.log(params);
                return  params.name + ':<br/>市场容量：' + salesWeight_dictionary[params.name] + '吨<br/>我公司销量：' + qdisSalesWeight_dictionary[params.name] + '吨<br/>市场容量占比：' + params.value + '%';
            }
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:["市场容量占比"]
        },
        dataRange: {
            min: 0,
            max:  100,
            x: 'left',
            y: 'bottom',
            text:['高','低'],           // 文本，默认为数值文本
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
            //color: ['red','lightgray']
        },
        toolbox: {
            show: true,
            orient : 'vertical',
            x: 'right',
            y: 'center',
            feature : {
                //mark : {show: true},
                // dataView : {show: true, readOnly: false},
                //restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        roamController: {
            show: true,
            x: 'right',
            mapTypeControl: {
                'china': true
            }
        },
        series: [
            {
                name: "市场容量占比",
                type: 'map',
                mapType: 'china',
                roam: false,
                itemStyle:{
                    normal:{
                        label:{show:true},
                    },
                    emphasis:{label:{show:true}}

                },
                data: data
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}



//地图 --- 世界地图
function drawMapChartWorld(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name){
    // echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));
    
        // 指定图表的配置项和数据
    option = {
        title : {
            text: module_name + '——' + aspect_name + '（' + space_name + '）',
            subtext: sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name,
            x:'center',
            y:'top'
        },
       
        tooltip : {
            trigger: 'item',
            formatter : function (params) {
                //console.log(params);
                if (typeof params.value =='object'){
                    return aspect_name + '<br/>' + params.name + ' : 总销量为0，无法计算退货率！';
                }else{
                    return aspect_name + '<br/>' + params.name + ' : ' + params.value + unite;
                }
            }
        },
        toolbox: {
            show : true,
            orient : 'vertical',
            x: 'right',
            y: 'center',
            feature : {
                //mark : {show: true},
                // dataView : {show: true, readOnly: false},
                //restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        dataRange: {
            min: 0,
            max:  (maxValue + 1),
            text:['High','Low'],
            realtime: false,
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
        },
        series : [
            {
                name: aspect_name,
                type: 'map',
                mapType: 'world',
                roam: true,
                mapLocation: {
                    y : 60
                },
                itemStyle:{
                    emphasis:{label:{show:true}}
                },
                data:data
            }
        ]
    };
                    
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}



//地图----山东地图
function drawMapChartShandong(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name){
    // echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));
    
        // 指定图表的配置项和数据
    option = {
        title : {
            text: module_name + '——' + aspect_name + '（' + space_name + '）',
            subtext: sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name,
            x:'center'
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:[tradeNo]
        },
        tooltip : {
            trigger: 'item',
            formatter : function (params) {
                //console.log(params);
                if (typeof params.value =='object'){
                    return aspect_name + '<br/>' + params.name + ' : 总销量为0，无法计算退货率！';
                }else{
                    return aspect_name + '<br/>' + params.name + ' : ' + params.value + unite;
                }
            }
            // formatter: function(a){
            //   return a[2];
            // }
        },
        dataRange: {
            min: 0,
            max: (maxValue + 1),
            x: 'left',
            y: 'bottom',
            text:['高','低'],           // 文本，默认为数值文本
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
        },
        series : [
            {
                name: tradeNo,
                type: 'map',
                mapType: '山东',
                selectedMode: 'single',
                itemStyle:{
                    normal:{label:{show:true}},
                    emphasis:{label:{show:true}}
                },
                data: data
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//时间折线图 (Echarts 2)
function drawTimeLineBar(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,showStyle,sql_cust){

    var myChart = echarts.init(document.getElementById('main4'));
    //console.log(data);
    //console.log(data[0]);
    //console.log(data[0].name);
    //console.log(data[0].value);

//     myChart.showLoading({
//                     text: "图表数据正在努力加载..."
//                 });
    
    //获取月/日的数据
    for (var i=0;i<10;i++)
    {
        if(data[i].name == 'timeline_Day'){
            timeline_Day = data[i].value;
        }else if (data[i].name == 'timelineValue_Day'){
            timelineValue_Day = data[i].value;
        }else if (data[i].name == 'timeline_Month'){
            timeline_Month = data[i].value;
        }else if (data[i].name == 'timelineValue_Month'){
            timelineValue_Month = data[i].value;
        }else if (data[i].name == 'timeline_Week'){
            timeline_Week = data[i].value;
        }else if(data[i].name == 'timelineValue_Week'){
            timelineValue_Week = data[i].value;
        }else if (data[i].name == 'timeline_15Day'){
            timeline_15Day = data[i].value;
        }else if(data[i].name == 'timelineValue_15Day'){
            timelineValue_15Day = data[i].value;
        }else if (data[i].name == 'timeline_20Day'){
            timeline_20Day = data[i].value;
        }else{
            timelineValue_20Day = data[i].value;
        }
    }

    //月/日显示方式
    if (showStyle == 1){ //月
        timeline = timeline_Month;
        timelineValue = timelineValue_Month;
    }else if(showStyle == 2){ //周
        timeline = timeline_Week;
        timelineValue = timelineValue_Week;
    }else if(showStyle == 3){ //日
        timeline = timeline_Day;
        timelineValue = timelineValue_Day;
    }else if(showStyle == 4){ //15天
        timeline = timeline_15Day;
        timelineValue = timelineValue_15Day;
    }else { //20天
        timeline = timeline_20Day;
        timelineValue = timelineValue_20Day;
    }

    if (module_name == "时间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
    }else{
        title = module_name + '——' + aspect_name + '（客户：' + sql_cust + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的，客户' + sql_cust + '范围内' + aspect_name;
    }

    option = {
    title : {
        text: title,
        subtext: subtext,
        x:'center'
    },
    tooltip : {
        trigger: 'axis', 
        formatter : function (params) {
                //console.log(params);
                //console.log(params[0].name);
                //console.log(params[0].value);
                if (params[0].value == "总销量为0，无法计算退货率！"){
                    return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value;
                }else{
                    return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value + unite;
                }
                
            }
    },
    toolbox: {   //这个不用改
        show : true,
        feature : {
            //dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    dataZoom: {            //这个不用改，下面日期默认缩放区域大小,0-100指最前与最后

        start :0,

        end :100 
    },
    legend : {
        orient: 'vertical',
        x:'left',
        data : [tradeNo]
    },
    grid: {  //这个不用改，图所占区域竖直方向长度
        y2: 80
    },
    xAxis : [   //这个不用改
        {
            type : 'category',
            boundaryGap : false,
            data : timeline
        }
    ],
    yAxis : [ //这个不用改
        {
            type : 'value'
        }
    ],
    series : [
        {
            name: tradeNo,
            type: 'line',
            data:timelineValue
        }
    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//普通折线图 (Echarts 2)
function drawTimeLineBar_normal(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,sql_cust){

    var myChart = echarts.init(document.getElementById('main4'));
    console.log(data);
    console.log(data[0]);
    console.log(data[0].name);
    console.log(data[0].value);

//     myChart.showLoading({
//                     text: "图表数据正在努力加载..."
//                 });
    lineName = []
    lineValue = []
    for (var i=0;i<data.length;i++)
    {       
        lineName.push(data[i].name);  
        lineValue.push(data[i].value);
    }

    if (module_name == "空间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
 
    }else if (module_name == "时间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
    }else{
        title = module_name + '——' + aspect_name + '（客户：' + sql_cust + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的，客户' + sql_cust + '范围内' + aspect_name;
    }

    option = {
    title : {
        text: title,
        subtext: subtext,
        x:'center'
    },
    tooltip : {
        trigger: 'axis', 
        formatter : function (params) {
                //console.log(params);
                //console.log(params[0].name);
                //console.log(params[0].value);
                if (params[0].value == "总销量为0，无法计算退货率！"){
                    return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value;
                }else{
                    return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value + unite;
                }
                
            }
    },
    toolbox: {   //这个不用改
        show : true,
        feature : {
            //dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    dataZoom: {            //这个不用改，下面日期默认缩放区域大小,0-100指最前与最后
        show : true,
        //realtime : true,
        // start : 30,
        // end : 70

    },
    legend : {
        orient: 'vertical',
        x:'left',
        data : [tradeNo]
    },
    grid: {  //这个不用改，图所占区域竖直方向长度
        y2: 80
    },
    xAxis : [   //这个不用改
        {
            type : 'category',
            //boundaryGap : false,
            data : lineName,
            //data : [1,2,3,4,5],
            axisLabel: {
                interval:0,//横轴信息全部显示
                //rotate: 90,//60度角倾斜显示
                formatter:function(val){
                    return val.split("").join("\n"); //横轴信息文字竖直显示
                }
            }
        }
    ],
    yAxis : [ //这个不用改
        {
            type : 'value'
        }
    ],
    series : [
        {
            name: tradeNo,
            type: 'line',
            data:lineValue
            //data:[5,6,4,6,5],
        }
    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//普通柱状图 (Echarts 2)
function drawBar_normal(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,sql_cust){

    var myChart = echarts.init(document.getElementById('main4'));
    console.log(data);
    console.log(data[0]);
    console.log(data[0].name);
    console.log(data[0].value);

//     myChart.showLoading({
//                     text: "图表数据正在努力加载..."
//                 });
    lineName = []
    lineValue = []
    for (var i=0;i<data.length;i++)
    {       
        lineName.push(data[i].name);  
        lineValue.push(data[i].value);
    }

    if (module_name == "空间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
 
    }else if (module_name == "时间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
    }else{
        title = module_name + '——' + aspect_name + '（客户：' + sql_cust + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的，客户' + sql_cust + '范围内' + aspect_name;
    }

    option = {
        title : {
            text: title,
            subtext: subtext,
            x:'center'
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:[tradeNo]
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                //dataView : {show: true, readOnly: false},
                //magicType: {show: true, type: ['line', 'bar']},
                //restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        // dataZoom: {            //这个不用改，下面日期默认缩放区域大小,0-100指最前与最后
        //     show : true,
        //     //realtime : true,
        //     start : 30,
        //     end : 70

        // },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                //boundaryGap : [0, 0.01]
                data: lineName,
                axisLabel: {
                    interval:0,//横轴信息全部显示
                    //rotate: 90,//60度角倾斜显示
                    formatter:function(val){
                        return val.split("").join("\n"); //横轴信息文字竖直显示
                    }
                }
            }

        ],
        yAxis : [
            {
                
                type : 'value',
                //data : lineValue
            }
        ],
        series : [
            {
                name:tradeNo,
                type:'bar',
                data:lineValue
            }
        ]
    };
                    
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//钢种分析饼图 (Echarts 2)
function drawpie(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,sql_cust){

    var myChart = echarts.init(document.getElementById('main4'));
    // console.log(data);
     console.log(tradeNo);
    // console.log(data[0]);
    // console.log(data[0].name);
    // console.log(data[0].value);
    if (module_name == "空间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
    }else if (module_name == "钢种分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;

    }else{
        title = module_name + '——' + aspect_name + '（客户：' + sql_cust + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的，客户' + sql_cust + '范围内' + aspect_name;
    }
    
    option = {
    title : {
        text: title,
        subtext: subtext,
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: aspect_name + "占比 <br/>{b} : {c} " + unite + "({d}%)"
    },
    // legend: {
    //     orient : 'vertical',
    //     x : 'left',
    //     data:[tradeNo]
    // },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            // dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:"饼状图",
            type:'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:data
        }
    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//钢种分析饼图 (Echarts 2)
function drawpie_marketShare(pie_data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,sql_cust,data){

    var myChart = echarts.init(document.getElementById('main4'));
    // console.log(data);
    // console.log(tradeNo);
    // console.log(data[0]);
    // console.log(data[0].name);
    // console.log(data[0].value);
    
    for (var i=0;i<8;i++)
    {
        if(data[i].name == '市场容量字典'){
            salesWeight_dictionary = data[i].value;
            console.log(salesWeight_dictionary);
        }else if (data[i].name == '全部信息list'){
            all_list = data[i].value;
        }else if (data[i].name == '比例字典'){
            ratio_dictionary = data[i].value;
        }else if(data[i].name == '青钢销量字典'){
            qdisSalesWeight_dictionary = data[i].value;
        }else if(data[i].name == '饼图比例字典'){
            pie_ratio = data[i].value;
        }else if(data[i].name == '饼图市场容量字典'){
            pie_salesWeigh = data[i].value;
        }else if(data[i].name == '饼图青钢销量字典'){
            pie_qdisSalesWeight = data[i].value;
        }else if(data[i].name == '饼图省份名称'){
            pie_nameList = data[i].value;
        }else {
            ratio_rst = data[i].value;
        }
    }
    // console.log(pie_nameList);
    // var list_pie_nameList = new Array();
    // for (var i=0;i<pie_nameList.length;i++)
    // {
    //     list_pie_nameList[i] = pie_nameList[i].name
    // }
    // console.log(pie_ratio)

    option = {
    title : {
        text: module_name,
        subtext: sql_date1 + '至' + sql_date2 + '内，全国各省份市场容量及占比',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{b} <br/>市场容占比 : {c}% <br/>市场容量占比占全国百分比:{d}%"
        // formatter : function (params) {
        //     console.log(params);
        //     return  params.name + ':<br/>市场容量：' + pie_salesWeigh[params.name] + '吨<br/>我公司销量：' + pie_qdisSalesWeight[params.name] + '吨<br/>市场容量占比：' + params.value + '%<br/>({d}%)';
        // }
    },
    // legend: {
    //     orient : 'vertical',
    //     x : 'left',
    //     data:['各省份市场容量及占比']
    // },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            // dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:"饼状图",
            type:'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:pie_data
        }
    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}



//钢种分析漏斗图 (Echarts 2)
function drawfunnel(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,sql_cust){

    var myChart = echarts.init(document.getElementById('main4'));
    console.log(data);
    //console.log(tradeNo);
    console.log(data[0]);
    //console.log(data[0].name);
    //console.log(data[0].value);
    widthValue = "40%";
    xValue = '30%';
    yValue = '30%';
    maxValue = 0;
    if (module_name == "空间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
        widthValue = "40%";
        for(var i=0; i<data.length; i++)  {  
            if(data[i].value > maxValue){
                maxValue = data[i].value;
            }else{
                maxValue = maxValue;
            }
        }  
    }else if (module_name == "钢种分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
        for(var i=0; i<data.length; i++)  {  
            if(data[i].value > maxValue){
                maxValue = data[i].value;
            }else{
                maxValue = maxValue;
            }
        }
    }else{
        title = module_name + '——' + aspect_name + '（客户：' + sql_cust + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的，客户' + sql_cust + '范围内' + aspect_name;
        for(var i=0; i<data.length; i++)  {  
            if(data[i].value > maxValue){
                maxValue = data[i].value;
            }else{
                maxValue = maxValue;
            }
        }
    }

    
    option = {
    title : {
        text: title,
        subtext: subtext,
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: aspect_name + "<br/>{b} : {c}" + unite
    },
    // legend: {
    //     orient : 'vertical',
    //     x : 'left',
    //     data:[tradeNo]
    // },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            // dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'漏斗图',
            type:'funnel',
            width: widthValue,
            x : xValue,
            y : yValue,
            data:data,
            max: maxValue
        },

    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//钢种分析饼图 (Echarts 2)
function drawpie_marketShare(pie_data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,sql_cust,data){

    var myChart = echarts.init(document.getElementById('main4'));
    // console.log(data);
    // console.log(tradeNo);
    // console.log(data[0]);
    // console.log(data[0].name);
    // console.log(data[0].value);
    
    for (var i=0;i<8;i++)
    {
        if(data[i].name == '市场容量字典'){
            salesWeight_dictionary = data[i].value;
            console.log(salesWeight_dictionary);
        }else if (data[i].name == '全部信息list'){
            all_list = data[i].value;
        }else if (data[i].name == '比例字典'){
            ratio_dictionary = data[i].value;
        }else if(data[i].name == '青钢销量字典'){
            qdisSalesWeight_dictionary = data[i].value;
        }else if(data[i].name == '饼图比例字典'){
            pie_ratio = data[i].value;
        }else if(data[i].name == '饼图市场容量字典'){
            pie_salesWeigh = data[i].value;
        }else if(data[i].name == '饼图青钢销量字典'){
            pie_qdisSalesWeight = data[i].value;
        }else if(data[i].name == '饼图省份名称'){
            pie_nameList = data[i].value;
        }else {
            ratio_rst = data[i].value;
        }
    }
    // console.log(pie_nameList);
    // var list_pie_nameList = new Array();
    // for (var i=0;i<pie_nameList.length;i++)
    // {
    //     list_pie_nameList[i] = pie_nameList[i].name
    // }
    // console.log(pie_ratio)

    option = {
    title : {
        text: module_name,
        subtext: sql_date1 + '至' + sql_date2 + '内，全国各省份市场容量及占比',
        x:'center'
    },

    tooltip : {
        trigger: 'item',
        formatter: aspect_name + "<br/>{b} : {c}" + unite
    },
    // legend: {
    //     orient : 'vertical',
    //     x : 'left',
    //     data:[tradeNo]
    // },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            // dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'漏斗图',
            type:'funnel',
            width: '40%',
            x : '30%',
            y : '30%',
            data:pie_data,
            max: maxValue
        },

    ]








};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


////时间折线图 (Echarts 2) 和 指数平滑移动平均值 多条折线
function drawTimeLineBar_average(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,showStyle,sql_cust,N){

    //var myChart = echarts.init(document.getElementById('main4'));

    //console.log(data);
    //console.log(data[0]);
    //console.log(data[0].name);
    //console.log(data[0].value);
    
    //获取月/日的数据
    for (var i=0;i<10;i++)
    {
        if(data[i].name == 'timeline_Day'){
            timeline_Day = data[i].value;            
        }else if (data[i].name == 'timelineValue_Day'){
            timelineValue_Day = data[i].value;            
        }else if (data[i].name == 'timeline_Month'){
            timeline_Month = data[i].value;
        }else if (data[i].name == 'timelineValue_Month'){
            timelineValue_Month = data[i].value;
        }else if (data[i].name == 'timeline_Week'){
            timeline_Week = data[i].value;
        }else if(data[i].name == 'timelineValue_Week'){
            timelineValue_Week = data[i].value;
        }else if (data[i].name == 'timeline_15Day'){
            timeline_15Day = data[i].value;
        }else if(data[i].name == 'timelineValue_15Day'){
            timelineValue_15Day = data[i].value;
        }else if (data[i].name == 'timeline_20Day'){
            timeline_20Day = data[i].value;
        }else{
            timelineValue_20Day = data[i].value;
        }
    }

    //月/日显示方式
    if (showStyle == 1){ //月
        timeline = timeline_Month;
        timelineValue = timelineValue_Month;
        unite_of_time = "月"
    }else if(showStyle == 2){ //周
        timeline = timeline_Week;
        timelineValue = timelineValue_Week;
        unite_of_time = "7日"
    }else if(showStyle == 3){ //日
        timeline = timeline_Day;
        timelineValue = timelineValue_Day;
        unite_of_time = "日"
    }else if(showStyle == 4){ //15天
        timeline = timeline_15Day;
        timelineValue = timelineValue_15Day;
        unite_of_time = "15日"
    }else { //20天
        timeline = timeline_20Day;
        timelineValue = timelineValue_20Day;
        unite_of_time = "20日"
    }

    // // 周期时间
    // var N = 6; 
    //如果数据数量小于N值，将小的值赋给N
    if (timeline.length < N){
        N = timeline.length;
    }
    //求 EXPMA
    EXPMA_timeline_Value = EXPMA(timelineValue,N);


    if (module_name == "时间分析"){
        title = module_name + '——' + aspect_name + '（' + space_name + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
    }else{
        title = module_name + '——' + aspect_name + '（客户：' + sql_cust + '）';
        subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的，客户' + sql_cust + '范围内' + aspect_name;
    }

    data_Value = "所选钢种的" + aspect_name
    data_Value_average = N + "个" + unite_of_time + "指数平滑移动平均值"

    option = {
    title : {
        text: title,
        subtext: subtext,
        x:'center'
    },
    tooltip : {
        trigger: 'axis', 
        formatter : function (params) {
            //   新写一个函数，先算数值，把这个函数的前面全包含进来
            //   在吧算好的数值传入到此函数中，数值包含EXPMA
            //   此时就可以保证提示文本不出错了
                //console.log(params);
                //console.log(params[0].name);
                //console.log(EXPMA_timeline_Value);
                //console.log(params[0].value);
                if (params[0].value == "总销量为0，无法计算退货率！"){
                    return params[0].name + "<br/>" +  data_Value + " : " + params[0].value+ "<br/>" +  data_Value_average + " : " + EXPMA_timeline_Value[params[1].dataIndex] + unite;
                }else{
                    return params[0].name + "<br/>" +  data_Value + " : " + params[0].value + unite + "<br/>" +  data_Value_average + " : " + EXPMA_timeline_Value[params[1].dataIndex] + unite;
                }
                
            }
    },
    toolbox: {   //这个不用改
        show : true,
        feature : {
            //dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    dataZoom: {            //这个不用改，下面日期默认缩放区域大小,0-100指最前与最后

        start :0,

        end :100 
    },
    legend : {
        orient: 'vertical',
        x:'left',
        data : [data_Value,data_Value_average]
    },
    grid: {  //这个不用改，图所占区域竖直方向长度
        y2: 80
    },
    xAxis : [   //这个不用改
        {
            type : 'category',
            boundaryGap : false,
            data : timeline
        }
    ],
    yAxis : [ //这个不用改
        {
            type : 'value'
        }
    ],
    series : [
        {
            name: data_Value,
            type: 'line',
            data:timelineValue
        },
        {
            name: data_Value_average,
            type: 'line',
            data:EXPMA_timeline_Value
        }
    ]
};

    var myChart = echarts.init(document.getElementById('main4'));
    myChart.setOption(option);

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//求指数平滑移动平均值
function EXPMA(data,N){//  N 为周期天数  data 为全部数据的list
    //console.log(data);
    var a_index = 2 / ( N + 1 ); //平滑指数
    var EXPMA = new Array(); //用于存放计算好的移动平滑指数 前N天是没有数据的
    var sum = 0;
    //   arr[0] = "aaa"; //添加
    //   arr.pop();  //删除
    //   arr.push(6);  //在结尾添加并返回长度 
    
    // 【 求初始值（第一个值）】
    // 一种理解
    for (var i = 0 ; i < N ; i++){
        sum = sum + data[i];
    }
    EXPMA[0] = Math.round(sum / N) ; //前N日均值作为该值
    // //另一种理解
    // EXPMA[0] = data[0]; //第一个 EMP 为当日值

    // 【 迭代求后面的值 】
    for (var i = 1 ; i < data.length ; i++ ){  //初始值 i = 1
        EXPMA[i] = Math.round(a_index * (data[i] - EXPMA[i-1]) + EXPMA[i-1]); //EMA 的计算公式
    }

    return EXPMA;

}



////库存管理
function drawStockControl(data,module_unit_key){

    //var myChart = echarts.init(document.getElementById('main4'));
    console.log("正在绘图");
    console.log(data);

    for (var i=0;i<4;i++)
    {
        if(data[i].name == 'tradeNo'){
            tradeNo = data[i].value;            
        }else if (data[i].name == 'stock_All'){
            stock_All = data[i].value;            
        }else if (data[i].name == 'stock_overstock'){
            stock_overstock = data[i].value;
        }else{
            percent = data[i].value;
        }
    }

    // console.log(tradeNo)
    // console.log(stock_All)
    // console.log(stock_overstock)
    // console.log(percent)

    option = {
    title : {
        text: "库存管理",
        subtext: "subtext",
        x:'center'
    },
    tooltip : {
        trigger: 'axis', 
        formatter : function (params) {
                //console.log(params);
                return params[0].name + "<br/>" +  params[0].seriesName + ":" + params[0].value + "<br/>库龄大于3月的总重量:" + params[1].value ;
            }
    },
    legend: {
        orient: 'vertical',
        x:'left',
        data:['总重量', '库龄大于3月的总重量']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            // dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            data : tradeNo
        }
    ],
    series : [
        {
            name:'总重量',
            type:'bar',
            data:stock_All
           
        },
        {
            name:'库龄大于3月的总重量',
            type:'bar',
            data:stock_overstock
            
        }
    ]




};

    var myChart = echarts.init(document.getElementById('main4'));
    myChart.setOption(option);

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}



// //时间折线图 (Echarts 2) 和 指数平滑移动平均值 多图联动
// function drawTimeLineBar_average2(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,showStyle,sql_cust){

//     //var myChart = echarts.init(document.getElementById('main4'));

//     //console.log(data);
//     //console.log(data[0]);
//     //console.log(data[0].name);
//     //console.log(data[0].value);
    
//     //获取月/日的数据
//     for (var i=0;i<10;i++)
//     {
//         if(data[i].name == 'timeline_Day'){
//             timeline_Day = data[i].value;            
//         }else if (data[i].name == 'timelineValue_Day'){
//             timelineValue_Day = data[i].value;
//         }else if (data[i].name == 'timeline_Month'){
//             timeline_Month = data[i].value;
//         }else if (data[i].name == 'timelineValue_Month'){
//             timelineValue_Month = data[i].value;
//         }else if (data[i].name == 'timeline_Week'){
//             timeline_Week = data[i].value;
//         }else if(data[i].name == 'timelineValue_Week'){
//             timelineValue_Week = data[i].value;
//         }else if (data[i].name == 'timeline_15Day'){
//             timeline_15Day = data[i].value;
//         }else if(data[i].name == 'timelineValue_15Day'){
//             timelineValue_15Day = data[i].value;
//         }else if (data[i].name == 'timeline_20Day'){
//             timeline_20Day = data[i].value;
//         }else{
//             timelineValue_20Day = data[i].value;
//         }
//     }

//     //月/日显示方式
//     if (showStyle == 1){ //月
//         timeline = timeline_Month;
//         timelineValue = timelineValue_Month;        
//     }else if(showStyle == 2){ //周
//         timeline = timeline_Week;
//         timelineValue = timelineValue_Week;
//     }else if(showStyle == 3){ //日
//         timeline = timeline_Day;
//         timelineValue = timelineValue_Day;
//     }else if(showStyle == 4){ //15天
//         timeline = timeline_15Day;
//         timelineValue = timelineValue_15Day;
//     }else { //20天
//         timeline = timeline_20Day;
//         timelineValue = timelineValue_20Day;
//     }

//     if (module_name == "时间分析"){
//         title = module_name + '——' + aspect_name + '（' + space_name + '）';
//         subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name;
//     }else{
//         title = module_name + '——' + aspect_name + '（客户：' + sql_cust + '）';
//         subtext = sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的，客户' + sql_cust + '范围内' + aspect_name;
//     }

//     option = {
//     title : {
//         text: title,
//         subtext: subtext,
//         x:'center'
//     },
//     tooltip : {
//         trigger: 'axis', 
//         formatter : function (params) {
//                 //console.log(params);
//                 //console.log(params[0].name);
//                 //console.log(params[0].value);
//                 if (params[0].value == "总销量为0，无法计算退货率！"){
//                     return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value;
//                 }else{
//                     return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value + unite;
//                 }
                
//             }
//     },
//     toolbox: {   //这个不用改
//         show : true,
//         feature : {
//             //dataView : {show: true, readOnly: false},
//             saveAsImage : {show: true}
//         }
//     },
//     dataZoom: {            //这个不用改，下面日期默认缩放区域大小,0-100指最前与最后

//         start :0,

//         end :100 
//     },
//     legend : {
//         orient: 'vertical',
//         x:'left',
//         data : [tradeNo]
//     },
//     grid: {  //这个不用改，图所占区域竖直方向长度
//         y2: 80
//     },
//     xAxis : [   //这个不用改
//         {
//             type : 'category',
//             boundaryGap : false,
//             data : timeline
//         }
//     ],
//     yAxis : [ //这个不用改
//         {
//             type : 'value'
//         }
//     ],
//     series : [
//         {
//             name: tradeNo,
//             type: 'line',
//             data:timelineValue
//         }
//     ]
// };

//     var myChart = echarts.init(document.getElementById('main4'));
//     myChart.setOption(option);


//     option2 = {
//     title : {
//         text: title,
//         subtext: subtext,
//         x:'center'
//     },
//     tooltip : {
//         trigger: 'axis', 
//         formatter : function (params) {
//                 //console.log(params);
//                 //console.log(params[0].name);
//                 //console.log(params[0].value);
//                 if (params[0].value == "总销量为0，无法计算退货率！"){
//                     return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value;
//                 }else{
//                     return params[0].name + "<br/>" +  "所选钢种" + aspect_name + " : " + params[0].value + unite;
//                 }
                
//             }
//     },
//     toolbox: {   //这个不用改
//         show : true,
//         feature : {
//             //dataView : {show: true, readOnly: false},
//             saveAsImage : {show: true}
//         }
//     },
//     dataZoom: {            //这个不用改，下面日期默认缩放区域大小,0-100指最前与最后

//         start :0,

//         end :100 
//     },
//     legend : {
//         orient: 'vertical',
//         x:'left',
//         data : [tradeNo]
//     },
//     grid: {  //这个不用改，图所占区域竖直方向长度
//         y2: 80
//     },
//     xAxis : [   //这个不用改
//         {
//             type : 'category',
//             boundaryGap : false,
//             data : timeline
//         }
//     ],
//     yAxis : [ //这个不用改
//         {
//             type : 'value'
//         }
//     ],
//     series : [
//         {
//             name: tradeNo,
//             type: 'line',
//             data:timelineValue
//         }
//     ]
// };


//     var myChart2 = echarts.init(document.getElementById('main6'));
//     myChart2.setOption(option2);

//     myChart.connect(myChart2);
//     myChart2.connect(myChart);

//     setTimeout(function (){
//         window.onresize = function () {
//             myChart.resize();
//             myChart2.resize();
//         }
//     },200)


//     // 使用刚指定的配置项和数据显示图表。
//     myChart.setOption(option);
// }

