$( document ).ready(function() {
    $.getJSON("http://localhost:8000/schedule.json").then(function (data) {
        var items = []
        $.each( data, function( key, game ) {
            row = "<tr><td class='text-end p-3 fs-5'>" + game.when + "</td><td class='p-3 fs-5'>" + game.visiting + " @ " + game.hosting + "</td></tr>";
            items.push(row);
        });
        $( "#games-list" ).append(items.join(''));
    });
});
