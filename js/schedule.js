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

            row =  "<div class='d-flex bg-gradient mb-1 bd-highlight ps-3 py-2 align-middle " + colorClass + "'>";
            row +=     "<div style='min-width:120px;' class='w-25 p-1'><span class='float-end'>" + when + "</span></div>";
            row +=     "<div class='ps-3 p-1 d-flex justify-content-start'><span class='d-none d-md-block px-1'>" + visitingCity + "</span><span class='fw-bold'>" + visitingName + "</span></div>";
            row +=     "<div class='p-1'>@</div>";
            row +=     "<div class='p-1 d-flex justify-content-start'><span class='d-none d-md-block px-1'>" + hostingCity + "</span><span class='fw-bold'>" + hostingName + "</span></div>";
            row += "</div>";
            items.push(row);
        });

        $( "#games-list" ).append(items.join(''));
    });
});
