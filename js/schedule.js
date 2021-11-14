$( document ).ready(function() {
    $.getJSON("http://localhost:8000/schedule.json").then(function (data) {
        var items = []
        $.each( data, function( key, game ) {
            row = "<tr class='py-5 my-5'><td>" + game.when + "</td><td>" + game.visiting + "</td><td>" + game.hosting + "</td></tr>";
            items.push(row);
        });
        $( "#games-list" ).append(items.join(''));
    });
});
