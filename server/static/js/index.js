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

$('#nav_bar_title').click(()=>{
    var current_loc = window.location.href;
    var name = decodeURI(current_loc.split('/')[4].split('?')[0]);
    console.log(name);
    var temp="";
    for(i = 0 ; i < current_loc.search('/keyword') ; i++)
        temp+=current_loc[i]
    console.log(temp)
    window.location.href = temp + "/mall/"+name;
})

function SearchFunc(){
    var keyword = $('#search_input').val();
    console.log(keyword);
    var current_loc = window.location.href;
    
    var name = decodeURI(current_loc.split('/')[4].split('?')[0]);
    console.log(name);

    var temp="";
    if (current_loc.search('/keyword/') > 0){
        console.log("yes");
        for(i = 0 ; i < current_loc.search('/keyword/')+('/keyword/').length; i++)
            temp += current_loc[i];
        temp += name
        console.log(temp)
    }
    else{
        temp = current_loc.replace('mall','keyword');
        console.log(temp);
    }
    if (! keyword){
        alert("Please enter keyword");
    }
    else{
        window.location.href = temp + "?keyword=" + keyword;
    }
 
}

$('#search_button').click(()=>{
    SearchFunc();
    /*
    var keyword = $('#search_input').val();
    console.log(keyword);
    var current_loc = window.location.href;
    
    var name = decodeURI(current_loc.split('/')[4].split('?')[0]);
    console.log(name);

    var temp="";
    if (current_loc.search('/keyword/') > 0){
        console.log("yes");
        for(i = 0 ; i < current_loc.search('/keyword/')+('/keyword/').length; i++)
            temp += current_loc[i];
        temp += name
        console.log(temp)
    }
    else{
        temp = current_loc.replace('mall','keyword');
        console.log(temp);
    }
    if (! keyword){
        alert("Please enter keyword");
    }
    else{
        window.location.href = temp + "?keyword=" + keyword;
    }
    */

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
    var checked = $('[name=optionsRadios]:checked');
    var checked_value = checked.val();
	var type = $("#exampleModalLabel").text();
    var enumber = $("#recipient-name").val();
    
    var current_loc = window.location.href;
    var name = decodeURI(current_loc.split('/')[4].split('?')[0]);
    console.log(name);

	$('#confirm-button').attr("data-dismiss","modal");

    $.ajax({
		url: "/add?"+"name="+name+"&type="+type+"&value="+checked_value+"&enum="+enumber,
		type: 'GET',
		data: {
			//user_name: $('#user_name').val()
		},
		error: function(xhr) {
			alert('Ajax request 發生錯誤');
		},
		success: function(response) {
            if(response == "cannotreserved"){
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
