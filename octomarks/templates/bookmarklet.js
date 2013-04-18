(function(){

    var URL = encodeURIComponent(location.href);
    var image = document.createElement('img');
    image.onload = function() {
        console.log('nice!!');
    };
    image.onerror = function() {
        console.log('error!');
    };
    image.src = '{{ full_url_for(".save_bookmark", token=user.gb_token) }}?uri='+encodeURIComponent(location.href)+'&should_redirect=1&time='+(new Date().getTime());
    
})();
