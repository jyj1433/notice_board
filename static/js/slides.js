var slideIndex = 0;
showDivs(slideIndex);
carousel()

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function currentDiv(n) {
    var x = document.getElementsByClassName("display-container mySlides");
    var d = document.getElementsByClassName("dot");
    for (i = 0; i < x.length; i++) {
       d[i].style.fontWeight = "400";
    }
    d[n-1].style.fontWeight = "bold";
    showDivs(slideIndex = n);
}

// 자동 슬라이드쇼 함수
function carousel() {
    var i;
    var x = document.getElementsByClassName("display-container mySlides");
    var d = document.getElementsByClassName("dot");

    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";
    }
    slideIndex++;

    if (slideIndex > x.length) {slideIndex = 1; d[x.length-1].style.fontWeight = "400";}
    if (slideIndex > 1) {d[slideIndex-2].style.fontWeight = "400";}
    x[slideIndex-1].style.display = "block";
    d[slideIndex-1].style.fontWeight = "bold";
    setTimeout(carousel, 5000); // Change image every 2 seconds
}

// 슬라이드 쇼 setup 함수
function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("display-container mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > x.length) {slideIndex = 1}
    if (n < 1) {slideIndex = x.length} ;
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" w3-red", "");
    }
    x[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " w3-red";
}



