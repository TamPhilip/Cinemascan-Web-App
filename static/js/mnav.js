var navWrap = $('#navWrap'),
    nav = $('nav'),
    pred = $(document.getElementsByClassName('title')[0]);
    startPosition = navWrap.offset().top;
    // stopPosition = $('#stopHere').offset().top - nav.outerHeight();

$(document).scroll(function () {
    //stick nav to top of page
    var y = $(this).scrollTop();

    if (y > startPosition) {
        nav.addClass('sticky');
        pred.css({top:'100px'});
    } else {
        pred.css({top:'5%'});
        nav.removeClass('sticky');
    }
});