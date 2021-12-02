$( document ).ready(function() {
    var getUrl = window.location;
    var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
    var lowDate = new Date();
    lowDate.setDate(lowDate.getDate() - 4);
    var currentDate = new Date();
    $.getJSON(baseUrl + "/schedule.json").then(function (data) {
        var items = []
        $.each( data, function( key, game ) {
            var gameDate = new Date(game.iso);
            if (gameDate <= lowDate) {
                return;
            }

            var when = gameDate.getDate() + "/" + (gameDate.getMonth() + 1);
            if (gameDate >= currentDate) {
                when += " " + (gameDate.getHours() == 0 ? "00" : gameDate.getHours()) + ":" + (gameDate.getMinutes() == 0 ? "00" : gameDate.getMinutes());
            }

            row = "<tr><td class='text-end p-3 fs-5'>" + when + "</td><td class='p-3 fs-5'>" + game.visiting + " @ " + game.hosting + "</td></tr>";
            items.push(row);
        });
        $( "#games-list" ).append(items.join(''));
    });
});
