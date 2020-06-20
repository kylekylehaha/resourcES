$(document).ready(()=>{
    console.log("document ready");
});

$("button").click((evt)=>{
    console.log($(evt.target).attr('id'));
    //var trid = $(event.target).closest("tr").attr('id'); // table row ID
	//console.log(trid);
    
    /*
    $.ajax({
		url: "/send?"+"product="+product_num+"&sensor="+send_topic+"&change="+send_message,
		type: 'GET',
		data: {
			//user_name: $('#user_name').val()
		},
		error: function(xhr) {
			alert('Ajax request 發生錯誤');
		},
		success: function(response) {
			console.log("sucess");
		}
	});
    */
});

$('#exampleModal').on('show.bs.modal', function (event) {
	var button = $(event.relatedTarget); // Button that triggered the modal
    var modal = $(this);
    if(button.text() == 'Reservation'){
	    modal.find('.modal-title').text('Reservation');
	    modal.find('.modal-body input').val(button.attr('id'));
        $("label[for=message-text]").html('預約:');
        $("label[for=options1]").html("確認預約");
        $("label[for=options2]").html("先不要預約");
    }
    else if(button.text() == 'Borrow'){
    	modal.find('.modal-title').text('Borrow');
	    modal.find('.modal-body input').val(button.attr('id'));
        $("label[for=message-text]").html("借用:");
        $("label[for=options1]").html("確認借用");
        $("label[for=options2]").html("先不要借用");   
    }

  //var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
	/*
    var modal = $(this);
	modal.find('.modal-title').text('Reservation');
	modal.find('.modal-body input').val(button.attr('id'));
    */
});

$("#confirm-button").click(()=>{
});
