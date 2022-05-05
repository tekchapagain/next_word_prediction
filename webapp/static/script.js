const log = document.getElementById('search');

function getKey(e) {
    var location = e.location;
    var selector;
    if (location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
        selector = ['[data-key="' + e.keyCode + '-R"]']
    } else {
        var code = e.keyCode || e.which;
        selector = [
            '[data-key="' + code + '"]',
            '[data-char*="' + encodeURIComponent(String.fromCharCode(code)) + '"]'
        ].join(',');
    }
    return document.querySelector(selector);
}

function pressKey(char) {
    var key = document.querySelector('[data-char*="' + char.toUpperCase() + '"]');
    if (!key) {
        return console.warn('No key for', char);
    }
    key.setAttribute('data-pressed', 'on');
    setTimeout(function() {
        key.removeAttribute('data-pressed');
    }, 200);
}


document.body.addEventListener('keydown', function(e) {
    var key = getKey(e);
    if (!key) {
        return console.warn('No key for', e.keyCode);
    }

    key.setAttribute('data-pressed', 'on');
});

document.body.addEventListener('keyup', function(e) {
    var key = getKey(e);
    key && key.removeAttribute('data-pressed');
});

function size() {
    var size = keyboard.parentNode.clientWidth / 90;
    keyboard.style.fontSize = size + 'px';
    console.log(size);
}

var keyboard = document.querySelector('.keyboard');
window.addEventListener('resize', function(e) {
    size();
});
size();

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  $(document).ready(function() {
      $("#f1").submit(function() {
        event.preventDefault();
        var csrftoken = getCookie('csrftoken');
        $.ajax("api/?q="+document.getElementById('transliterateTextarea').value,{
          method: "POST",
          headers: {'X-CSRFToken': csrftoken},
          mode: 'same-origin',
          data : JSON.stringify({"query":"text",
        }),
        success: function(data){
          console.log(data)},
          crossDomain: true,
          contentType: "application/json; charset=utf-8",
          dataType: "json"
      });

    });
  });

$(document).ready(function() {
    $("#f1").submit(function() {
        event.preventDefault();
      var csrftoken = getCookie('csrftoken');
      $.ajax("predicted/",{
        method: "GET",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
      success: function(res){
        document.getElementById('prediction1').innerHTML=res[0]['prediction']
        document.getElementById('prediction2').innerHTML=res[0]['prediction']},
        crossDomain: true,
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });

  });
});