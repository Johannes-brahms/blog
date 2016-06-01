
/* Variable */

var is_toggle = false

var image

/* Function */

$('#binary').click(

	function (argument) {


		var filename = $('#filename').text();

		var version = $('#current-version').text();
		  
		$.get('binary', {'filename' : filename, 'current-version' : version}, function(response){

			alert(response['filename']);
			//$('#image-zone').html('<img src = ' + response['image-url'] + '></img>')
			$('#processing-image-area').html('<img id = "processing-image" src = ' + response['filename'] + '></img>')
			$('#current-version').html(response['current-version']);

            refresh();
		})
	})


$('#toggle').click(

    function(){

        if(is_toggle == false){

            $('#original-image').hide();

            is_toggle = true;

            refresh();

        }

        else if(is_toggle == true){

            $('#original-image').show();

            is_toggle = false;

            refresh();
        }
    })


$(window).resize(function() {

    var width = $(window).width();

    refresh();

    $('.dropbtn').css({

        'width' : width / 10,
        'font-size' : width / 70

    })
    

});


function refresh(){

    var width = $(window).width();

    var right = (width - image) / 2;

    if (is_toggle == true){

        $('#processing-image').css({    

            'position' : 'absolute',
            'right' : right,
            'width' : image,

        });
    }

    else if(is_toggle == false){

        var center = width / 2;

        var axis = (center - image) / 3 * 2;

        $('#original-image').css({

            'position' : 'absolute',
            'width' : image,
            'left' : axis

        })


        $('#processing-image').css({

            'position' : 'absolute',
            'width' : image,
            'right' : axis

        })
    }
}




$('#upload-form').on('submit', function(event){
    
    event.preventDefault();

    alert('submit');
  
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
            refresh();
    	   $('#home').slideUp();

    	}
	});
})


$(document).ready(

    function(){

        var width = $(window).width();

        image = width / 2.5;

        var center = width / 2;

        var axis = (center - image) / 3 * 2;

        refresh();
  
})



$("#upload-input").change(

    function() {

        $('#upload-form').trigger('submit');
     
});

/*
$(window).load(function(){
      // your code
      alert('standby')
});*/

/*$("#upload-input").on('submit', function(event){
    
     $('#upload-form2').trigger('submit');
     
});*/

/*
$('.dropbtn').click(
	function(){

		$(this).closest('.dropdown').find('.dropdown-content').show();
	})*/

    /*
$('#open-image').click(

    function(argument){

        var image_url = $('#image-url').val();

        $.get('open', {'image-url' : image_url}, function(response) {

            $('#image-zone').html('<img src = ' + response['image-url'] + '></img>')
        
        })
    })

*/

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



