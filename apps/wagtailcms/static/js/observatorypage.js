$(function () {
  let region_dd = $(".region-or-country #id_region");
  let country_dd = $(".region-or-country #id_country");
  region_dd.change((ev) => {
    if (ev.target.value) {
      country_dd.val("");
    }
  });
  country_dd.change((ev) => {
    if (ev.target.value) {
      region_dd.val("");
    }
  });
});
