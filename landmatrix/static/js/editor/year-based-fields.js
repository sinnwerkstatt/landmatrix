function cloneYBDfield(link) {
  var wrap = link.parents(".field").find(".input-append:last"),
    inputs = wrap.find(":input"),
    input_data = $(inputs[inputs.size()-2]).clone(),
    input_year = $(inputs[inputs.size()-1]).clone(),
    helptext = wrap.find(".helptext:last").clone(),
    remove_link = wrap.find("a.remove-ybd").clone(),
    prefix = input_data.attr("id");
  prefix = prefix.slice(0, prefix.lastIndexOf("_")+1);
  input_data.attr("id", prefix + (parseInt(input_data.attr("id").replace(prefix, ""))+2));
  input_data.attr("name", prefix.slice(3) + (parseInt(input_data.attr("name").replace(prefix.slice(3), ""))+2));
  input_data.val("");
  input_data.removeClass('form-control');
  input_year.attr("id", prefix + (parseInt(input_year.attr("id").replace(prefix, ""))+2));
  input_year.attr("name", prefix.slice(3) + (parseInt(input_year.attr("name").replace(prefix.slice(3), ""))+2));
  input_year.val("");
  input_year.removeClass('form-control');
  remove_link.css("display", "inline-block");
  remove_link.click(function () { removeYBDfield($(this)); });
  var button_wrap = $("<span class=\"input-group-btn\">");
  button_wrap.append(remove_link);
  var new_wrap = $("<div class=\"input-group\"></div>");
  new_wrap.append(input_data);
  new_wrap.append(input_year);
  new_wrap.append(helptext);
  new_wrap.append(button_wrap);
  link.parents(".field").find("td").append(new_wrap);
  //link.next().show();
}

function removeYBDfield(link) {
  len = link.parents(".field").find(".input-group").length;
  console.log($(this));
  if (len >= 1) {
    link.parents(".input-group").remove();
  }
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
  $("input.year-based-year").prop("placeholder","Year");

  $(".add-ybd").click(function () { cloneYBDfield($(this)); });
  $(".remove-ybd").click(function () { removeYBDfield($(this)); });
})
