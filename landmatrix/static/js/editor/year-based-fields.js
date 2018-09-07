function cloneYBDfield(link) {
  link = $(link);
  var container = link.parents(".controls"),
      field = container.find(".input-group:last-child"),
      data = field.children(":not(a,.select2)").clone(),
      remove_link = field.find("a.remove-ybd").clone();
  data.filter(':checkbox').prop('checked', false);
  var new_field = $("<div class=\"input-group\"></div>");
  new_field.append(data);
  remove_link.css("display", "inline-block");
  new_field.append(remove_link);
  link.parents(".controls").append(new_field);
  new_field.find('.select2-hidden-accessible').select2();
  new_field.find('.remove-ybd').click(function () { removeYBDfield(this); });
  new_field.find(':input').val("");
  renumberYBDInputs(container);
}

function removeYBDfield(link) {
  link = $(link);
  var container = link.parents(".controls");
  link.parents('.input-group').remove();
  renumberYBDInputs(container);
}

function renumberYBDInputs(container) {
  container = $(container);
  var inputs = container.find(':input'),
      counter = 0,
      prefix = inputs.first().attr("name");
  prefix = prefix.slice(0, prefix.lastIndexOf("_")+1);
  inputs.each(function () {
    $(this)
      .attr("id", "id_" + prefix + counter)
      .attr("name", prefix + counter);
    counter++;
  });
}

$(document).ready(function () {
  $("input.year-based-year").prop("placeholder", "YYYY-MM-DD");
  $("input.year-based-is-current").after($('<label>' + 'Current' + '</label>'));

  $(".add-ybd").click(function () { cloneYBDfield(this); });
  $(".remove-ybd").click(function () { removeYBDfield(this); });
})
