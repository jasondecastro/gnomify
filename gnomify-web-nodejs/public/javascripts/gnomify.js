$(".btn1").click(function(e) {
    // var rotation = function (){
    //    $("#Layer_1").rotate({
    //       angle:0, 
    //       animateTo:360, 
    //       callback: rotation,
    //       easing: function (x,t,b,c,d){        // t: current time, b: begInnIng value, c: change In value, d: duration
    //           return c*(t/d)+b;
    //       }
    //    });
    // }
    // rotation();
  var inputValue1 = $('#username').val().replace("http://","")
  var inputValue = $('#username').val().replace("https://","")


  var hashedURL = CryptoJS.MD5(inputValue).toString().split("").splice(1, 4).join("")
  $('#output').html("http://localhost:3000/" + hashedURL);

  var randomIndex = Math.floor(Math.random()*11).toString();
  $("#finalOutput").html("Your link: <a target='_blank' href='http://localhost:3000/" + hashedURL + "'>http://localhost:3000/" + hashedURL + "</a> <button class='btn btn1 btn-primary' style='background-color: #b73a39;  -moz-border-radius:75px; -webkit-border-radius: 75px;'><span style='padding:0px'><i class='fa fa-clipboard'></i></span></button>");
    $.ajax({
        url: '/getLinks',
        type: 'POST',
        data: {"original_url": inputValue, "short_url": hashedURL},
        success: function () {},
        dataType: 'json'
    });

  e.preventDefault();
 });