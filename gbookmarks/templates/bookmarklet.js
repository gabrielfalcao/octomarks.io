(function(){
    if (!($ = window.jQuery)) { // typeof jQuery=='undefined' works too
        script = document.createElement( 'script' );
        script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
        script.onload=save_bookmark;
        document.body.appendChild(script);
    }
    else {
        save_bookmark();
    }

    function save_bookmark() {
        var URL = encodeURIComponent(location.href);
        location.href='{{ full_url_for(".save_bookmark", token=user.gb_token) }}?uri='+encodeURIComponent(location.href)+'&should_redirect=1&time='+(new Date().getTime());
    }
})()