$( document ).ready(function() {
    var getUrl = window.location;
    var baseUrl = getUrl .protocol + "//" + getUrl.host;
    console.log(baseUrl);
    var lowDate = new Date();
    lowDate.setDate(lowDate.getDate() - 4);
    var currentDate = new Date();
    $.getJSON(baseUrl + "/games/schedule.json").then(function (data) {
        var items = []
        $.each( data, function( key, game ) {
            var gameDate = new Date(game.iso);
            if (gameDate <= lowDate) {
                return;
            }

            var when = gameDate.getDate() + "/" + (gameDate.getMonth() + 1);
            var colorClass = "bg-warning text-black"
            if (gameDate >= currentDate) {
                when += " " + (gameDate.getHours() == 0 ? "00" : gameDate.getHours()) + ":" + (gameDate.getMinutes() == 0 ? "00" : gameDate.getMinutes());
                colorClass = "bg-primary text-white"
            }

            row =  "<div class='d-flex bg-gradient mb-1 bd-highlight " + colorClass + "'>";
            row +=     "<div style='min-width:120px;' class='w-25 p-1'><span class='float-end'>" + when + "</span></div>";
            row +=     "<div class='w-75 p-1'>" + game.visiting + " @ " + game.hosting + "</div>";
            row += "</div>";
            items.push(row);
        });
        $( "#games-list" ).append(items.join(''));
    });
});
