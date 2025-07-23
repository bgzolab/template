(function() {
    alert('unicorn!');
  })(); //called the moment it’s defined.


  (function () {
    var script = document.createElement('script');

    script.src = './bookmarklets.js' + "?" + new Date().getTime();// problem of browser caching

    document.body.appendChild(script);
  })();