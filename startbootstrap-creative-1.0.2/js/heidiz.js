
$("#right-button").hover(function(){
        $(this).stop(true, true).animate({ width: "200px" });
}, function() {
        $(this).stop(true, true).animate({ width: "100px" });
});


$("#right-butto").hover(
        function(){
            $(this).hide()
        });


$("#right-button").click(function(){
    
    $(this).text("Hello this is text");


});
