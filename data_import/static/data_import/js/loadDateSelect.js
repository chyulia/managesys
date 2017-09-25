
 function day_formatter(day,month,year){  //格式化输出日期
        if(day<10){
           day="0"+day;
        }
        if(month<10){
           month="0"+month;
        }
        var date = year+"-"+ month +"-"+day;
        return date
    }

    function get_today(){ //获取今日的日期
        var date = new Date(); 
        var year = date.getFullYear();  //年
        var month = date.getMonth()+1;   //月
        var day = date.getDate();  //日
        var hour = date.getHours();   //时
        var minute = date.getMinutes();   //分
        var second = date.getSeconds();  //秒

        sql_date2 = day_formatter(day,month,year);
        document.getElementById("select_date2").value = sql_date2;
        var today = {
            year:year,
            month:month,
            day:day,
            sql_date2:sql_date2
        };
        //console.log(today);
        return today
    }

    function SelectDate_default(){
        document.getElementById("select_date1").value = '2016-01-01';
        document.getElementById("select_date2").value = '2016-07-31';
    }

    function SelectDate_oneMonth(){
        var today = get_today();
        var newYear;
        var newMonth;
        var newDay;
        var sql_date2;
        var sql_date1;
        //得到每月天数
        var daysInMonth = new Array(0,31,28,31,30,31,30,31,31,30,31,30,31);
        if(today.tear%4 == 0 && today.tear%100 != 0){ 
            //闰年2月有29天
           daysInMonth[2]= 29;
       }
        //得到上一月月份数 与 年份数
        if (today.month == 1){
            newMonth = 12;
            newYear = today.year - 1
        }else{
            newMonth = today.month - 1
            newYear = today.year
        }
        //得到上一月日期的 日
        if(daysInMonth[newMonth] < today.day){
            newDay = daysInMonth[newMonth];
        }else{
            newDay = today.day
        }
        //格式化输出
        sql_date1 = day_formatter(newDay,newMonth,newYear);
        //赋值给时间选择空间
        document.getElementById("select_date1").value = sql_date1;

        var oneMonth = {
            year:newYear,
            month:newMonth,
            day:newDay,
            sql_date1:sql_date1
        };
        console.log(oneMonth);
        return oneMonth
    }

    function SelectDate_threeMonth(){
        var today = get_today();
        var newYear;
        var newMonth;
        var newDay;
        var sql_date2;
        var sql_date1;
        //得到每月天数
        var daysInMonth = new Array(0,31,28,31,30,31,30,31,31,30,31,30,31);
        if(today.tear%4 == 0 && today.tear%100 != 0){ 
            //闰年2月有29天
           daysInMonth[2]= 29;
       }
        //得到上一月月份数 与 年份数
        if (today.month == 1){
            newMonth = 10;
            newYear = today.year - 1
        }else if (today.month == 2){
            newMonth = 11;
            newYear = today.year - 1
        }else if (today.month == 3){
            newMonth = 12;
            newYear = today.year - 1
        }else{
            newMonth = today.month - 3
            newYear = today.year
        }
        //得到上一月日期的 日
        if(daysInMonth[newMonth] < today.day){
            newDay = daysInMonth[newMonth];
        }else{
            newDay = today.day
        }

        sql_date1 = day_formatter(newDay,newMonth,newYear);
        document.getElementById("select_date1").value = sql_date1;
        // var oneMonth = {
        //     year:newYear,
        //     month:newMonth,
        //     day:newDay,
        //     sql_date1:sql_date1
        // };
        // console.log(oneMonth);
        // return oneMonth
    }

    function SelectDate_halfYear(){
        var today = get_today();
        var newYear;
        var newMonth;
        var newDay;
        var sql_date2;
        var sql_date1;
        //得到每月天数
        var daysInMonth = new Array(0,31,28,31,30,31,30,31,31,30,31,30,31);
        if(today.tear%4 == 0 && today.tear%100 != 0){ 
            //闰年2月有29天
           daysInMonth[2]= 29;
       }
        //得到上一月月份数 与 年份数
        if (today.month == 1){
            newMonth = 7;
            newYear = today.year - 1
        }else if (today.month == 2){
            newMonth = 8;
            newYear = today.year - 1
        }else if (today.month == 3){
            newMonth = 9;
            newYear = today.year - 1
        }else if (today.month == 4){
            newMonth = 10;
            newYear = today.year - 1
        }else if (today.month == 5){
            newMonth = 11;
            newYear = today.year - 1
        }else if (today.month == 6){
            newMonth = 12;
            newYear = today.year - 1
        }else{
            newMonth = today.month - 6
            newYear = today.year
        }
        //得到上一月日期的 日
        if(daysInMonth[newMonth] < today.day){
            newDay = daysInMonth[newMonth];
        }else{
            newDay = today.day
        }

        sql_date1 = day_formatter(newDay,newMonth,newYear);
        document.getElementById("select_date1").value = sql_date1;
        // var oneMonth = {
        //     year:newYear,
        //     month:newMonth,
        //     day:newDay,
        //     sql_date1:sql_date1
        // };
        // console.log(oneMonth);
        // return oneMonth
    }

    function SelectDate_oneYear(){
        var today = get_today();
        var newYear;
        var newMonth;
        var newDay;
        var sql_date1;
        //得到上一月月份数 与 年份数
        newYear = today.year -1
        newMonth = today.month 
        newDay = today.day
        //格式化输出日期
        sql_date1 = day_formatter(newDay,newMonth,newYear);
        document.getElementById("select_date1").value = sql_date1;
        // var oneMonth = {
        //     year:newYear,
        //     month:newMonth,
        //     day:newDay,
        //     sql_date1:sql_date1
        // };
        // console.log(oneMonth);
        // return oneMonth
    }