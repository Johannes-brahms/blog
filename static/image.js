
/* Variable */

var is_toggle = false

var image

var version

var filename

/* Function */

function refresh(){

    

    var width = $(window).width();

    if (is_toggle == true){

        var right = (width - image * 2) / 2;

        $('#processing-image').css({    

            'position' : 'absolute',
            'right' : right,
            'width' : image * 2,

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

$(document).ready(

    function(){

        var width = $(window).width();

        image = width / 2.5;

        var center = width / 2;

        var axis = (center - image) / 3 * 2;

        refresh();
  
})

$(window).resize(function() {

    var width = $(window).width()

    refresh()

    $('.dropbtn').css({

        'width' : width / 10,

        'font-size' : width / 70

    })

});


/* Button */

$('#binary').click(

	function (argument) {

		//var version = $('#current-version').text();
		  
		$.get('binary', {'filename' : filename, 'current-version' : version}, function(response){
			
			$('#processing-image-area').html('<img id = "processing-image" src = ' + response['filename'] + '></img>')

            version = response['current-version']

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


$('#undo').click(

    function(){

        version -= 1

        if (version < 0)

            version = 0

        else {

            $('#processing-image-area').html('<img id = "processing-image" src = ' + filename.concat('/').concat(version).concat('.jpg') + '></img>')

            refresh();
        }
    })

/* listen */

$('#upload-form').on('submit', function(event){
    
    event.preventDefault();

    /*alert('submit');*/
  
    $.ajax({

    	url: 'upload_file',
    	type: 'POST',
    	data: new FormData(this),
    	contentType: false, //必须
    	processData: false, //必须
    	dataType: 'json',
    	success: function(response){
    	
    	   $('#original-image-area').html('<img id = "original-image" src = ' + response['original'] + '></img>')
    	   $('#processing-image-area').html('<img id = "processing-image" src = ' + response['original'] + '></img>')
    	   //$('#filename').html(response['filename']);
    	   //$('#current-version').html('0');
           filename = response['filename'];
           version = 0;
           refresh();

           $('#home').animate({width:'toggle'}, 350);

        }
    });
});

$('#upload-input').change(

    function() {

        /*alert('change')*/

        $('#upload-form').trigger('submit');
     
});


$('.value-bar').change(

    function(){

        var values = $(this).find('input[type = "range"]').val();

        $(this).find('.values').html(values);

    }
)

function Call(S){

    var J = {}

    $('#' + S).parent().find('input[type = "range"]').each(function(){

        name = $(this).attr('id');
            
        var values = $(this).val();

        J[name] = values;

        })

    J['filename'] = filename;

    J['current-version'] = version;

    $.get(S, J, function(response){
            
        $('#processing-image-area').html('<img id = "processing-image" src = ' + response['filename'] + '></img>')

        version = response['current-version']

        refresh();

    })

}

/* Opencv function */

$('#canny').click(

    function(){

        Call('canny')
    })

$('#blur').click(

    function(){

        Call('blur')
    })

$('#GaussianBlur').click(

    function(){

        Call('GaussianBlur')
    })

$('#medianBlur').click(

    function(){

        Call('medianBlur')
    })


