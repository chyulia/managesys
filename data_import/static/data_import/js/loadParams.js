function loadOption(){
	$.ajax({
        type: "post",
        url:  "/load_procedure_name",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {

            console.log(data.procedure_names);
            pnames=data.procedure_names;
            for(var pname in pnames){
                // console.log(pnames[pname])
                $(".procedurename").append("<option value='"+pname+"'>"+pnames[pname]+"</option>")
            }
            var filepath= 'http://127.0.0.1:8000'+data.filepath;
            console.log("<a href='"+filepath+"'>")
            $("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
function loadOption_ha(){
    $.ajax({
        type: "post",
        url:  "/lond_to",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {
            //console.log(data.procedure_names)
            //console.log(data.procedure_names);
            pnames=data.procedure_names;
            for(var pname in pnames){
                //console.log(pnames[pname])
                $(".procedurename").append("<option value='"+pname+"'>"+pnames[pname]+"</option>")
            }
            // var filepath= 'http://127.0.0.1:8000'+data.filepath;
            // console.log("<a href='"+filepath+"'>")
            // $("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
function no_loadOption_ha(){
    $.ajax({
        type: "post",
        url:  "/no_lond_to",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {
            pnames=data.no_procedure_names;
            for(var pname in pnames){
                //console.log(pnames[pname])
                //console.log(pname)
                $(".no_procedurename").append("<option value='"+pname+"'>"+pnames[pname]+"</option>")
            }
            //var filepath= 'http://127.0.0.1:8000'+data.filepath;
            //console.log("<a href='"+filepath+"'>")
            //$("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
function getFilepath(){
    var procedure=$("#procedure").find("option:selected").val();//获取值用text()
    $.ajax({
        type: "post",
        url:  "/ana_data_lack",
        data: {'procedure':procedure},
        error: function() {
            alert("404");
        },
        success: function(data) {
            console.log(data.filepath);
            console.log('<a href="/download_file?filepath='+data.filepath+'">下载文件</a>')
            // $("#filedownload").html('<a href="/download_file?filepath='+data.filepath+'">下载文件</a>')
        }
    })


}
function loadOption_chen(){
    $.ajax({
        type: "post",
        url:  "/lond_to",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {
            //console.log(data.procedure_names);
            pnames=data.procedure_names;
            for(var pname in pnames){
                // console.log(pnames[pname])
                $(".procedurename1").append("<option value='"+pname+"'>"+pnames[pname]+"</option>");
                $(".fluctution_time").append("<option value='"+pname+"'>"+pnames[pname]+"</option>");
            }
            //var filepath= 'http://127.0.0.1:8000'+data.filepath;
            //console.log("<a href='"+filepath+"'>")
            //$("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
function p_loadGrape_ha(){
    $.ajax({
        type: "POST",
        dataType:"json",
        url: "/paihao_getGrape" ,
        data: {'greet':'hello'},
        success: function(data){
            pnames=data.result;
            $(".gangzhong_name").append("<option value='blank' selected =\"selected\"></option>");
            for(var pname in pnames){
                //  console.log(pnames[pname])
                 $(".gangzhong_name").append("<option value='"+pnames[pname]+"'>"+pnames[pname]+"</option>");
            }
        },
        error: function () {
						console.log("here");
            alert("error");
            }
        });
        };

function little_loadOption_ha(){
    $.ajax({
        type: "post",
        url:  "/little_lond_to",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {
            pnames=data.little_procedure_names;
            for(var pname in pnames){
                //console.log(pnames[pname])
                //console.log(pname)
                $(".little_procedurename").append("<option value='"+pname+"'>"+pnames[pname]+"</option>")
            }
            //var filepath= 'http://127.0.0.1:8000'+data.filepath;
            //console.log("<a href='"+filepath+"'>")
            //$("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
