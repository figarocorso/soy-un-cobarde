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

            var visiting = game.visiting.split(" ");
            var visitingName = visiting.pop();
            var visitingCity = visiting.join(" ");

            var hosting = game.hosting.split(" ");
            var hostingName = hosting.pop();
            var hostingCity = hosting.join(" ");

            row =  "<div class='d-flex bg-gradient bd-highlight align-middle mb-1 ps-3 " + colorClass + "'>";
            row +=     "<div class='w-25'><span class='py-3 px-1 float-end'>" + when + "</span></div>";
            row +=     "<img class='d-none d-md-block mx-1' height='60px' src='/images/teams/" + visitingName.toLowerCase() + ".png' />";
            row +=     "<span class='d-none d-md-block py-3 px-1'>" + visitingCity + "</span><span class='fw-bold py-3'>" + visitingName + "</span>";
            row +=     "<div class='px-2 py-3'>@</div>";
            row +=     "<span class='d-none d-md-block px-1 py-3'>" + hostingCity + "</span><span class='py-3 fw-bold'>" + hostingName + "</span>";
            row +=     "<img class='d-none d-md-block mx-1' height='60px' src='/images/teams/" + hostingName.toLowerCase() + ".png' />";
            row += "</div>";
            items.push(row);
        });

        $( "#games-list" ).append(items.join(''));
    });
});
