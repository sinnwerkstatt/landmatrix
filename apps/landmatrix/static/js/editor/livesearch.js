var init_livesearch = function (el) {
    el = $(el); // link
    el.click(function (e) {
      e.preventDefault();
      el.parent().find("ul").show();
      return false;
    });
    var parent = el.parent(); // parent = li
    parent.children(".livesearch-active").text(parent.find("ul li a.active").text());
    parent.find("ul li a").click(function (e) {
      e.preventDefault();
      var ul = $(this).parents(".form ul");
      ul.find("li a.active").removeClass("active");
      $(this).addClass("active");
      parent.children(".livesearch-active").text($(this).text() || "&nbsp;");
      parent.children("input").val($(this).attr("href").substr(1));
      ul.hide();
      return false;
    });
}

$(document).ready(function () {
    /* Investor select  */
    $("a.new-investor,a.existing-investor").click(function (e) {
        e.preventDefault();
        $(".form:not(.empty) a.livesearch").each(function () { init_livesearch(this); });
        return false;
    });
});
