var firstIndex = 1;
var seccondIndex = 101;
var therdIndex = 201;

function randomNum(min, max){
var randNum = Math.floor(Math.random()*(max-min+1)) + min;
return randNum; }


function clicker(){
 var id = document.getElementById(firstIndex)
 var per = document.getElementById("percentage").innerText
 var random = randomNum(0,100)
 if(random <= parseInt(per)){
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

 firstIndex++

}

function clicker2(){
 var id = document.getElementById(seccondIndex)
 var per = document.getElementById("percentage").innerText
 var random = randomNum(0,100)
 if(random <= parseInt(per)){
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

function clicker3(){
 var id = document.getElementById(therdIndex)
 var per = document.getElementById("percentage").innerText
 var random = randomNum(0,100)
 if(random <= parseInt(per)){
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