$(document).ready(()=>{
    console.log("document ready");
});

var dir = "";
$("#up").click(()=>{
	dir = "up";
	SendChange();
})

$("#right").click(()=>{
	dir = "right";
	SendChange();
})

$("#left").click(()=>{
	dir = "left";
	SendChange();
})

$("#down").click(()=>{
	dir = "down";
	SendChange();
})

function SendChange(){
	console.log(dir);
	$.ajax({
		url: "/change_dir?"+"dir="+dir,
		type: 'GET',
		data: {
			//user_name: $('#user_name').val()
		},
		error: function(xhr) {
			alert('Ajax request 發生錯誤');
		},
		success: function(response) {
			console.log(response);
        }
	});
}

$(document).keydown(function(e) {
	if(e.keyCode == 37) { // left
		$("#left").button('toggle');
		dir = "left";
		SendChange();
	}
	else if(e.keyCode == 39) { // right
		$("#right").button('toggle');
		dir = "right";
		SendChange();
	}
	else if(e.keyCode == 38){ //up
		$("#up").button('toggle');
		dir = "up";
		SendChange();
	}
	else if(e.keyCode == 40){ //down
		$("#down").button('toggle');
		dir = "down";
		SendChange();
	}
});

$(document).keyup(function(e){
	if(e.keyCode == 37)
		$("#left").button('toggle');
	else if(e.keyCode == 39)
		$("#right").button('toggle');
	else if(e.keyCode == 38)
		$("#up").button('toggle');
	else if(e.keyCode == 40)
		$("#down").button('toggle');
})

