function cloneYBDfield(link) {
  var wrap = link.parents(".control-group").find(".input-group:last-child"),
    input_data = wrap.children(':input,label').clone(),
    //input_year = wrap.find('.year-based-year').clone(),
    helptext = wrap.find(".helptext:last").clone(),
    remove_link = wrap.find("a.remove-ybd").clone(),
    prefix = input_data.attr("id");
  prefix = prefix.slice(0, prefix.lastIndexOf("_")+1);
  input_data.filter(':input').each(function () {
    $(this)
      .attr("id", prefix + (parseInt($(this).attr("id").replace(prefix, "")) + input_data.size()))
      .attr("name", prefix.slice(3) + (parseInt($(this).attr("name").replace(prefix.slice(3), "")) + input_data.size()))
      .val("");
  });
  //input_data.removeClass('form-control');
  //if (input_year.length > 0) {
  //  input_year.attr("id", prefix + (parseInt(input_year.attr("id").replace(prefix, ""))+2));
  //  input_year.attr("name", prefix.slice(3) + (parseInt(input_year.attr("name").replace(prefix.slice(3), ""))+2));
  //  input_year.val("");
  //}
  //input_year.removeClass('form-control');
  remove_link.css("display", "inline-block");
  remove_link.click(removeYBDfield);
  var new_wrap = $("<div class=\"input-group\"></div>");
  new_wrap.append(input_data);
  //new_wrap.append(input_year);
  new_wrap.append(helptext);
  new_wrap.append(remove_link);
  new_wrap = link.parents(".controls").append(new_wrap);
  new_wrap.find('.select2-hidden-accessible').select2();

  //link.next().show();
}

function removeYBDfield() {
  $(this).parent().remove();
}

function update_year_based_history (el, id) {
  var field = el.attr("id");
  $.get("/ajax/history/" + id, {field: field}, function (data) {
    el.html(data);
  });
};

$(document).ready(function () {
  $("a.history").click(function(e) {
    var id = $("input[name='deal_id']").val();
    update_year_based_history($(this).next("div"), id);
    e.preventDefault();
  });
  /* Overall: Quick placeholder for year-based data year field */
  $("input.year-based-year").prop("placeholder", "YYYY-MM-DD");
  $("input.year-based-is-current").after($('<label>' + 'Current' + '</label>'));

  $(".add-ybd").click(function () { cloneYBDfield($(this)); });
  $(".remove-ybd").click(function () { removeYBDfield($(this)); });
})
