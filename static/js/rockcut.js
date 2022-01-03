var firstIndex = 1;
var seccondIndex = 101;
var therdIndex = 201;
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
 var id = document.getElementById(seccondIndex)
 var per = document.getElementById("percentage").innerText
 var random = randomNum(0,100)
 if(seccondIndex <= 110){
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

 seccondIndex++
 }

}

function clicker3(){
 var id = document.getElementById(therdIndex)
 var per = document.getElementById("percentage").innerText
 var random = randomNum(0,100)
 if(therdIndex <= 210){
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

 therdIndex++
}
}