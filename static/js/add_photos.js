function inputUrl(id){ //点击div触发点击input事件
	$(id).click();
};

function fileUrl(self){ //当有图片输入时
    var read = new FileReader();
    img = document.getElementById(""+self.id).files[0];
    console.log(img);
    read.readAsDataURL(img);
    num = self.id[self.id.length-1];
    read.onload = function(e){
    	$(".p-"+num+">img").attr("src",this.result);
    	$(".p-"+num+">img").attr("name",img.name);

    }
    $(".p-"+num+">img").css({"display":"block"});
    $(".p-"+num+">i").attr("style", "display:none;");
    $(".p-"+num).siblings("button").css("display","block");
    var photoSize = $(".one-photo").length;
    num = parseInt(num);
    var fd = new FormData();
    fd.append("fafafa", img);

    var token = $.cookie('csrftoken');

    $.ajax({
        url: "/backend/upload_lbt/",
        type: "POST",
        headers: {'X-CSRFToken': token},
        data: fd,
        processData: false,  // tell jQuery not to process the data, 不要做特殊的处理
        contentType: false,  // tell jQuery not to set contentType, 不要做特殊的处理
        success: function(arg, a1, a2){
            window.location.reload();
        }
    });
    //if (num>=photoSize && photoSize<=4) //最多支持添加五张图片
    	addNew(num+1);
}

function addNew(num){ //新增加一个输入框
	var boxDiv = $('<div class="one-photo"></div>');
	var imgDiv = $('<div class="add-now p-'+num+'" onclick="inputUrl(\'#photo-'+num+'\')"></div>');
	var imgI = $('<i class="fa fa-fw fa-plus-square"></i>');
	var img = $('<img src = "" style="display: none; width:200px;">');
	var input = $('<input type="file" name="photo"  accept=".jpg,.jpeg,.png" style="display: none;" onchange="fileUrl(this);" id="photo-'+num+'">');
	var delButton = $('<button onclick="removeImge(this, \''+num+'\')" style="display:none;">删除</button>')
	imgDiv.append(imgI);
	imgDiv.append(img);
	console.log(imgDiv);
	boxDiv.append(imgDiv);
	boxDiv.append(input);
	boxDiv.append(delButton);
	$("#add-photos").append(boxDiv);


}

function removeImge(ths, num){
	//var ch = ths.previousSibling.previousSibling.previousSibling.children();
	var ch = $(ths).prev().prev().prev().children();
	var path = ch[0].src;
	console.log(path);
	var photos = $(".one-photo");
	var photosLength = photos.length;
	console.log(photosLength);
	photos[num-1].remove(); //删除当前图片框div
	for(var i=num;i<photosLength;++i){ //修改后面图片内容
		photos.eq(i).find("div.add-now").attr("class","add-now p-"+i);
		photos.eq(i).find("div.add-now").attr("onclick","inputUrl('#photo-"+i+"')");
		photos.eq(i).find("input").attr("id","photo-"+i);
		photos.eq(i).find("button").attr("onclick","removeImge(this, \""+i+"\")");
	}
	var token = $.cookie('csrftoken');
    $.ajax({
        url: "/backend/delete_lbt/",
        type: "POST",
        headers: {'X-CSRFToken': token},
        data: {"path": path},
        // processData: false,  // tell jQuery not to process the data, 不要做特殊的处理
        // contentType: false,  // tell jQuery not to set contentType, 不要做特殊的处理
        success: function(arg, a1, a2){

        }
    });

}

