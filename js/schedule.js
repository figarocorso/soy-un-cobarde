$( document ).ready(function() {
    $.getJSON("http://localhost:8000/schedule.json").then(function (data) {
        var items = []
        $.each( data, function( key, game ) {
            li_string = "<li>" + game.when + " | " + game.visiting + " | " + game.hosting + "</li>";
            items.push(li_string);
        });
        $( "#games-list" ).append(items.join(''));
    });
});
