$('#open-image').click(

	function(argument){

		var image_url = $('#image-url').val();

		$.get('open', {'image-url' : image_url}, function(response) {

			$('#image-zone').html('<img src = ' + response['image-url'] + '></img>')
		
		})
	})



$('#binary').click(

	function (argument) {


		var filename = $('#filename').text();
		var version = $('#current-version').text();
		  


		alert(filename);

		$.get('binary', {'filename' : filename, 'current-version' : version}, function(response){

			//$('#image-zone').html('<img src = ' + response['image-url'] + '></img>')
			$('#processing-image-area').html('<img id = "processing-image" src = ' + response['filename'] + '></img>')

		})
	})



/*$('#upload-btn').hover(
        function(){
            
            $('#upload-image').slideDown();
        })
*/

/*$('#upload-image').mouseleave(
        function(){
            $(this).slideUp();
        })
*/

/*$('#upload-btn').click(

	function(){
		alert('dddssssd')

		var fileInput = $('#upload-image')


		$.post('upload_file', {}, function(response){

			alert('dddd')
			$('#upload-result').html('upload success')
		})
	})
*/

/*$('#upload-btn').click( function() {
	var a = $('#upload-form').serialize()
    
    $.post( 'upload_file', $('#upload-form').serialize(), function(data) {
         
         
       },
       'json' // I expect a JSON response
    );
});*/

/*$('#upload-btn').click(function(){
	alert('dddddddddddd')
	$('#upload-form').submit()
})*/

/*


$('form#upload-form').submit(function(){
	

	var formData = new FormData($(this))

	alert('success')

	 $.ajax({
        url: 'upload_file',
        type: 'POST',
        data: formData,
        async: false,
        success: function (data) {
            alert(data)
        },
        cache: false,
        contentType: false,
        processData: false
    });


})*/

$("#upload-input").change(
	function() {
     $('#upload-form2').trigger('submit');
     
});

$('#upload-form2').on('submit', function(event){
    
    event.preventDefault();
    alert('submit')

  
    $.ajax({
    	url: 'upload_file',
    	type: 'POST',
    	data: new FormData(this),
    	contentType: false, //必须
    	processData: false, //必须
    	dataType: 'json',
    	success: function(response){
    	
    	$('#original-image-area').html('<img id = "original-image" src = ' + response['filename'] + '></img>')
    	$('#processing-image-area').html('<img id = "processing-image" src = ' + response['filename'] + '></img>')
    	$('#filename').html(response['filename']);
    	$('#current-version').html('0');
    	$('#home').slideUp();

    	}
	});
})

/*
$("#upload-input").on('submit', function(event){
    
     $('#upload-form2').trigger('submit');
     
});*/



/*
$('.dropbtn').click(
	function(){

		$(this).closest('.dropdown').find('.dropdown-content').show();
	})*/