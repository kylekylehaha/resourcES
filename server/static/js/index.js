$(document).ready(()=>{
    console.log("document ready");
});

$('#exampleModal').on('show.bs.modal', function (event) {
	var button = $(event.relatedTarget); // Button that triggered the modal
    var modal = $(this);
    if(button.text() == 'Reservation'){
	    modal.find('.modal-title').text('Reservation');
        $("#recipient-name").val(button.attr('id'));
		$("label[for=message-text]").html('預約:');
        $("label[for=options1]").html("確認預約");
        $("label[for=options2]").html("先不要預約");
    }
    else if(button.text() == 'Borrow'){
    	modal.find('.modal-title').text('Borrow');
	    modal.find('#recipient-name').val(button.attr('id'));
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

$('#search_button').click(()=>{
    var keyword = $('#search_input').val();
    console.log(keyword);
    
    if (! keyword){
        alert("Please enter keyword");
    }
    else{
        window.location.href = "/keyword?keyword="+keyword;
    }
    /*$.ajax({
		url: "/keyword?"+keyword,
		type: 'POST',
		data: {
			//user_name: $('#user_name').val()
		},
		error: function(xhr) {
			alert('Ajax request 發生錯誤');
		},
		success: function(response) {
            console.log("good")
        }
	});*/

})

$("#confirm-button").click(()=>{
	var ssn = 'E94051136';
    var checked = $('[name=optionsRadios]:checked');
    var checked_value = checked.val();
	var type = $("#exampleModalLabel").text();
    var enumber = $("#recipient-name").val();

	$('#confirm-button').attr("data-dismiss","modal");
	$.ajax({
		url: "/add?"+"ssn="+ssn+"&type="+type+"&value="+checked_value+"&enum="+enumber,
		type: 'GET',
		data: {
			//user_name: $('#user_name').val()
		},
		error: function(xhr) {
			alert('Ajax request 發生錯誤');
		},
		success: function(response) {
            if(response == "duplicated"){
	    	    $.alert({
                    theme: 'modern',
                    icon: 'fa fa-warning',
                    columnClass: 'col-md-5 col-md-offset-5',
                    //columnClass: 'large',
                    closeIcon: true,
                    type: 'orange',
                    typeAnimated: true,
 
                    title: 'Alert!',
                    content: '<strong>You have already made a reservation of this equipment.</strong>',
                }); 
           }
            else
                console.log("sucess");
                location.reload();
		}
	});
});
