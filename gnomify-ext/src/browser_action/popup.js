chrome.tabs.query({'active': true}, function (tabs) {
    var url = tabs[0].url;
    console.log("hey");
    $('#savedLinks').html("hey");
});