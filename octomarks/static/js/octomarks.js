$(function(){
    function toggle_navbar (){
        var hiddenClass = "navbar-stashed";
        var $navbar = $(".navbar");
        var $navbarContents = $navbar.find(".profile,ul,img");

        if ($navbar.hasClass(hiddenClass)) {
            $navbarContents.animate({
                "opacity": "1"
            }, 500);
            $navbar.animate({
                "margin-top": "0px",
                "margin-bottom": "80px"
            }, 500, function(){
                $navbar.removeClass(hiddenClass);
            });
        } else {
            $navbarContents.animate({
                "opacity": "0"
            }, 500);
            $navbar.animate({
                "margin-top": "-40px",
                "margin-bottom": "40px"
            }, 500, function(){
                $navbar.addClass(hiddenClass);
            });
        }
    }
    $(".navbar-handle").on("click", function(e){
        toggle_navbar();
        return e.preventDefault();
    });
    toggle_navbar();
});
