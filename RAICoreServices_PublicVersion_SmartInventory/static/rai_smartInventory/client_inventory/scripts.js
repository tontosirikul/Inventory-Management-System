function smoothScroll(target, duration) {
    var target = document.querySelector(target);
    var targetPosition = target.getBoundingClientRect().top;
    var startPosition = window.pageYOffset;
    var distace = targetPosition - startPosition;
    var startTime = null;

    function animation(currentTime) {
        if(startTime === null) startTime = currentTime;
        var timeElapsed = currentTime - startTime;
        var run = ease(timeElapsed, startPosition, distace, duration);
        window.scrollTo(0, run);
        if(timeElapsed < duration) requestAnimationFrame(animation);
    }

    function ease(t, b, c, d) {
        t /= d/2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation)
}

var section1 = document.querySelector('.menu__link');

section1.addEventListener('click', function (params) {
    smoothScroll('.content', 1000);
});

var prevScrollpos = "0";
var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var currentScrollpos = window.pageYOffset;
    if((prevScrollpos > currentScrollpos)||(prevScrollpos < "0")){
        document.getElementById("navbar").style.top = "0";
    } else{
        document.getElementById("navbar").style.top = "-100px";
    }
    prevScrollpos = currentScrollpos;
}

function goBack() {
    window.history.back();
}