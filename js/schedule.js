$( document ).ready(function() {
    var getUrl = window.location;
    var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
    console.log(baseUrl);
    $.getJSON(baseUrl + "/schedule.json").then(function (data) {
        var items = []
        $.each( data, function( key, game ) {
            row = "<tr><td class='text-end p-3 fs-5'>" + game.when + "</td><td class='p-3 fs-5'>" + game.visiting + " @ " + game.hosting + "</td></tr>";
            items.push(row);
        });
        $( "#games-list" ).append(items.join(''));
    });
});
