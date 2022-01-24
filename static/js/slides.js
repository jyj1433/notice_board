var slideIndex = 0; // 처음 시작할 슬라이드 번호 설정
var x = document.getElementsByClassName("display-container mySlides");
var d = document.getElementsByClassName("dot");
currentSlides(slideIndex);
carousel()

function currentSlides(n) {
    // dot을 선택했을 때 해당 슬라이드를 보여주는 함수. 매개변수는 slideIndex
    // 자동 슬라이드 함수에서도 이 함수를 불러오게 됨
    // 처음 슬라이드 setup 때도 이 함수를 사용. 시작 때 보여줄 슬라이드 번호를 매개변수로 주고 호출

    slideIndex = n // 선택된 dot을 현재 slideIndex로 변경
    if (slideIndex > x.length) {slideIndex = 1} // 인덱스가 슬라이드 개수보다 커지면 첫 번째 슬라이드로 돌아옴 (마지막 슬라이드인데 오른쪽 눌렀을 경우)
    else if(slideIndex < 1) {slideIndex = x.length} // 인덱스가 첫 번째보다 앞으로 가면 인덱스를 마지막 슬라이드로 보냄 (첫 슬라이드인데 왼쪽 눌렀을 경우)

    for (var i = 0; i < x.length; i++) { // 모든 슬라이드를 돌면서
        x[i].style.display = "none"; // 전부 안보이게 함
    }
    for (var i = 0; i < x.length; i++) { // 모든 슬라이드 돌면서
       d[i].style.fontWeight = "400"; // dot 강조 전부 해제
    }

    x[slideIndex-1].style.display = "block"; // 선택된 슬라이드 보이게 하고
    d[slideIndex-1].style.fontWeight = "bold"; // 선택된 dot 강조하고 완료
}

function plusSlides(n) { // prev, next 함수
    slideIndex += n // 왼쪽, 오른쪽 인디케이터를 누르면 인덱스에 -1 이나 1 이 더해짐
    currentSlides(slideIndex);
}

function carousel() { // 자동 슬라이드쇼 함수
    slideIndex++;
    currentSlides(slideIndex);
    setTimeout(carousel, 5000); // 정해진 시간마다 자신을 다시 호출 (1000 = 1초)
}
