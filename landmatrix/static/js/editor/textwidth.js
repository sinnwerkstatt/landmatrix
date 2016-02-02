$.fn.textWidth = function(text){
    var org = $(this);
    var html = $('<span style="position:absolute;width:auto;left:-9999px">' + (text || org.html()) + '</span>');
    if (!text) {
        html.css("font-family", org.css("font-family"));
        html.css("font-size", org.css("font-size"));
    }
    $('body').append(html);
    var width = html.width();
    html.remove();
    return width;
}

$(document).ready(function () {
    // Set width of headings to make them horizontally centerable
    $("h1.separator span").each(function () {
        $(this).css("width", $(this).textWidth()+80);
    });
    $("h2.separator span").each(function () {
        $(this).css("width", $(this).textWidth()+30);
    });
});