$("button").click((evt)=>{
    var btn_id = $(evt.target).attr('id');
    //console.log(btn_id);

    var order_num = "";
    var operation = "";    
    for(i = 0 ; i < btn_id.length ; i++){
        if (i < 5)
            order_num += btn_id[i];
        else
            operation += btn_id[i];
    }
    console.log(order_num);
    console.log(operation);

	var current_loc = window.location.href;
	var name = decodeURI(current_loc.split('/')[4].split("?")[0]);

    $.ajax({
		url: "/update_status?name="+name+"&order_num="+order_num+"&operation="+operation,
		type: 'GET',
		data: {
			//user_name: $('#user_name').val()
		},
		error: function(xhr) {
			alert('Ajax request 發生錯誤');
		},
		success: function(response){
            console.log("good");
            location.reload();
        }
	});
})
