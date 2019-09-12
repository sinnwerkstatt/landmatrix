$(document).ready(function () {

  /* Browse: Disable all subchecks by default */
  $("body#add span.input-append ul li ul li label input:checkbox, body#browse span.input-append ul li ul li label input:checkbox").prop("disabled" , true);

  /* Browse: Update hidden field with current tab */
  $("#browse .rule-links a").click(function () {
    $(":input[name=current-form]").val($(this).attr("href").substr(1));
  }).filter("[href=#"+$(":input[name=current-form]").val()+"]").click();

  /* Browse: Select all checkbox */
  $(":checkbox[name^=select-all]").click(function() {
      $(this).parents("li.field").find("ul li :checkbox").prop("checked", this.checked);
  });
});

function update_widget (el, key_id, form) {
  var value = form.find("input[type='hidden']").val(),
      name = el.find(":input").attr("name"),
      op = el.parents(".field").prev().find("option:selected").val();
  // year based fields delete suffix (e.g. _0)
  name = name.replace(/_\d+$/, "");
  $.get("/ajax/widget/" + doc_type + "/", {key_id:  key_id, value: value, name: name, operation: op}, function (data) {
    el.html(data);
  });
};
