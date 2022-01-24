var firstIndex = 1;
var secondIndex = 101;
var thirdIndex = 201;
var sus1 = 0
var sus2 = 0
var sus3 = 0

function randomNum(min, max){
var randNum = Math.floor(Math.random()*(max-min+1)) + min;
return randNum; }

function clicker(){
    var id = document.getElementById(firstIndex)
    var per = document.getElementById("percentage").innerText
    var random = randomNum(0,100)
    if(firstIndex <= 10){
        if(random <= parseInt(per)){
            sus1++
            document.getElementById("sus1").innerText = sus1 + '번 성공'
            id.src = "static/image/성공.PNG"
            if(25 == parseInt(per)){}
            else{
                document.getElementById("percentage").innerText = parseInt(per)-10
            }
        }
        else{
            id.src = "static/image/실패.PNG"
            if(75 == parseInt(per)){}
            else{
                document.getElementById("percentage").innerText = parseInt(per)+10
            }
        }
    }
    firstIndex++
}

function clicker2(){
    var id = document.getElementById(secondIndex)
    var per = document.getElementById("percentage").innerText
    var random = randomNum(0,100)
    if(secondIndex <= 110){
        if(random <= parseInt(per)){
            sus2++
            document.getElementById("sus2").innerText = sus2 + '번 성공'
            id.src = "static/image/성공.PNG"
            if(25 == parseInt(per)){}
            else{
                document.getElementById("percentage").innerText = parseInt(per)-10
            }
        }
        else{
            id.src = "static/image/실패.PNG"
            if(75 == parseInt(per)){}
            else{
                document.getElementById("percentage").innerText = parseInt(per)+10
            }
        }
        secondIndex++
    }
}

function clicker3(){
    var id = document.getElementById(thirdIndex)
    var per = document.getElementById("percentage").innerText
    var random = randomNum(0,100)
    if(thirdIndex <= 210){
        if(random <= parseInt(per)){
            sus3++
            document.getElementById("sus3").innerText = sus3 + '번 성공'
            id.src = "static/image/감소성공.PNG"
            if(25 == parseInt(per)){}
            else{
                document.getElementById("percentage").innerText = parseInt(per)-10
            }
        }
        else{
            id.src = "static/image/실패.PNG"
            if(75 == parseInt(per)){}
            else{
                document.getElementById("percentage").innerText = parseInt(per)+10
            }
        }
        thirdIndex++
    }
}

$(".pageGo").click(function(){
			page = $(this).attr("data-page");
		    pageAjax(div,review_id,mid)
)}

function page_nation(review){
var pageHtml = ''
if(review[7] -1 > 0){
pageHtml += '<li class="page-item"><a class="page-link">< 뒤로</a></li>'
}

for( i in range(review[7],review[8]+1)){
    if( i > review[4] ){}
    else
    {
     if( i == review[0]){
     pageHtml += '<li class="page-item active"><a class="page-link" href="#">'+ i +'</a></li>'
     }
     else{
     pageHtml += '<li class="page-item" id="pageGo" data-page="' + i + '"><a class="page-link">' + i + '</a></li>'
     }
    }
}

if(review[8]< review[4]){
pageHtml += '<li class="page-item"><a class="page-link">다음 ></a></li>'
}

return pageHtml;
}


function pageAjax(div,review_id,mid){
        var formData = new FormData();
        formData.append('ref',ref_id);
        $.ajax({
            type: 'POST',
            url:'/review_ajax',
            data:formData,
            contentType: false,
            processData: false,
            success: function(data){
            var innerHtml = '';
            var i = 1;
            var ref = data.ref_rev[2]
            for(value in data.ref_rev[2]){
                innerHtml += '<b>'+ref[value][0]+'</b><br>'+
                                '<span>&nbsp&nbsp&nbsp'+ref[value][3]+'</span><br>'+
                                '<span class="review-date">'+ dateFormat(new Date(ref[value][4])) +'</span>';
                if(mid == ref[value][2]){
                innerHtml +=  '<i class="fas fa-times float-right" style="color:red; cursor:pointer; position:relative; left:12px;" onclick="review_del('+ref[value][1]+')">'
                             +'</i>';
                }
                innerHtml += '<hr>';
            }
            div.html(innerHtml);
            },
            error:function(error){
            alert('오류'+error);
            }
        });

}