
function range(m,n){
return Array.from(Array(n - m).keys()).map(v=>v+m).map(v=>v);
}


function dateFormat(date) {
        let month = date.getMonth() + 1;
        let day = date.getDate();
        let hour = date.getHours();
        let minute = date.getMinutes();
        let second = date.getSeconds();

        month = month >= 10 ? month : '0' + month;
        day = day >= 10 ? day : '0' + day;
        hour = hour >= 10 ? hour : '0' + hour;
        minute = minute >= 10 ? minute : '0' + minute;
        second = second >= 10 ? second : '0' + second;

        return date.getFullYear() + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}


function page_nation(review){

var pageHtml = ''
var rev = review[7] -1
if(review[7] -1 > 0){
pageHtml += '<li class="page-item" id="pageGo" data-page ="' + rev + '"><a class="page-link">< 뒤로</a></li>'
}

var range_for = range(review[7],review[8]+1)

for( i in range(review[7],review[8]+1)){

    if( range_for[i] > review[4] ){}
    else
    {
     if( range_for[i] == review[0]){
     pageHtml += '<li class="page-item active"><a class="page-link" href="#">'+ range_for[i] +'</a></li>'
     }
     else{
     pageHtml += '<li class="page-item" id="pageGo" data-page="' + range_for[i] + '"><a class="page-link">' + range_for[i] + '</a></li>'
     }
    }
}

var next = review[8] + 1

if(review[8]< review[4]){
pageHtml += '<li class="page-item" id="pageGo" data-page="' + next + '" ><a class="page-link">다음 ></a></li>'
}
return pageHtml;
}



function pageAjax(div,review_id,mid,page){
        var formData = new FormData();
        formData.append('ref',review_id);
        formData.append('ref_page',page);
        var return_ajax;
        $.ajax({
            type: 'POST',
            url:'/review_ajax',
            data:formData,
            contentType: false,
            processData: false,
            async: false,
            success: function(data){
            var innerHtml = '';
            var i = 1;
            return_ajax = data.ref_rev;
            var ref = data.ref_rev[2];
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
return return_ajax
}