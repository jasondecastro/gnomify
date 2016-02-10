var express = require('express');
var router = express.Router();
var Firebase = require("firebase");
var bodyParser = require('body-parser');
var ref = new Firebase("https://radiant-inferno-9779.firebaseio.com/");

/*myFirebaseRef.child("original_link").on("value", function(snapshot) {
  var link = snapshot.val()
});*/

/* GET home page. */
router.get('/', function(req, res, next){
  res.render('index.html');
});

router.get('/about', function(req, res, next){
  res.render('about.html');
});

router.get('/documentation', function(req, res, next){
  res.render('documentation.html');
});

router.get('/privacy', function(req, res, next){
  res.render('privacy.html');
});

router.get('/terms', function(req, res, next){
  res.render('terms.html');
});

router.post('/getLinks', function(req, res, next){
   console.log(req.body)
   ref.push({"links": {'original_url': req.body.original_url, 'short_url': req.body.short_url}});
});

router.all('/:short_url', function(req, res, next){

   ref.once('value', function (snapshot) {
        var correctLink;
        snapshot.forEach(function (childSnapshot) {
            var name = childSnapshot.key();
            var childData = childSnapshot.val();
            var originalLink = "http://" + childData["links"]["original_url"]
            var hashedLink = childData["links"]["short_url"]
            if (hashedLink == req.params.short_url) {
              console.log("")
              console.log(hashedLink)
              console.log("Accessing " + originalLink)
              console.log("")
              correctLink = originalLink;
            }
            // console.log(name); // unique id
            // console.log(childData["links"]["short_url"]); // actual data
            // console.log("");
        });
        return res.redirect(correctLink || "http://carlyfiorina.org/");
    });

});

/*

*/

module.exports = router;