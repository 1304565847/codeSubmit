window.onload = function(){
    $("#info").attr("data-content", 
            "本页显示的图片经过了统一格式处理，会导致图片长宽比异常，正常图片请单击查看\n要使用图片请在图片上方右键->复制链接进行使用\n再次单击说明按钮关闭本说明页")
    // 初始化弹出框
    $('[data-toggle="popover"]').popover();   
    // 预览图片
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

// 使用ajax上传图片
function uploadImg()
{
    var fd = new FormData($("#imgForm")[0]) 
    if ($("#uploadImg")[0].files[0].size > 1024*1024){
        alert("图片大小大于1M，上传失败")
        reutrn
    }
    if ($("#uploadImg")[0].files[0].type.indexOf("image") == -1){
        alert("文件格式不对，请选择图片文件")
        return
    }
    if($)
    src = $("#preview").attr("src")
    if (!src){
        alert("请选择图片")
        reutrn
    }
    $.ajax({
        url:"/upload/",
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