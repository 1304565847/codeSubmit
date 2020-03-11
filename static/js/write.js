function preview()
{
}

window.onload = function(){
    $("#content").bind("input propertychange", function(){
        $("#res").html(marked($("#content").val()))
        $("table").attr("class", "table table-bordered table-hover")
    })
    var i = document.getElementById('uploadImg');
    var reader = new FileReader();
    var img = document.getElementById("preview");
    reader.onload = function()
    {
        img.src = this.result;
        $("#preview").fadeIn(500)
    }
    $("#uploadImg").bind("input propertychange", function(){
        reader.readAsDataURL(i.files[0]);
    })
}


// 口令
function run() {
    var passwd = prompt("请输入口令：")
    $.get("/verify", {passwd: passwd}, function(res){
        if (!res.res){
            window.location = "/"
        }
    })
}


function uploadImg()
{
    var fd = new FormData($("#imgForm")[0]) 
    $.ajax({
        url:"/upload",
        type:"post",
        data:fd,
        processData:false,
        contentType:false,
        success:function(res){
            console.log(res);
        },
        error: function(data){
            $("#imgres").val(data['responseText'])
        },
        dataType:"multipart/form-data"
    })
}