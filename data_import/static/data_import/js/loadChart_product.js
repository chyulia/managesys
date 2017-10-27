
//单炉次成本分析：------------------
     // 条形图（原料raw）(多Y轴直方图)
    function drawBarChart_raw(heat_no,str_select,result){
        // var myChart = echarts.init(document.getElementById('main1'));
        var myChart = echarts.getInstanceByDom(document.getElementById('main1'));
        myChart.clear();
        // var colors = ['#5793f3', '#d14a61', '#675bba','#00c957','#5793f3', '#d14a61', '#675bba','#00c957'];
        // var colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF','#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF'];
        // var colors = ['#FCBE91','#AB837D','#E6DD86','#BCA997','#ADC8C8','#9D947E','#AE8083','#9C8987','#807455','#DEC87B','#C3B7BB'];
        var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
        var barWidth_value=40;//柱条（K线蜡烛）宽度
        var barGap_value='100%';//柱间距离，默认为柱形宽度的30%，可设固定值
        var barCategoryGap_value='60%';//类目间柱形距离，默认为类目间距的20%，可设固定值

            // 指定图表的配置项和数据
            var option = {
                color:colors,
                title: {
                    text: '炉次号'+heat_no+'的原料组成',
                    x:'center'
                },
                tooltip: {
                    // trigger: 'axis',
                    // axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    //     type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        trigger:'item',
                        formatter: function (params){
                            var res = result.raw.xname[params.seriesIndex]+':</br>实际值：'+params.value+result.raw.danwei[params.seriesIndex] + '<br/>偏离程度：'+result.raw.offset_result[params.seriesIndex]+'</br>定性判断：'+result.raw.qualitative_offset_result[params.seriesIndex];
                            return res;

                     }
                },
                toolbox: {
                    show : true,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['']
                },
                xAxis: {
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: ['单炉次原料投入字段']
                },
                yAxis: [{
                    type: 'value',
                    name: '铁水重量(Kg)',
                    min: 0,
                    max: 105000,
                    position: 'left',
                    offset:-20,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[0]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '生铁(Kg)',
                    min: 0,
                    max: 12000,
                    position: 'left',
                    offset: -100,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[1]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} NM3'
                    // }
                },
                {
                    type: 'value',
                    name: '废钢总和(Kg)',
                    min: 0,
                    max: 12000,
                    position: 'left',
                    splitLine:{show: false},//去除网格线
                    offset: -180,
                    axisLine: {
                        lineStyle: {
                            color: colors[2]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '大渣钢(Kg)',
                    min: 0,
                    max: 10000,
                    position: 'left',
                    offset: -260,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[3]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '自产废钢(Kg)',
                    min: 0,
                    max: 10000,
                    position: 'left',
                    offset: -340,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[4]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '重型废钢(Kg)',
                    min: 0,
                    max: 10000,
                    position: 'left',
                    offset: -420,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[5]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '中型废钢(Kg)',
                    min: 0,
                    max: 10000,
                    position: 'left',
                    offset: -500,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[6]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                }
                ],
                series: [{
                    name: '铁水重量',
                    type: 'bar',
                    barWidth : barWidth_value,//柱条（K线蜡烛）宽度
                    barGap: barGap_value,//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap: barCategoryGap_value,//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    data: [result.raw.yvalue[0]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'生铁',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 1,
                    data:[result.raw.yvalue[1]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'废钢总和',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 2,
                    data:[result.raw.yvalue[2]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'大渣钢',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 3,
                    data:[result.raw.yvalue[3]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'自产废钢',
                    type:'bar',
                   barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 4,
                    data:[result.raw.yvalue[4]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'重型废钢',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 5,
                    data:[result.raw.yvalue[5]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'中型废钢',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 6,
                    data:[result.raw.yvalue[6]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                }
                ]
            };

            var ecConfig = echarts.config;
            myChart.on('click', function (params) {
            if (typeof params.seriesIndex != 'undefined') {
                //mes += '  seriesIndex : ' + param.seriesIndex;
                //mes += '  dataIndex : ' + param.dataIndex+result.xEnglishname[param.dataIndex];
                fieldname_chinese=result.raw.xname[params.seriesIndex];
                fieldname_english=result.raw.xEnglishname[params.seriesIndex];
                // str_select=result.raw.str_select;
                probability_normal(fieldname_chinese,fieldname_english,result.raw.offset_result[params.seriesIndex],params.value,str_select);
                $("#hidden_inform1").val(fieldname_english);//字段英文名
                $("#hidden_inform2").val(fieldname_chinese);//字段中文名
                $("#hidden_inform3").val(params.value);//实际值
                $("#hidden_inform4").val(result.raw.offset_result[params.seriesIndex]);//偏离程度
            }
            console.log(params);
            });

            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    // 条形图（物料material）(多Y轴直方图)
    function drawBarChart_material(heat_no,str_select,result){
        // var myChart = echarts.init(document.getElementById('main2'));
        var myChart = echarts.getInstanceByDom(document.getElementById('main2'));
        myChart.clear();
        // var colors = ['#5793f3', '#d14a61', '#675bba','#00c957','#5793f3', '#d14a61', '#675bba','#00c957'];
        // var colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF','#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF'];
        // var colors = ['#FCBE91','#AB837D','#E6DD86','#BCA997','#ADC8C8','#9D947E','#AE8083','#9C8987','#807455','#DEC87B','#C3B7BB'];
         var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
        var barWidth_value=40;
        var barGap_value='100%';
        var barCategoryGap_value='60%';

            // 指定图表的配置项和数据
            var option = {
                color:colors,
                title: {
                    text: '炉次号'+heat_no+'的物料组成',
                    x:'center'
                },
                tooltip: {
                    // trigger: 'axis',
                    // axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    //     type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        trigger:'item',
                        formatter: function (params){
                            var res = result.material.xname[params.seriesIndex]+':</br>实际值：'+params.value+result.material.danwei[params.seriesIndex] + '<br/>偏离程度：'+result.material.offset_result[params.seriesIndex]+'</br>定性判断：'+result.material.qualitative_offset_result[params.seriesIndex];
                            return res;

                     }
                },
                toolbox: {
                    show : true,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['']
                },
                xAxis: {
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: ['单炉次物料投入字段']
                },
                yAxis: [{
                    type: 'value',
                    name: '总吹氧消耗(NM3)',
                    // min: 0,
                    // max: 105000,
                    position: 'left',
                    offset:20,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[0]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '氮气耗量(NM3)',
                    // min: 0,
                    // max: 12000,
                    position: 'left',
                    offset: -60,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[1]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} NM3'
                    // }
                },
                {
                    type: 'value',
                    name: '1#烧结矿(Kg)',
                    min: 0,
                    max: 8000,
                    position: 'left',
                    splitLine:{show: false},//去除网格线
                    offset: -140,
                    axisLine: {
                        lineStyle: {
                            color: colors[2]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '石灰石(Kg)',
                    min: 0,
                    max: 8000,
                    position: 'left',
                    offset: -220,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[3]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '萤石(Kg)',
                    min: 0,
                    max: 8000,
                    position: 'left',
                    offset: -300,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[4]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '增碳剂(Kg)',
                    min: 0,
                    max: 8000,
                    position: 'left',
                    offset: -380,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[5]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '低氮增碳剂(Kg)',
                    min: 0,
                    max: 8000,
                    position: 'left',
                    offset: -460,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[6]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '石灰(Kg)',
                    min: 0,
                    max: 8000,
                    position: 'left',
                    offset: -540,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[7]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '轻烧白云石(Kg)',
                    min: 0,
                    max: 8000,
                    position: 'left',
                    offset: -620,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[8]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                }
                ],
                series: [{
                    name: '总吹氧消耗',
                    type: 'bar',
                    barWidth : barWidth_value,//柱条（K线蜡烛）宽度
                    barGap: barGap_value,//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap: barCategoryGap_value,//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    data: [result.material.yvalue[0]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'氮气耗量',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 1,
                    data:[result.material.yvalue[1]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'1#烧结矿',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 2,
                    data:[result.material.yvalue[2]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'石灰石',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 3,
                    data:[result.material.yvalue[3]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'萤石',
                    type:'bar',
                   barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 4,
                    data:[result.material.yvalue[4]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'增碳剂',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 5,
                    data:[result.material.yvalue[5]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'低氮增碳剂',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 6,
                    data:[result.material.yvalue[6]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'石灰',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 7,
                    data:[result.material.yvalue[7]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'轻烧白云石',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 8,
                    data:[result.material.yvalue[8]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                }
                ]
            };

            var ecConfig = echarts.config;
            myChart.on('click', function (params) {
            if (typeof params.seriesIndex != 'undefined') {
                //mes += '  seriesIndex : ' + param.seriesIndex;
                //mes += '  dataIndex : ' + param.dataIndex+result.xEnglishname[param.dataIndex];
                fieldname_chinese=result.material.xname[params.seriesIndex];
                fieldname_english=result.material.xEnglishname[params.seriesIndex];
                // str_select=result.material.str_select;
                probability_normal(fieldname_chinese,fieldname_english,result.material.offset_result[params.seriesIndex],params.value,str_select);
                $("#hidden_inform1").val(fieldname_english);//字段英文名
                $("#hidden_inform2").val(fieldname_chinese);//字段中文名
                $("#hidden_inform3").val(params.value);//实际值
                $("#hidden_inform4").val(result.material.offset_result[params.seriesIndex]);//偏离程度
            }
            console.log(params);
            });

            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    // 条形图（产品product）（多Y轴直方图）
    function drawBarChart_product(heat_no,str_select,result){
        // var myChart = echarts.init(document.getElementById('main3'));
        var myChart = echarts.getInstanceByDom(document.getElementById('main3'));
        myChart.clear();
        // var colors = ['#5793f3', '#d14a61', '#675bba','#00c957','#5793f3', '#d14a61', '#675bba','#00c957'];
        // var colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF','#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF'];
        var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
        var barWidth_value=60;
        var barGap_value='100%';
        var barCategoryGap_value='60%';
            // 指定图表的配置项和数据
            var option = {
                color:colors,
                title: {
                    text: '炉次号'+heat_no+'的产品组成',
                    x:'center'
                },
                tooltip: {
                    // trigger: 'axis',
                    // axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    //     type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        trigger:'item',
                        formatter: function (params){
                            var res = result.product.xname[params.seriesIndex]+':</br>实际值：'+params.value+result.product.danwei[params.seriesIndex] + '<br/>偏离程度：'+result.product.offset_result[params.seriesIndex]+'</br>定性判断：'+result.product.qualitative_offset_result[params.seriesIndex];
                            return res;

                     }
                },
                toolbox: {
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['']
                },
                xAxis: {
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: ['单炉次产品产出字段']
                },
                yAxis: [{
                    type: 'value',
                    name: '钢水(Kg)',
                    min: 0,
                    max: 105000,
                    position: 'left',
                    offset:-130,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[0]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '转炉煤气(NM3)',
                    min: 0,
                    max: 12000,
                    position: 'left',
                    offset: -250,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[1]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} NM3'
                    // }
                },
                {
                    type: 'value',
                    name: '钢渣(Kg)',
                    min: 0,
                    max: 22000,
                    position: 'left',
                    splitLine:{show: false},//去除网格线
                    offset: -370,
                    axisLine: {
                        lineStyle: {
                            color: colors[2]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                }
                ],
                series: [{
                    name: '钢水重量',
                    type: 'bar',
                    barWidth : barWidth_value,//柱条（K线蜡烛）宽度
                    barGap: barGap_value,//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:barCategoryGap_value,//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    data: [result.product.yvalue[0]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'转炉煤气',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 1,
                    data:[result.product.yvalue[1]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'钢渣',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 2,
                    data:[result.product.yvalue[2]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                }
                ]
            };

            var ecConfig = echarts.config;
            // alert('test1');
            myChart.on('click', function (params) {
                // alert('test4');
                if (typeof params.seriesIndex != 'undefined') {
                    // alert(params.seriesIndex);
                    //mes += '  seriesIndex : ' + param.seriesIndex;
                    //mes += '  dataIndex : ' + param.dataIndex+result.xEnglishname[param.dataIndex];
                    fieldname_chinese=result.product.xname[params.seriesIndex];
                    fieldname_english=result.product.xEnglishname[params.seriesIndex];
                    // str_select=result.product.str_select;
                    // alert("test2");
                    probability_normal(fieldname_chinese,fieldname_english,result.product.offset_result[params.seriesIndex],params.value,str_select);
                    $("#hidden_inform1").val(fieldname_english);//字段英文名
                    $("#hidden_inform2").val(fieldname_chinese);//字段中文名
                    $("#hidden_inform3").val(params.value);//实际值
                    $("#hidden_inform4").val(result.product.offset_result[params.seriesIndex]);//偏离程度
                    // alert($("#hidden_inform4").val());
                }
                console.log(params);
            });

            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    // 条形图（合金alloy）(多Y轴直方图)
    function drawBarChart_alloy(heat_no,str_select,result){
        // var myChart = echarts.init(document.getElementById('main4'));
        var myChart = echarts.getInstanceByDom(document.getElementById('main4'));
        myChart.clear();
        // var colors = ['#5793f3', '#d14a61', '#675bba','#00c957','#5793f3', '#d14a61', '#675bba','#00c957'];
        // var colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF','#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF'];
        var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
        var barWidth_value=40;
        var barGap_value='100%';
        var barCategoryGap_value='60%';

            // 指定图表的配置项和数据
            var option = {
                color:colors,
                title: {
                    text: '炉次号'+heat_no+'的合金组成',
                    x:'center'
                },
                tooltip: {
                    // trigger: 'axis',
                    // axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    //     type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        trigger:'item',
                        formatter: function (params){
                            var res = result.alloy.xname[params.seriesIndex]+':</br>实际值：'+params.value+result.alloy.danwei[params.seriesIndex] + '<br/>偏离程度：'+result.alloy.offset_result[params.seriesIndex]+'</br>定性判断：'+result.alloy.qualitative_offset_result[params.seriesIndex];
                            return res;

                     }
                },
                toolbox: {
                    show : true,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['']
                },
                xAxis: {
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: ['单炉次合金投入字段']
                },
                yAxis: [{
                    type: 'value',
                    name: '硅铁(Kg)',
                    min: 0,
                    max: 5000,
                    position: 'left',
                    offset:-140,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[0]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '微铝硅铁(Kg)',
                    min: 0,
                    max: 5000,
                    position: 'left',
                    offset: -220,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[1]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} NM3'
                    // }
                },
                {
                    type: 'value',
                    name: '硅锰合金(Kg)',
                    min: 0,
                    max: 5000,
                    position: 'left',
                    splitLine:{show: false},//去除网格线
                    offset: -300,
                    axisLine: {
                        lineStyle: {
                            color: colors[2]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '高硅硅锰(Kg)',
                    min: 0,
                    max: 5000,
                    position: 'left',
                    offset: -380,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[3]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: '中碳铬铁(Kg)',
                    min: 0,
                    max: 5000,
                    position: 'left',
                    offset: -460,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[4]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                }
                ],
                series: [{
                    name: '硅铁',
                    type: 'bar',
                    barWidth : barWidth_value,//柱条（K线蜡烛）宽度
                    barGap: barGap_value,//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap: barCategoryGap_value,//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    data: [result.alloy.yvalue[0]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'微铝硅铁',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 1,
                    data:[result.alloy.yvalue[1]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'硅锰合金',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 2,
                    data:[result.alloy.yvalue[2]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'高硅硅锰',
                    type:'bar',
                    barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 3,
                    data:[result.alloy.yvalue[3]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'中碳铬铁',
                    type:'bar',
                   barWidth : barWidth_value,
                    barGap: barGap_value,
                    barCategoryGap: barCategoryGap_value,
                    barMinHeight:10,
                    yAxisIndex: 4,
                    data:[result.alloy.yvalue[4]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                }
                ]
            };

            var ecConfig = echarts.config;
            myChart.on('click', function (params) {
            if (typeof params.seriesIndex != 'undefined') {
                //mes += '  seriesIndex : ' + param.seriesIndex;
                //mes += '  dataIndex : ' + param.dataIndex+result.xEnglishname[param.dataIndex];
                fieldname_chinese=result.alloy.xname[params.seriesIndex];
                fieldname_english=result.alloy.xEnglishname[params.seriesIndex];
                // str_select=result.alloy.str_select;
                probability_normal(fieldname_chinese,fieldname_english,result.alloy.offset_result[params.seriesIndex],params.value,str_select);
                $("#hidden_inform1").val(fieldname_english);//字段英文名
                $("#hidden_inform2").val(fieldname_chinese);//字段中文名
                $("#hidden_inform3").val(params.value);//实际值
                $("#hidden_inform4").val(result.alloy.offset_result[params.seriesIndex]);//偏离程度
            }
            console.log(params);
            });

            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    // 雷达图（合）
    function drawRadarMap(heat_no,result,classification_index,area){
        // var myChart = echarts.init(document.getElementById('main4'));
        var myChart = echarts.getInstanceByDom(document.getElementById(area));
        myChart.clear();
        var classification_ch = ['原料','物料','产品','合金'];
        var classification_en = ['raw','material','product','alloy'];
        var classification_ch_single=classification_ch[classification_index];
        var classification_en_single=classification_en[classification_index];
        var option = {
            title: {
                text: '炉次'+heat_no+'【'+classification_ch_single+'】组成',
                // x: 'center'
            },
            tooltip: {},
            legend: {
                data: ['炉次实际值', '上范围','下范围']
            },
            radar: {
                // shape: 'circle',
                name: {
                    formatter:'{value}',
                    textStyle: {
                        color: '#000',
                        backgroundColor: '#999',
                        borderRadius: 3,
                        padding: [3, 5],
                        
                   }
                },
                indicator: (function (){
                    var res = [];
                    var fieldname = result[classification_en_single].xname;
                    for(var i=0;i<fieldname.length;i++){
                        res.push({
                            name: fieldname[i], max:result[classification_en_single].updesired[i]*1.2
                        });
                    };
                    
                    return res;
                })()

            },
            series: [{
                name: '实际值 vs 正常范围',
                type: 'radar',
                // areaStyle: {normal: {}},
                data : [
                    {
                        value : result[classification_en_single].yvalue,
                        name : '炉次实际值',
                        label: {
                            normal: {
                                show: true,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    },
                     {
                        value : result[classification_en_single].updesired,
                        name : '上范围',
                        label: {
                            normal: {
                                show: false,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    },
                    {
                        value : result[classification_en_single].downdesired,
                        name : '下范围',
                        label: {
                            normal: {
                                show: false,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    }
                ]
            }]
        };
         var ecConfig = echarts.config;
         myChart.setOption(option,true);
    }

//单炉次质量分析：------------------
    // 条形图（含量）(多Y轴直方图)
    function drawBarChart_quality(result){
        var myChart = echarts.getInstanceByDom(document.getElementById('main1'));
        myChart.clear();
        // var colors = ['#5793f3', '#d14a61', '#675bba','#00c957','#e02222', '#2367d9','#f39646','#e02222'];
        // var colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF','#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF'];
        var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
            // 指定图表的配置项和数据
            var option = {
                color:colors,
                title: {
                    text: '炉次号'+result.heat_no+'的钢水含量组成',
                    x:'center'
                },
                tooltip: {
                    // trigger: 'axis',
                    // axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    //     type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        trigger:'item',
                        formatter: function (params){
                            var res = result.xname[params.seriesIndex]+':</br>实际值：'+params.value+ '<br/>偏离程度：'+result.offset_result[params.seriesIndex]+'</br>定性判断：'+result.qualitative_offset_result[params.seriesIndex];
                            return res;

                     }
                },
                toolbox: {
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['']
                },
                xAxis: {
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: ['单炉次字段']
                },
                yAxis: [{
                    type: 'value',
                    name: 'C',
                    min: 0,
                    max: 0.9905,
                    position: 'left',
                    offset:-40,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[0]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: 'SI',
                    min: 0,
                    max: 0.4200,
                    position: 'left',
                    offset: -200,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[1]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} NM3'
                    // }
                },
                {
                    type: 'value',
                    name: 'MN',
                    min: 0,
                    max: 0.8970,
                    position: 'left',
                    splitLine:{show: false},//去除网格线
                    offset: -360,
                    axisLine: {
                        lineStyle: {
                            color: colors[2]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
                {
                    type: 'value',
                    name: 'P',
                    min: 0,
                    max: 0.0180,
                    position: 'left',
                    offset: -520,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[3]
                        }
                    },
                },
                {
                    type: 'value',
                    name: 'S',
                    min: 0,
                    max: 0.0180,
                    position: 'left',
                    offset: -680,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[4]
                        }
                    },
                },
                {
                    type: 'value',
                    name: '重量',
                    min: 0,
                    max: 113000,
                    position: 'left',
                    offset: -840,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[5]
                        }
                    },
                },
                {
                    type: 'value',
                    name: '温度',
                    min: 1000,
                    max: 2000,
                    position: 'left',
                    offset: -1000,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[6]
                        }
                    },
                },
                ],
                series: [{
                    name: 'C',
                    type: 'bar',
                    barWidth : 80,//柱条（K线蜡烛）宽度
                    barGap: '100%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'60%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    data: [result.yvalue[0]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'SI',
                    type:'bar',
                    barWidth : 80,
                    barGap: '100%',
                    barCategoryGap:'60%',
                    barMinHeight:10,
                    yAxisIndex: 1,
                    data:[result.yvalue[1]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'MN',
                    type:'bar',
                    barWidth : 80,
                    barGap: '100%',
                    barCategoryGap:'60%',
                    barMinHeight:10,
                    yAxisIndex: 2,
                    data:[result.yvalue[2]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'P',
                    type:'bar',
                    barWidth : 80,
                    barGap: '100%',
                    barCategoryGap:'60%',
                    barMinHeight:10,
                    yAxisIndex: 3,
                    data:[result.yvalue[3]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'S',
                    type:'bar',
                    barWidth : 80,
                    barGap: '100%',
                    barCategoryGap:'60%',
                    barMinHeight:10,
                    yAxisIndex: 4,
                    data:[result.yvalue[4]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'重量',
                    type:'bar',
                    barWidth : 80,
                    barGap: '100%',
                    barCategoryGap:'60%',
                    barMinHeight:10,
                    yAxisIndex: 5,
                    data:[result.yvalue[5]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                {
                    name:'温度',
                    type:'bar',
                    barWidth : 80,
                    barGap: '100%',
                    barCategoryGap:'60%',
                    barMinHeight:10,
                    yAxisIndex: 6,
                    data:[result.yvalue[6]],
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    }
                },
                ]
            };

            var ecConfig = echarts.config;
            myChart.on('click', function (params) {
            if (typeof params.seriesIndex != 'undefined') {
                //mes += '  seriesIndex : ' + param.seriesIndex;
                //mes += '  dataIndex : ' + param.dataIndex+result.xEnglishname[param.dataIndex];
                fieldname_chinese=result.xname[params.seriesIndex];
                fieldname_english=result.xEnglishname[params.seriesIndex];
                probability_normal(fieldname_chinese,fieldname_english,result.offset_result[params.seriesIndex],params.value,result.str_select);

                $("#hidden_inform1").val(fieldname_english);//字段英文名
                $("#hidden_inform2").val(fieldname_chinese);//字段中文名
                $("#hidden_inform3").val(params.value);//实际值
                $("#hidden_inform4").val(result.offset_result[params.seriesIndex]);//偏离程度
                            }
            console.log(params);
            });

            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    // 雷达图
    function drawRadarMap_quality(result){
        // var myChart = echarts.init(document.getElementById('main4'));
        var myChart = echarts.getInstanceByDom(document.getElementById('main1'));
        myChart.clear();

        var option = {
            title: {
                text: '炉次'+result.heat_no+'【质量】分析',
                // x: 'center'
            },
            tooltip: {},
            legend: {
                data: ['炉次实际值', '上范围','下范围']
            },
            radar: {
                // shape: 'circle',
                name: {
                    formatter:'{value}',
                    textStyle: {
                        color: '#000',
                        backgroundColor: '#999',
                        borderRadius: 3,
                        padding: [3, 5],
                        
                   }
                },
                indicator: (function (){
                    var res = [];
                    var fieldname = result.xname;
                    for(var i=0;i<fieldname.length;i++){
                        res.push({
                            name: fieldname[i], max:result.updesired[i]*1.2
                        });
                    };
                    
                    return res;
                })()

            },
            series: [{
                name: '实际值 vs 正常范围',
                type: 'radar',
                // areaStyle: {normal: {}},
                data : [
                    {
                        value : result.yvalue,
                        name : '炉次实际值',
                        label: {
                            normal: {
                                show: true,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    },
                     {
                        value : result.updesired,
                        name : '上范围',
                        label: {
                            normal: {
                                show: false,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    },
                    {
                        value : result.downdesired,
                        name : '下范围',
                        label: {
                            normal: {
                                show: false,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    }
                ]
            }]
        };
         var ecConfig = echarts.config;
         myChart.setOption(option,true);
    }

//单炉次分布图：------------------
    // 正态分布+概率分布画图
    function probability_normal_picture(result){
        // var myChart = echarts.init(document.getElementById('main5'));
        // alert("enter probability_normal_picture");
        var myChart = echarts.getInstanceByDom(document.getElementById('main5'));
        // var myChart = echarts.getOption(document.getElementById('main5'));
        myChart.clear();
        //var bookname=document.getElementById('bookno1')
            // 指定图表的配置项和数据
            var option = {
                title: {
                    // text: result.base_result.fieldname_chinese+'('+result.base_result.fieldname+')的概率(bar)及正态(line)分布',
                    text: result.base_result.fieldname_chinese+'的分布图',
                    x:'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                     }
                },
                legend: {
                    data:['']
                },
                toolbox: {
                    show : true,
                    feature : {
                        dataView : {show: true, readOnly: false},
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                xAxis: [
                    {
                        data: result.ana_result.normx,
                        axisLabel :{
                                //interval:0,//横轴信息全部显示
                                //rotate: 60//60度角倾斜显示
                            }
                    },
                    {
                        type : 'category',
                        // axisLine: {show:true},
                        // axisTick: {show:true},
                        // axisLabel: {show:true},
                        // splitArea: {show:true},
                        // splitLine: {show:true},
                        data : result.ana_result.scope,
                        show:false,
                    }
                ],
                yAxis: [{
                    name:'正态分布密度(line)'
                },
                {
                    name:'概率分布密度(bar)'
                }
                ],
                series: [{
                    name: '正态分布',
                    type: 'line',
                    xAxisIndex:0,
                    yAxisIndex:0,
                    data: result.ana_result.normy,
                    // markPoint: {
                    //     itemStyle : {
                    //          normal: {
                    //              color:'#1e90ff'
                    //          }
                    //      },
                    //     data:[
                    //             // {type : 'max', name: '最大值'},
                    //             // {type : 'min', name: '最小值'},
                    //             {name : '位置点偏离程度'+result.normal_result.offset_value, value : result.normal_result.actual_value, xAxis: result.normal_result.match_value, yAxis: result.normal_result.normy[result.normal_result.match_index]},
                    //     ]
                    // },
                    markLine: {
                        name:'炉次号'+result.base_result.fieldname+'的标线',
                        itemStyle : {
                            normal: {
                                color:'#1e90ff'
                            }
                        },
                        data:[
                                [
                                {name: '位置点偏离程度'+result.base_result.offset_value, value:  result.base_result.actual_value, xAxis: result.base_result.match_value, yAxis: 0},
                                {name: '标线1终点', xAxis: result.base_result.match_value, yAxis: 'max'}
                                ],
                                [{
                                    // 固定起点的 x 位置，用于模拟一条指向最大值的水平线
                                    name: '位置点偏离程度'+result.base_result.offset_value,
                                    value: result.base_result.offset_value,
                                    yAxis: 'max',
                                    xAxis: result.base_result.match_value
                                 },
                                 {
                                    type: 'max'
                                }],
                               ]

                    },
                    // itemStyle: {
                    //         normal: {
                    //         color: 'tomato',
                    //         // label : {
                    //         //     show: false, position: 'top'
                    //         // }
                    //     }
                    // }

                },
                  {
                    name: '概率分布',
                    type: 'bar',
                    xAxisIndex:1,//xAxis坐标轴数组的索引，指定该系列数据所用的横坐标轴
                    yAxisIndex:1,
                    data: result.ana_result.num,
                    // itemStyle: {
                    //     normal: {
                    //     color: '#675bba',
                    //     }
                    // }
                }
                ]

            };

        var ecConfig = echarts.config;
        // myChart.on('click', function (params) {
        //     // if (params.componentType == 'markPoint') {
        //         //mes += '  seriesIndex : ' + param.seriesIndex;
        //         //mes += '  dataIndex : ' + param.dataIndex+result.xEnglishname[param.dataIndex];
        //         offset_value=result.base_result.offset_value;//读取偏离值
        //         fieldname_english=result.base_result.fieldname;//读取字段英文名字
        //         retrospectfactor(fieldname_english,fieldname_chinese,offset_value);
        //     // }
        //     console.log(params);
        //     });

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option,true);
    }

//多炉次成本分析：------------------
    //条形图
    function drawBarChart_fluc(result,classification_index,area){
        var myChart = echarts.getInstanceByDom(document.getElementById(area));
        myChart.clear();
        // var colors = ['#5793f3', '#d14a61', '#675bba','#00c957','#eeeeee', '#3397c9','#f39646','#e02222','#e0442f'];
        // var colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF','#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#8B00FF'];
        var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
        var classification_ch = ['原料','物料','产品','合金'];
        var classification_ch_single=classification_ch[classification_index];
        var classification=result.field_classification[classification_index];//classification_index 字段分类的索引
        // alert(result.result[classification].condition);
        if (result.result[classification].condition=='NoData'){
            document.getElementById(area).innerHTML = classification_ch[classification_index]+"字段缺少数据，无法进行图表展示！详情请见成本分析结果.";
            return;
        }
            // 指定图表的配置项和数据
            var option = {
                color:colors,
                title: {
                    text: '转炉工序【'+classification_ch_single+'】字段波动率',
                    subtext: result.time.time1+'~'+result.time.time2+' || '+result.time.history_time1+'~'+result.time.history_time2+'时间范围内的波动率对比',
                    // subtext: '当前时间范围：'+result.time.time1+'~'+result.time.time2+'\n历史时间范围：'+result.time.history_time1+'~'+result.time.history_time2,
                    x:'center'
                },
                tooltip: {
                        trigger:'item',
                        formatter: function (params){//result.result.raw.fieldname_ch[params.dataIndex]
                            var res = result.result[classification].fieldname_ch[params.dataIndex]+'<br/>'+params.seriesName+'：'+params.value+ '<br/>偏离程度：'+result.result[classification].offset_result_cent[params.dataIndex]+'</br>定性判断：'+result.result[classification].qualitative_offset_result[params.dataIndex];        
                            // var res = result.fieldname_ch[params.seriesIndex]+':</br>波动率实际值：'+params.value+'</br>波动率历史值：'+result.ana_describe_history[params.seriesIndex].numb[2]+ '<br/>偏离程度：'+result.offset_result[params.seriesIndex]+'</br>定性判断：'+result.qualitative_offset_result[params.seriesIndex];                         
                            return res;
                            }
                     
                },
                toolbox: {
                    show : true,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['波动率','对比历史波动率'],
                    show:false
                },
                xAxis: [{
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: result.result[classification].fieldname_ch,
                },
                ],
                yAxis: [{
                    name:'波动率',
                    type: 'value',
                    // min: 0,
                    // max: 105000,
                    position: 'left',
                    offset:0,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[0]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
               
                ],
                series: [{
                    name:'波动率',
                    type: 'bar',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result[classification].fluc_ratio,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                            color:function(params) {
                                return colors[params.dataIndex]
                            }
                        }
                    }
                },
                {
                    name:'对比历史波动率',
                    type: 'bar',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result[classification].fluc_ratio_history,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                            color: function(params) {
                                return colors[params.dataIndex]
                        }
                    }
                }
                },
                
                ]
            };

            var ecConfig = echarts.config;

            // myChart.on('click', function (params) {
            // alert("ttttt");
            // if (typeof params.seriesIndex != 'undefined') { 
            //     // fieldname_chinese=result.fieldname_ch[params.seriesIndex];
            //     // fieldname_english=result.fieldname_en[params.seriesIndex];
            //     // probability_distribution(fieldname_chinese,fieldname_english,result.offset_result[params.seriesIndex],params.value);

            //     // fieldname_en=result.fieldname_en[params.dataIndex];//读取字段英文名字
            //     index=params.dataIndex;//index表示分类中的第几个字段
            //     alert("index");
            //     retrospectfactor(result,classification,index);
            // }
            // console.log(params);
            // });


            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    //折线图
    function drawLineChart_fluc(result,classification_index,area){
        var myChart = echarts.getInstanceByDom(document.getElementById(area));
        myChart.clear();
        // var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
        var classification_ch = ['原料','物料','产品','合金'];
        var classification_ch_single=classification_ch[classification_index];
        var classification=result.field_classification[classification_index];//classification_index 字段分类的索引

        if (result.result[classification].condition=='NoData'){
            document.getElementById(area).innerHTML = classification_ch[classification_index]+"字段缺少数据，无法进行图表展示！详情请见成本分析结果.";
            return;
        }
            // 指定图表的配置项和数据
            var option = {
                // color:colors,
                title: {
                    text: '转炉工序【'+classification_ch_single+'】字段波动率',
                    subtext: result.time.time1+'~'+result.time.time2+' || '+result.time.history_time1+'~'+result.time.history_time2+'时间范围内的波动率对比',
                    // subtext: '当前时间范围：'+result.time.time1+'~'+result.time.time2+'\n历史时间范围：'+result.time.history_time1+'~'+result.time.history_time2,
                    x:'center'
                },
                tooltip: {
                        trigger:'item',
                        formatter: function (params){//result.result.raw.fieldname_ch[params.dataIndex]
                            var res = result.result[classification].fieldname_ch[params.dataIndex]+'<br/>'+params.seriesName+'：'+params.value+ '<br/>偏离程度：'+result.result[classification].offset_result_cent[params.dataIndex]+'</br>定性判断：'+result.result[classification].qualitative_offset_result[params.dataIndex];        
                            // var res = result.fieldname_ch[params.seriesIndex]+':</br>波动率实际值：'+params.value+'</br>波动率历史值：'+result.ana_describe_history[params.seriesIndex].numb[2]+ '<br/>偏离程度：'+result.offset_result[params.seriesIndex]+'</br>定性判断：'+result.qualitative_offset_result[params.seriesIndex];                         
                            return res;
                            }
                     
                },
                toolbox: {
                    show : false,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['波动率','对比历史波动率'],
                    show:true,
                    right:10,
                },
                xAxis: [{
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: result.result[classification].fieldname_ch,
                },
                ],
                yAxis: [{
                    name:'波动率',
                    type: 'value',
                    // min: 0,
                    // max: 105000,
                    position: 'left',
                    offset:0,
                    splitLine:{show: false},//去除网格线
                    // axisLine: {
                    //     lineStyle: {
                    //         color: colors[0]
                    //     }
                    // },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
               
                ],
                series: [{
                    name:'波动率',
                    type: 'line',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result[classification].fluc_ratio,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                            // color:function(params) {
                            //     return colors[params.dataIndex]
                            // }
                        }
                    }
                },
                {
                    name:'对比历史波动率',
                    type: 'line',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result[classification].fluc_ratio_history,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                        //     color: function(params) {
                        //         return colors[params.dataIndex]
                        // }
                    }
                }
                },
                
                ]
            };

            var ecConfig = echarts.config;
            // myChart.on('click', function (params) {
            // if (typeof params.seriesIndex != 'undefined') { 
            //     // fieldname_chinese=result.fieldname_ch[params.seriesIndex];
            //     // fieldname_english=result.fieldname_en[params.seriesIndex];
            //     // probability_distribution(fieldname_chinese,fieldname_english,result.offset_result[params.seriesIndex],params.value);

            //     // fieldname_en=result.fieldname_en[params.dataIndex];//读取字段英文名字
            //     index=params.dataIndex;//index表示分类中的第几个字段
            //     retrospectfactor(result,classification,index);
            // }
            // console.log(params);
            // });


            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    //雷达图
    function drawRadarMap_fluc(result,classification_index,area){
        var myChart = echarts.getInstanceByDom(document.getElementById(area));
        myChart.clear();
        var classification_ch = ['原料','物料','产品','合金'];
        var classification_ch_single=classification_ch[classification_index];
        var classification=result.field_classification[classification_index];//classification_index 字段分类的索引
        // alert(result.result[classification].condition);
        if (result.result[classification].condition=='NoData'){
            document.getElementById(area).innerHTML = classification_ch[classification_index]+"字段缺少数据，无法进行图表展示！详情请见成本分析结果.";
            return;
        }

        var option = {
            title: {
                text: '转炉工序【'+classification_ch_single+'】字段波动率',
                subtext: result.time.time1+'~'+result.time.time2+' || '+result.time.history_time1+'~'+result.time.history_time2,
                // subtext: '当前时间范围：'+result.time.time1+'~'+result.time.time2+'\n历史时间范围：'+result.time.history_time1+'~'+result.time.history_time2,
                // x:'center'
            },
            tooltip: {},
            legend: {
                data: ['当前波动率', '历史波动率'],
                right:10,
            },
            radar: {
                // shape: 'circle',
                name: {
                    formatter:'{value}',
                    textStyle: {
                        color: '#000',
                        backgroundColor: '#999',
                        borderRadius: 3,
                        padding: [3, 5],
                        
                   }
                },
                indicator: (function (){
                    var res = [];
                    var len = 0;
                    var fieldname = result.result[classification].fieldname_ch;
                    for(var i=0;i<fieldname.length;i++){
                        res.push({
                            name: fieldname[i],max:result.result[classification].fluc_ratio_history[i]*1.2
                        });
                    };
                    
                    return res;
                })()
 

            },

            series: [{
                name: '当前波动率 vs 历史波动率',
                type: 'radar',
                // areaStyle: {normal: {}},
                data : [
                    {
                        // value : result.material.yvalue,
                        value : result.result[classification].fluc_ratio,
                        name : '当前波动率',
                        label: {
                            normal: {
                                show: true,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    },
                     {
                        // value : result.material.yvalue,
                        value : result.result[classification].fluc_ratio_history,
                        name : '历史波动率',
                        label: {
                            normal: {
                                show: true,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    }
                ]
            }]
        };
        // var ecConfig = echarts.config;
        myChart.setOption(option,true);
    };

//多炉次质量分析：------------------

    //条形图
    function drawBarChart_qualityfluc(result,area){
        var myChart = echarts.getInstanceByDom(document.getElementById(area));
        myChart.clear();
        // var colors = ['#5793f3', '#d14a61', '#675bba','#00c957','#eeeeee', '#3397c9','#f39646','#e02222','#e0442f'];
        var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];
        if (result.condition=='NoData'){
            document.getElementById(area).innerHTML = "质量相关字段缺少数据，无法进行图表展示！详情请见成本分析结果.";
            return;
        }
            // 指定图表的配置项和数据
            var option = {
                color:colors,
                title: {
                    text: '转炉工序【质量】字段波动率计算',
                    subtext: result.time.time1+'~'+result.time.time2+' || '+result.time.history_time1+'~'+result.time.history_time2+'时间范围内的波动率对比',
                    // subtext: '当前时间范围：'+result.time.time1+'~'+result.time.time2+'\n历史时间范围：'+result.time.history_time1+'~'+result.time.history_time2,
                    x:'center'
                },
                tooltip: {
                        trigger:'item',
                        formatter: function (params){//result.result.raw.fieldname_ch[params.dataIndex]
                            var res = result.result.fieldname_ch[params.dataIndex]+'<br/>'+params.seriesName+'：'+params.value+ '<br/>偏离程度：'+result.result.offset_result_cent[params.dataIndex]+'</br>定性判断：'+result.result.qualitative_offset_result[params.dataIndex];
                            // var res = result.fieldname_ch[params.seriesIndex]+':</br>波动率实际值：'+params.value+'</br>波动率历史值：'+result.ana_describe_history[params.seriesIndex].numb[2]+ '<br/>偏离程度：'+result.offset_result[params.seriesIndex]+'</br>定性判断：'+result.qualitative_offset_result[params.seriesIndex];
                            return res;
                            }

                },
                toolbox: {
                    show : true,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['波动率','对比历史波动率'],
                    show:false
                },
                xAxis: [{
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: result.result.fieldname_ch,
                },
                ],
                yAxis: [{
                    name:'波动率',
                    type: 'value',
                    // min: 0,
                    // max: 105000,
                    position: 'left',
                    offset:0,
                    splitLine:{show: false},//去除网格线
                    axisLine: {
                        lineStyle: {
                            color: colors[0]
                        }
                    },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },

                ],
                series: [{
                    name:'波动率',
                    type: 'bar',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result.fluc_ratio,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                            color:function(params) {
                                return colors[params.dataIndex]
                            }
                        }
                    }
                },
                {
                    name:'对比历史波动率',
                    type: 'bar',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result.fluc_ratio_history,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                            color: function(params) {
                                return colors[params.dataIndex]
                        }
                    }
                }
                },

                ]
            };

            var ecConfig = echarts.config;
            // myChart.on('click', function (params) {
            // if (typeof params.seriesIndex != 'undefined') {
            //     // fieldname_chinese=result.fieldname_ch[params.seriesIndex];
            //     // fieldname_english=result.fieldname_en[params.seriesIndex];
            //     // probability_distribution(fieldname_chinese,fieldname_english,result.offset_result[params.seriesIndex],params.value);

            //     // fieldname_en=result.fieldname_en[params.dataIndex];//读取字段英文名字
            //     index=params.dataIndex;//index表示分类中的第几个字段
            //     retrospectfactor(result,index);
            // }
            // console.log(params);
            // });


            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    //折线图
    function drawLineChart_qualityfluc(result,area){
        var myChart = echarts.getInstanceByDom(document.getElementById(area));
        myChart.clear();
        // var colors = ['#FCBE91','#ACA7DC','#FFBF32','#BC8F8F','#DC6428','#7DB8CB','#9400D3','#AE8083','#808080','#3E8DC6','#9D947E'];

        if (result.condition=='NoData'){
            document.getElementById(area).innerHTML = "质量字段缺少数据，无法进行图表展示！详情请见成本分析结果.";
            return;
        }
            // 指定图表的配置项和数据
            var option = {
                // color:colors,
                title: {
                    text: '转炉工序【质量】字段波动率',
                    subtext: result.time.time1+'~'+result.time.time2+' || '+result.time.history_time1+'~'+result.time.history_time2+'时间范围内的波动率对比',
                    // subtext: '当前时间范围：'+result.time.time1+'~'+result.time.time2+'\n历史时间范围：'+result.time.history_time1+'~'+result.time.history_time2,
                    x:'center'
                },
                tooltip: {
                        trigger:'item',
                        formatter: function (params){//result.result.raw.fieldname_ch[params.dataIndex]
                            var res = result.result.fieldname_ch[params.dataIndex]+'<br/>'+params.seriesName+'：'+params.value+ '<br/>偏离程度：'+result.result.offset_result_cent[params.dataIndex]+'</br>定性判断：'+result.result.qualitative_offset_result[params.dataIndex];        
                                       
                            return res;
                            }
                     
                },
                toolbox: {
                    show : false,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                        }
                },
                legend: {
                    data:['波动率','对比历史波动率'],
                    show:true,
                    right:10,
                },
                xAxis: [{
                    type: 'category',
                    axisTick: {
                    alignWithLabel: true
                    },
                    data: result.result.fieldname_ch,
                },
                ],
                yAxis: [{
                    name:'波动率',
                    type: 'value',
                    // min: 0,
                    // max: 105000,
                    position: 'left',
                    offset:0,
                    splitLine:{show: false},//去除网格线
                    // axisLine: {
                    //     lineStyle: {
                    //         color: colors[0]
                    //     }
                    // },
                    // axisLabel: {
                    //     formatter: '{value} Kg'
                    // }
                },
               
                ],
                series: [{
                    name:'波动率',
                    type: 'line',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result.fluc_ratio,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                            // color:function(params) {
                            //     return colors[params.dataIndex]
                            // }
                        }
                    }
                },
                {
                    name:'对比历史波动率',
                    type: 'line',
                    // barWidth : 50,//柱条（K线蜡烛）宽度
                    // barGap: '1%',//柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap:'10%',//类目间柱形距离，默认为类目间距的20%，可设固定值
                    barMinHeight:10,//柱条最小高度，可用于防止某item的值过小而影响交互
                    yAxisIndex: 0,
                    data: result.result.fluc_ratio_history,
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            },
                        //     color: function(params) {
                        //         return colors[params.dataIndex]
                        // }
                    }
                }
                },
                
                ]
            };

            var ecConfig = echarts.config;
            // myChart.on('click', function (params) {
            // if (typeof params.seriesIndex != 'undefined') { 
            //     // fieldname_chinese=result.fieldname_ch[params.seriesIndex];
            //     // fieldname_english=result.fieldname_en[params.seriesIndex];
            //     // probability_distribution(fieldname_chinese,fieldname_english,result.offset_result[params.seriesIndex],params.value);

            //     // fieldname_en=result.fieldname_en[params.dataIndex];//读取字段英文名字
            //     index=params.dataIndex;//index表示分类中的第几个字段
            //     retrospectfactor(result,classification,index);
            // }
            // console.log(params);
            // });


            myChart.setOption(option,true);
            // 使用刚指定的配置项和数据显示图表。
    };

    //雷达图
    function drawRadarMap_qualityfluc(result,area){
        var myChart = echarts.getInstanceByDom(document.getElementById(area));
        myChart.clear();

        // alert(result.result[classification].condition);
        if (result.condition=='NoData'){
            document.getElementById(area).innerHTML = "质量字段缺少数据，无法进行图表展示！详情请见成本分析结果.";
            return;
        }

        var option = {
            title: {
                text: '转炉工序【质量】字段波动率',
                subtext: result.time.time1+'~'+result.time.time2+' || '+result.time.history_time1+'~'+result.time.history_time2,
                // subtext: '当前时间范围：'+result.time.time1+'~'+result.time.time2+'\n历史时间范围：'+result.time.history_time1+'~'+result.time.history_time2,
                // x:'center'
            },
            tooltip: {},
            legend: {
                data: ['当前波动率', '历史波动率'],
                right:10,
            },
            radar: {
                // shape: 'circle',
                name: {
                    formatter:'{value}',
                    textStyle: {
                        color: '#000',
                        backgroundColor: '#999',
                        borderRadius: 3,
                        padding: [3, 5],
                        
                   }
                },
                indicator: (function (){
                    var res = [];
                    var len = 0;
                    var fieldname = result.result.fieldname_ch;
                    for(var i=0;i<fieldname.length;i++){
                        res.push({
                            name: fieldname[i],max:result.result.fluc_ratio_history[i]*1.2
                        });
                    };
                    
                    return res;
                })()
 

            },

            series: [{
                name: '当前波动率 vs 历史波动率',
                type: 'radar',
                // areaStyle: {normal: {}},
                data : [
                    {
                        // value : result.material.yvalue,
                        value : result.result.fluc_ratio,
                        name : '当前波动率',
                        label: {
                            normal: {
                                show: true,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    },
                     {
                        // value : result.material.yvalue,
                        value : result.result.fluc_ratio_history,
                        name : '历史波动率',
                        label: {
                            normal: {
                                show: true,
                                formatter:function(params) {
                                    return params.value;
                                }
                            }
                        }
                    }
                ]
            }]
        };
        // var ecConfig = echarts.config;
        myChart.setOption(option,true);
    };









//单炉次成本分析：雷达图---------------------
    // //雷达图（原料raw）
    // function drawRadarMap_raw(heat_no,str_select,result){
    //     // var myChart = echarts.init(document.getElementById('main1'));
    //     var myChart = echarts.getInstanceByDom(document.getElementById('main1'));
    //     myChart.clear();
    //     var option = {
    //         title: {
    //             text: '炉次号'+heat_no+'的原料组成',
    //             // x: 'center'
    //         },
    //         tooltip: {},
    //         legend: {
    //             data: ['炉次实际值', '历史平均值']
    //         },
    //         radar: {
    //             // shape: 'circle',
    //             name: {
    //                 formatter:'{value}',
    //                 textStyle: {
    //                     color: '#000',
    //                     backgroundColor: '#999',
    //                     borderRadius: 3,
    //                     padding: [3, 5],
                        
    //                }
    //             },
    //             indicator: [
    //                { name: '铁水重量(Kg)',  max: 150000},
    //                { name: '生铁(Kg)', max: 12000},
    //                { name: '废钢总和(Kg)', max: 12000},
    //                { name: '大渣钢(Kg)', max: 10000},
    //                { name: '自产废钢(Kg)', max: 10000},
    //                { name: '重型废钢(Kg)', max: 10000},
    //                { name: '中型废钢(Kg)', max: 10000}
    //             ]

    //         },
    //         series: [{
    //             name: '实际值 vs 平均值',
    //             type: 'radar',
    //             // areaStyle: {normal: {}},
    //             data : [
    //                 {
    //                     value : result.raw.yvalue,
    //                     name : '炉次实际值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 },
    //                  {
    //                     value : result.raw.yvalue,
    //                     name : '历史平均值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 }
    //             ]
    //         }]
    //     };
    //      var ecConfig = echarts.config;
    //      myChart.setOption(option);
    // }

    // //雷达图（物料material）
    // function drawRadarMap_material(heat_no,str_select,result){
    //     // var myChart = echarts.init(document.getElementById('main2'));
    //     var myChart = echarts.getInstanceByDom(document.getElementById('main2'));
    //     myChart.clear();
    //     var option = {
    //         title: {
    //             text: '炉次号'+heat_no+'的物料组成',
    //             // x: 'center'
    //         },
    //         tooltip: {},
    //         legend: {
    //             data: ['炉次实际值', '历史平均值']
    //         },
    //         radar: {
    //             // shape: 'circle',
    //             name: {
    //                 formatter:'{value}',
    //                 textStyle: {
    //                     color: '#000',
    //                     backgroundColor: '#999',
    //                     borderRadius: 3,
    //                     padding: [3, 5],
                        
    //                }
    //             },
    //             indicator: [
    //                { name: '总吹氧消耗(NM3)',  max: 5000},
    //                { name: '氮气耗量(NM3)', max: 1500},
    //                { name: '1#烧结矿(Kg)', max: 8000},
    //                { name: '石灰石_40-70mm(Kg)', max: 8000},
    //                { name: '萤石_FL80(Kg)', max: 8000},
    //                { name: '增碳剂(Kg)', max: 8000},
    //                { name: '低氮增碳剂(Kg)', max: 8000},
    //                { name: '石灰(Kg)', max: 8000},
    //                { name: '轻烧白云石(Kg)', max: 8000}
    //             ]

    //         },
    //         series: [{
    //             name: '实际值 vs 平均值',
    //             type: 'radar',
    //             // areaStyle: {normal: {}},
    //             data : [
    //                 {
    //                     value : result.material.yvalue,
    //                     name : '炉次实际值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 },
    //                  {
    //                     value : result.material.yvalue,
    //                     name : '历史平均值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 }
    //             ]
    //         }]
    //     };
    //      var ecConfig = echarts.config;
    //      myChart.setOption(option);
    // }

    // //雷达图（产品product）
    // function drawRadarMap_product(heat_no,str_select,result){
    //     // var myChart = echarts.init(document.getElementById('main3'));
    //     var myChart = echarts.getInstanceByDom(document.getElementById('main3'));
    //     myChart.clear();
    //     var option = {
    //         title: {
    //             text: '炉次号'+heat_no+'的产品组成',
    //             // x: 'center'
    //         },
    //         tooltip: {},
    //         legend: {
    //             data: ['炉次实际值', '历史平均值']
    //         },
    //         radar: {
    //             // shape: 'circle',
    //             name: {
    //                 formatter:'{value}',
    //                 textStyle: {
    //                     color: '#000',
    //                     backgroundColor: '#999',
    //                     borderRadius: 3,
    //                     padding: [3, 5],
                        
    //                }
    //             },
    //             indicator: [
    //                { name: '钢水(Kg)',  max: 105000},
    //                { name: '转炉煤气(Kg)', max: 12000},
    //                { name: '钢渣(Kg)', max: 22000},
    //             ]

    //         },
    //         series: [{
    //             name: '实际值 vs 平均值',
    //             type: 'radar',
    //             // areaStyle: {normal: {}},
    //             data : [
    //                 {
    //                     value : result.product.yvalue,
    //                     name : '炉次实际值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 },
    //                  {
    //                     value : result.product.yvalue,
    //                     name : '历史平均值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 }
    //             ]
    //         }]
    //     };
    //      var ecConfig = echarts.config;
    //      myChart.setOption(option);
    // }

    // //雷达图（合金alloy）
    // function drawRadarMap_alloy(heat_no,str_select,result){
    //     // var myChart = echarts.init(document.getElementById('main4'));
    //     var myChart = echarts.getInstanceByDom(document.getElementById('main4'));
    //     myChart.clear();
    //     var option = {
    //         title: {
    //             text: '炉次号'+heat_no+'的合金组成',
    //             // x: 'center'
    //         },
    //         tooltip: {},
    //         legend: {
    //             data: ['炉次实际值', '历史平均值']
    //         },
    //         radar: {
    //             // shape: 'circle',
    //             name: {
    //                 formatter:'{value}',
    //                 textStyle: {
    //                     color: '#000',
    //                     backgroundColor: '#999',
    //                     borderRadius: 3,
    //                     padding: [3, 5],
                        
    //                }
    //             },
    //             indicator: [
    //                { name: '硅铁(Kg)',  max: 5000},
    //                { name: '微铝硅铁(Kg)', max: 5000},
    //                { name: '硅锰合金(Kg)', max: 5000},
    //                { name: '高硅硅锰(Kg)', max: 5000},
    //                { name: '中碳铬铁(Kg)', max: 5000}
    //                // { name: '硅铁(Kg)'},
    //                // { name: '微铝硅铁(Kg)'},
    //                // { name: '硅锰合金(Kg)'},
    //                // { name: '高硅硅锰(Kg)'},
    //                // { name: '中碳铬铁(Kg)'}
    //             ]

    //         },
    //         series: [{
    //             name: '实际值 vs 平均值',
    //             type: 'radar',
    //             // areaStyle: {normal: {}},
    //             data : [
    //                 {
    //                     value : result.alloy.yvalue,
    //                     name : '炉次实际值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 },
    //                  {
    //                     value : result.alloy.yvalue,
    //                     name : '历史平均值',
    //                     label: {
    //                         normal: {
    //                             show: true,
    //                             formatter:function(params) {
    //                                 return params.value;
    //                             }
    //                         }
    //                     }
    //                 }
    //             ]
    //         }]
    //     };
    //      var ecConfig = echarts.config;
    //      myChart.setOption(option);
    // }


