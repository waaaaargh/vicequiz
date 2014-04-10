var current_tweet = null;

function answer(tweet_id, account_name) {
    $.ajax({
	url: '/backend/answer/'+tweet_id+'?answer='+account_name,
	dataType: 'json',
	success: function(data) {
	    if(data.result){
		$('#buttons').html(
		    "<div class=\"alert alert-success\"><b>Correct!</b> You were right!</div>"
		);
	    } else {
		$('#buttons').html(
		    "<div class=\"alert alert-danger\"><b>Nope!</b> This answer was wrong<div>"
		);
	    }
	    setTimeout(function(){
		make_buttons();
		nexttweet();
	    }, 2500);
	}
    })
}

function nexttweet() {
    current_tweet = $.ajax({
	url: '/backend/get_random_tweet',
	dataType: 'json',
	success: function(data){
	    current_tweet = data
	    $('#tweet').html(current_tweet.text);
	},
    })
}

function make_buttons() {
    $("#buttons").html(
	"<a href=\"#\" class=\"btn btn-lg btn-default\" id=\"leftbtn\">@VICE</a> "+
	"<a href=\"#\" class=\"btn btn-lg btn-default\" id=\"rightbtn\">Satire</a>"
    );
    $("#leftbtn").click(function(){
	answer(current_tweet.id, 'VICE');
    });
    $("#rightbtn").click(function(){
	answer(current_tweet.id, 'Vice_Is_Hip');
    });
}

$('#startbtn').click(function(){
    nexttweet();
    make_buttons();
});
