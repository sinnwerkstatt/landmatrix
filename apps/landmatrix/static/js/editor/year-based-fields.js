function initYBDfieldNoSelect(container) {
  // Prevent multiple selection of current checkboxes
  container.find('.year-based-is-current').click(function () {
    var checkbox = $(this);
    if (checkbox.is(':checked')) {
      // Uncheck other checkboxes
      checkbox.parents('.controls').find(':checkbox:not(#' + checkbox.attr('id') + ')').attr('checked', false);
    }
  });
}

function initYBDfield(container) {
  container.find('select:not(.select2-hidden-accessible)').select2();
  container.find('.remove-ybd').click(removeYBDfield);

  // Prevent multiple selection of current checkboxes
  container.find('.year-based-is-current').click(function () {
    var checkbox = $(this);
    if (checkbox.is(':checked')) {
      checkbox.parents('.controls').find(':checkbox:not(#' + checkbox.attr('id') + ')').attr('checked', false);
    }
  });
}

function cloneYBDfield() {
  var field = $(this).parents(".input-group");

  var container = field.parents(".controls");

  var data = field.children(":not(a,.select2)").clone();

  data.filter(':checkbox').prop('checked', false);
  data.filter("select").removeClass("select2-hidden-accessible").removeData("select2-id");

  var new_field = $('<div class="input-group"></div>').append(data);

  var removeLink = field.find("a.remove-ybd").clone().css("display", "inline-block");
  removeLink.appendTo(new_field);

  container.append(new_field);

  renumberYBDInputs(container);
  initYBDfield(container);
}

function removeYBDfield() {
  var link = $(this);
  var container = link.parents(".controls");
  link.parents('.input-group').remove();
  renumberYBDInputs(container);
}

function renumberYBDInputs(container) {
  var inputs = container.find(':input:not([type=search])');
  var prefix = inputs.first().attr("name");
  prefix = prefix.slice(0, prefix.lastIndexOf("_")+1);

  var counter = 0;
  inputs.each(function () {
    $(this)
      .attr("id", "id_" + prefix + counter)
      .attr("name", prefix + counter);
    counter++;
  });
}

$(function () {
  $("input.year-based-year").prop("placeholder", "YYYY-MM-DD");
  $("input.year-based-is-current").after($('<label>' + 'Current' + '</label>'));

  $(".add-ybd").click(cloneYBDfield);
  $(".remove-ybd").click(removeYBDfield);
  initYBDfieldNoSelect($('.year-based').parents('.controls'));
});
