function startTimer(e){timeInSecs=parseInt(e)-1,ticker=setInterval('tick()',1e3)}function tick(){var e=timeInSecs;e>0?timeInSecs--:clearInterval(ticker),document.getElementById('countdown').innerHTML=e}var timeInSecs,ticker;startTimer(5);

	function disableLink(e) {
    e.preventDefault();
};

window.onload = function() {
    // Bind above event handler to all anchors
    var els = document.getElementsByTagName('a');
    [].forEach.call(els, function(el, i) {
        el.addEventListener("click", disableLink);
    });
    // Remove it in 5 seconds
    setTimeout(function() {
        var els = document.getElementsByTagName('a');
        [].forEach.call(els, function(el, i) {
            el.removeEventListener("click", disableLink);
        });
    }, 5000);
};

	// var browser = null;

	// if (bowser.firefox){
	//   var browser = "Firefox";
	// } else if (bowser.chrome){
	//   var browser = "Chrome"
	// };

 //    $.ajax({
	//     url: '/analytics/browser',
	//     type: 'POST',
	//     data: {"original_url": browser},
	//     success: function () {},
	//     dataType: 'json'
 //  	});   
$(function () {
    $('#container').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45
            }
            // marginRight: 1000
        },
        title: {
            text: 'Browser Shares'
        },
        // subtitle: {
        //     text: 'The browser that has clicked this gnome the most...'
        // },
        exporting: { 
        	enabled: false 
        },
        credits: {
      		enabled: false
  		},
        plotOptions: {
            pie: {
                innerSize: 100,
                depth: 45
            }
        },
        series: [{
            name: 'Clicks',
            data: [
                ['Firefox', {{ff_clicks}}],
                ['Chrome', {{chrome_clicks}}],
                ['Internet Explorer', {{ie_clicks}}],
                ['Opera', {{opera_clicks}}],
                ['Safari', 3],
                ['Tor', 4],
                ['Other', 1],
            ]
        }]
    });
});