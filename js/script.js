// ON PAGE READY
$( document ).ready(function() {
    updateTime();
    updateShoppingList();
    updateTrainSchedule();
    updateChores();
    updateGarbage();
    initializeWeather();
    checkDarkMode();

    setInterval(updateTime, 1000);
    setInterval(updateShoppingList, 3000);
    setInterval(updateTrainSchedule, 5000);
    setInterval(updateChores, 3000);
    setInterval(updateGarbage, 4000);
    
})

// UPDATE DATE AND TIME
function updateTime() {
    function checkTime(i) {
        return (i < 10) ? "0" + i : i;
    }
    var today = new Date();
    h = checkTime(today.getHours());
    m = checkTime(today.getMinutes());
    s = checkTime(today.getSeconds());
    weekday = today.toLocaleDateString('de', {weekday:'long'});
    day = today.toLocaleDateString('de', {day:'numeric'});
    month = today.toLocaleDateString('de', {month:'long'});

    $('#hours').html(h + ":" + m );
    $('#date').html(weekday + ", " + day + ". " + month);
    $('#seconds').html(s);

    // Reload Page at Day/Night change to adjust weather widget
    if (h == 7 && m == 0 && s == 3){
        turnOffNightMode();
        window.location.reload(true);
    }
    if (h == 17 && m == 0 && s == 3){
        turnOnNightMode();
        window.location.reload(true);
    }
}

// UPDATE CHORES
function updateChores(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        response = xhttp.responseText;
        var chores = JSON.parse(this.response);

        $('#garbage-who').html(chores.muell.dran);
        $('#glas-who').html(chores.glas.dran);
        $('#bathroom-who').html(chores.bad.dran);
        $('#kitchen-who').html(chores.kueche.dran);
        $('#vacuum-who').html(chores.saugen.dran);
        $('#towels-who').html(chores.handtuecher.dran);
        $('#curtains-who').html(chores.duschvorhang.dran);

        $('#garbage-who').parent().css("background-color", "#17a2b8"); // light blue
        $('#glas-who').parent().css("background-color", "#17a2b8"); // light blue

        calculateDueDate(selector="#bathroom-due", chores.bad.intervall_tage, chores.bad.tage_vergangen);
        calculateDueDate(selector="#kitchen-due", chores.kueche.intervall_tage, chores.kueche.tage_vergangen);
        calculateDueDate(selector="#vacuum-due", chores.saugen.intervall_tage, chores.saugen.tage_vergangen);
        calculateDueDate(selector="#towels-due", chores.handtuecher.intervall_tage, chores.handtuecher.tage_vergangen);
        calculateDueDate(selector="#curtains-due", chores.duschvorhang.intervall_tage, chores.duschvorhang.tage_vergangen);

        function calculateDueDate(selector, interval, days_passed){
            days_remaining = interval - days_passed;
            
            if (days_remaining > 1){
                $(selector).html("in " + days_remaining + " Tagen");
                $(selector).parent().css( "background-color", "#28a745" );
            } else if (days_remaining == 1){
                $(selector).html("morgen");
                $(selector).parent().css( "background-color", "#ffc107" );
            } else if (days_remaining == 0){
                $(selector).html("heute");
                $(selector).parent().css( "background-color", "#dc3545" );
            } else if (days_remaining == -1){
                $(selector).html("gestern");
                $(selector).parent().css( "background-color", "#dc3545" );
            } else {
                $(selector).html("seit " + String(days_remaining).substring(1) + " Tagen");
                $(selector).parent().css( "background-color", "#dc3545" );
            }
        }
        }
    };
    xhttp.open("GET", "data/putzplan.json", true);
    xhttp.send();
}

// UPDATE GARBAGE
function updateGarbage(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        response = xhttp.responseText;
        var garbage = JSON.parse(this.response);

        calculateDueDate(selector=".garbage-black", garbage.schwarz);
        calculateDueDate(selector=".garbage-blue", garbage.blau);
        calculateDueDate(selector=".garbage-green", garbage.gruen);
        calculateDueDate(selector=".garbage-yellow", garbage.gelb);

        function calculateDueDate(selector, days_remaining){
            if (days_remaining > 1){
                $(selector).html("in " + days_remaining + " Tagen");
                $(selector).css( "background-color", "#28a745" );
                $(selector + "-image").css( "background-color", "inherit");
            } else if (days_remaining == 1){
                $(selector).html("morgen");
                $(selector).css( "background-color", "#ffc107" );
                $(selector + "-image").css( "background-color", "#ffc107" );
                blink(selector + "-image")
            } else if (days_remaining == 0){
                $(selector).html("heute");
                $(selector).css( "background-color", "#dc3545" );
                $(selector + "-image").css( "background-color", "#dc3545" );
                blink(selector + "-image")
            }
        }

        function blink(selector){
            $(selector).fadeOut(2000, function(){
                $(this).fadeIn(2000, function(){
                    //blink(this);
                });
            });
        }
        }
    };
    xhttp.open("GET", "data/zaw.json", true);
    xhttp.send();
}

// UPDATE SHOPPING LIST
function updateShoppingList(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        response = xhttp.responseText;
        var shopping_list = JSON.parse(this.response);

        markup = ""
        shopping_list.liste.forEach(function(item){
            markup += "<tr><td>" + item + "</td></tr>";
        })

        $("#shopping table tbody tr").remove();
        $("#shopping table tbody").append(markup);
        }
    };
    xhttp.open("GET", "data/einkaufsliste.json", true);
    xhttp.send();
}

// UPDATE TRAIN SCHEDULE
function updateTrainSchedule(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        response = xhttp.responseText;
        var timetable = JSON.parse(this.response);
        
        // TRIP 1
        lines = "";
        timetable.trips[0].line.forEach(function(line){
            lines += line + ", ";
        });
        $('#trip1-lines').html(lines.slice(0, -2));
        $('#trip1-ab').html("ab: " + timetable.trips[0].ab);
        $('#trip1-tz').html("an: " + timetable.trips[0].tz);
        $('#trip1-an').html("an: " + timetable.trips[0].an);

        // TRIP 2
        lines = "";
        timetable.trips[1].line.forEach(function(line){
            lines += line + ", ";
        });
        $('#trip2-lines').html(lines.slice(0, -2));
        $('#trip2-ab').html("ab: " + timetable.trips[1].ab);
        $('#trip2-tz').html("an: " + timetable.trips[1].tz);
        $('#trip2-an').html("an: " + timetable.trips[1].an);

        // TRIP 3
        lines = "";
        timetable.trips[2].line.forEach(function(line){
            lines += line + ", ";
        });
        $('#trip3-lines').html(lines.slice(0, -2));
        $('#trip3-ab').html("ab: " + timetable.trips[2].ab);
        $('#trip3-tz').html("an: " + timetable.trips[2].tz);
        $('#trip3-an').html("an: " + timetable.trips[2].an);

        // TRIP 4
        lines = "";
        timetable.trips[3].line.forEach(function(line){
            lines += line + ", ";
        });
        $('#trip4-lines').html(lines.slice(0, -2));
        $('#trip4-ab').html("ab: " + timetable.trips[3].ab);
        $('#trip4-tz').html("an: " + timetable.trips[3].tz);
        $('#trip4-an').html("an: " + timetable.trips[3].an);

        // TRIP 5
        lines = "";
        timetable.trips[4].line.forEach(function(line){
            lines += line + ", ";
        });
        $('#trip5-lines').html(lines.slice(0, -2));
        $('#trip5-ab').html("ab: " + timetable.trips[4].ab);
        $('#trip5-tz').html("an: " + timetable.trips[4].tz);
        $('#trip5-an').html("an: " + timetable.trips[4].an);
        }
    };
    xhttp.open("GET", "data/timetable.json", true);
    xhttp.send();
}

// ADJUST WEATHER WIDGET COLOR TO DAY/NIGHT MODE
function initializeWeather() {
     var currentTime = new Date().getHours();
     if (0 <= currentTime&&currentTime < 7) {
         document.getElementById("weatherwid").setAttribute("data-theme", "dark");
     }
     if (7 <= currentTime&&currentTime < 17) {
         document.getElementById("weatherwid").setAttribute("data-theme", "orange");
     }
     if (17 <= currentTime&&currentTime <= 24) {
         document.getElementById("weatherwid").setAttribute("data-theme", "dark");
     }
     !function wid(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
}

// CHECK IF DARK MODE APPLIES AT PAGE LOAD
function checkDarkMode(){
    var today = new Date();
    hour = checkTime(today.getHours());

    if (hour < 7 && hour > 16){
        turnOnNightMode();
    }
}

function turnOnNightMode(){
    // MAIN CONTAINERS
    $("#top-container").css("background-color", "black");
    $("#bot-container").css("background-color", "black");
    $("#top-container").css("color", "white");
    $("#bot-container").css("color", "white");

    // CLOCK
    $("#clock").css("background-color", "gray");

    // TABLES
    $("table").addClass('table-dark');

    // SLIDER
    $(".slide").css("background-color", "black");
    $(".title").css("color", "white");
    $(".description").css("color", "white");
}

function turnOffNightMode(){
    // MAIN CONTAINERS
    $("#top-container").css("background-color", "white");
    $("#bot-container").css("background-color", "white");
    $("#top-container").css("color", "black");
    $("#bot-container").css("color", "black");

    // CLOCK
    $("#clock").css("background-color", "white");

    // TABLES
    $("table").removeClass('table-dark');

    // SLIDER
    $(".slide").css("background-color", "white");
    $(".title").css("color", "black");
    $(".description").css("color", "black");
}