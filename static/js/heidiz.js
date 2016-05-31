
$("#right").hover(function(){
        $(this).stop(true, true).animate({ width: "200px" });
}, function() {
        $(this).stop(true, true).animate({ width: "100px" });
});


$('#previous-page').hover(
	function () {
		$(this).hide()
		  
	})


$('#next-page').hover(
    function(){
        $(this).hide();
    });


