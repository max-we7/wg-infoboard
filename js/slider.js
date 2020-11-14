$(document).ready(function(){
    $('.slider').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 4000,
        arrows: false,
    });
    newsRequest();
    setInterval(newsRequest, 3600000);
  });

function newsRequest(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        newsfeed = xhttp.responseText;
        addAllArticles(newsfeed)
        }
    };
    xhttp.open("GET", "data/newsfeed.xml", true);
    xhttp.send();
}

function addAllArticles(data){
    $('.slider').slick('slickRemove', null, null, true);
    $(data).find("item").each(function() {
        let link = $(this).find("photo").text();
        let title = $(this).find("title").text();
        let description = $(this).find("description").text()

        const template = `<div class="slide"><div class="image"><img src="` + link +
        `" alt=""></div><div class="content"><div class="title">` + title + 
        `</div><div class="description">` + description + `</div></div></div>`;

        $('.slider').slick('slickAdd', template);
    });  
}