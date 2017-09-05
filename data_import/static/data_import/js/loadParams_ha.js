function heatno_ha(){
    $.ajax({
        type: "POST",
        dataType:"json",
        url: "/heat_no_quality" ,
        data: {'greet':'hello'},
        success: function(data){
            pnames=data.result;
            $(".HEAT_NO").append("<option value='blank' selected =\"selected\"></option>");
            for(var pname in pnames){
                //  console.log(pnames[pname]) 
                 $(".HEAT_NO").append("<option value='"+pnames[pname]+"'>"+pnames[pname]+"</option>");
            }
        },
        error: function () {
            alert("error");
            }
        });
        };
