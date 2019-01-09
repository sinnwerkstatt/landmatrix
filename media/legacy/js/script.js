$(document).ready(function(){

/* ADD/CHANGE DEAL */

/* Overall: Disable all subchecks by default */
$("body#add span.input-append ul li ul li label input:checkbox, body#browse span.input-append ul li ul li label input:checkbox").prop("disabled" , true);
/* Overall: Enable them again on checking the parent input */
$("input#id_general_information-intention_0,input#id_general_information-intention_1,input#id_water-source_of_water_extraction_1").click(function(){
    if($(this).is(":checked")) {
      $(this).parent().parent().children("ul").find("input:checkbox").prop("disabled",false);
    }
    else {
      $(this).parent().parent().children("ul").find("input:checkbox").prop("disabled",true).prop("checked",false);
    }
  });

/* Overall: Deselecting radio buttons */
$(":radio").click( function(e){
    var itsOn = $(this).hasClass("on");
    $(":radio[name="+ this.name + "]").removeClass("on");
    if(itsOn){
      $(this).removeAttr('checked');
      $(this).siblings().filter("[value='']").attr('checked', true);
    } else {
      $(this).addClass("on");
    }
  }).filter(":checked").addClass("on");

/* Overall: Quick placeholder for year-based data year field */
$("input.year-based-year").prop("placeholder","Year");

/* Overall: Removing text from labels where needed */
$("li.intention, li.nature, li.negotiation_status, li.agreement_duration, li.implementation_status, li.contract_farming, li.community_reaction, li.community_consultation, li.community_compensation, li.community_benefits, li.land_owner, li.land_use, li.land_cover, li.water_extraction_envisaged, li.source_of_water_extraction li.tg_how_much_do_investors_pay_comment, li.source_of_water_extraction, li.lease_type, li.on_the_lease_farmers, li.on_the_lease_area, li.off_the_lease_farmers, li.off_the_lease_area").children("label").html('&nbsp;');

/* Overall: Disable checkboxes on "change" pages */
if($("input#id_general_information-intention_0, input#id_general_information-intention_1, input#id_water-source_of_water_extraction_1").is(":checked")) {
  $("input#id_general_information-intention_0:checked, input#id_general_information-intention_1:checked, input#id_water-source_of_water_extraction_1:checked").parent().parent().children("ul").find("input:checkbox").prop("disabled",false);
}
else {
  $("input#id_general_information-intention_0, input#id_general_information-intention_1, input#id_water-source_of_water_extraction_1").parent().parent().children("ul").find("input:checkbox").prop("disabled",true);
}

/* Spatial Data: Set zoom level */
$('#id_location-location').keyup(function (){
  map.setZoom(8);
});

/* Data sources: Hide fields if option not selected */
$("select[id*=data_sources]").each(function(){
	if ( $(this).find("option:eq(5), option:eq(6)").is(":selected") ){
	$(this).parents(".form").find("li.name, li.company, li.email, li.phone").show();
}
});
/* Data sources: Show fields based on selection */
$("select[id*=data_sources]").change(function (){
	if ( $(this).find("option:eq(6), option:eq(5)").is(":selected") ){
		$(this).parents(".form").find("li.name, li.company, li.email, li.phone").slideDown("fast");
	}
	else {
		$(this).parents(".form").find("li.name, li.company, li.email, li.phone").slideUp("fast");
	}
});
/* Data sources: Enable hide-show for new boxes */
$("a#add-data-source").click(function (){
	$("select[id*=data_sources]").change(function (){
		if ( $(this).find("option:eq(6), option:eq(5)").is(":selected") ){
			$(this).parents(".form").find("li.name, li.company, li.email, li.phone").slideDown("fast");
		}
		else {
			$(this).parents(".form").find("li.name, li.company, li.email, li.phone").slideUp("fast");
		}
	});
});

/* General information: Leasing fees area only visible if "for specified area" is selected */
$("li.annual_leasing_fee_area, li.purchase_price_area").css("display","none");
$("select#id_general_information-purchase_price_type").change(function (){
	if ( $(this).find("option:eq(2)").is(":selected") ){
		$("li.purchase_price_area").slideDown("fast");
	}
	else {
		$("li.purchase_price_area").slideUp("fast");
		$("li.purchase_price_area span input").val("");
	}
});
$("select#id_general_information-annual_leasing_fee_type").change(function (){
	if ( $(this).find("option:eq(2)").is(":selected") ){
		$("li.annual_leasing_fee_area").slideDown("fast");
	}
	else {
		$("li.annual_leasing_fee_area").slideUp("fast");
		$("li.annual_leasing_fee_area span input").val("");
	}
});

/* General information: Contract farming everything invisible until "Yes" selected */
if( !$("input#id_general_information-contract_farming_0").is(":checked") ){
	$("li.on_the_lease, li.off_the_lease, li.lease_type, li.on_the_lease_area, li.on_the_lease_farmers, li.off_the_lease_area, li.off_the_lease_farmers").css("display", "none");
}
$("input#id_general_information-contract_farming_0").click(function (){
	if ( $(this).is(":checked")){
		$("li.on_the_lease, li.off_the_lease, li.lease_type, li.on_the_lease_area, li.on_the_lease_farmers, li.off_the_lease_area, li.off_the_lease_farmers").slideDown("fast");
	}
	else {
		$("li.on_the_lease, li.off_the_lease, li.lease_type, li.on_the_lease_area, li.on_the_lease_farmers, li.off_the_lease_area, li.off_the_lease_farmers").slideUp("fast");
	}
});
$("input#id_general_information-contract_farming_1").click(function (){
	$("li.on_the_lease, li.off_the_lease, li.lease_type, li.on_the_lease_area, li.on_the_lease_farmers, li.off_the_lease_area, li.off_the_lease_farmers").slideUp("fast");
});

/* Employment: toggle visibility of subfields on click*/
if($("body").hasClass("public")) {
	if(!$('#id_employment-total_jobs_created').is(":checked")) {
		$('#id_employment-total_jobs_created').parent().parent().nextAll().slice(0,2).css("display","none");
	}
	if(!$('#id_employment-foreign_jobs_created').is(":checked")) {
		$('#id_employment-foreign_jobs_created').parent().parent().nextAll().slice(0,2).css("display","none");
	}
	if(!$('#id_employment-domestic_jobs_created').is(":checked")) {
		$('#id_employment-domestic_jobs_created').parent().parent().nextAll().slice(0,2).css("display","none");
	}
	$('#id_employment-total_jobs_created, #id_employment-foreign_jobs_created, #id_employment-domestic_jobs_created').click(function() {
		$(this).parent().parent().nextAll().slice(0,2).slideToggle('fast');
	});
} else {
	if(!$('#id_employment-total_jobs_created').is(":checked")) {
		$('#id_employment-total_jobs_created').parent().parent().nextAll().slice(0,7).css("display","none");
	}
	if(!$('#id_employment-foreign_jobs_created').is(":checked")) {
		$('#id_employment-foreign_jobs_created').parent().parent().nextAll().slice(0,7).css("display","none");
	}
	if(!$('#id_employment-domestic_jobs_created').is(":checked")) {
		$('#id_employment-domestic_jobs_created').parent().parent().nextAll().slice(0,7).css("display","none");
	}
	$('#id_employment-total_jobs_created, #id_employment-foreign_jobs_created, #id_employment-domestic_jobs_created').click(function() {
		$(this).parent().parent().nextAll().slice(0,7).slideToggle('fast');
	});
}

/* Investor info - live search  */
$("a.new-investor, a.existing-investor").click(function(){
	/*
$("input.livesearch").keyup(function(){
		var filter = $(this).val();
        $("input.livesearch").parent().find("ul li a").each(function(){
             if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                $(this).fadeOut();
             } else {
                $(this).show();
            }
        });
	  });
*/
	$("li.subsidiary_of span ul li a").click(function(e){
		e.preventDefault();
		var subsidiaryID = $(this).attr("href").substring(1);
		var subsidiaryName = $(this).parent().parent().parent().parent().find("label").attr("for").substring(0,16);
		if($(this).hasClass("selected-subsidiary")) {
			$(this).removeClass("selected-subsidiary");
			$(this).next().remove();
		} else {
			$(this).addClass("selected-subsidiary");
			$(this).after(function() {
				return '<input type="hidden" name="' + subsidiaryName + 'subsidiary_of" value="' + subsidiaryID + '">';
			});
		}

		return false;
	});

	$("li.investor span ul li a").click(function(e){
		e.preventDefault();
		var investorID = $(this).attr("href").substring(1);
		var investorName = $(this).parent().parent().parent().parent().find("label").attr("for").substring(0,16);
		$(this).addClass("selected-investor");
		$(this).after(function() {
			return '<input type="hidden" name="' + investorName + 'investor" value="' + investorID + '">';
		});
		$(this).parent().siblings().hide();
		$(this).parent().parent().height("auto").css("overflow","hidden");
		return false;
	});


});

$("li.investor span ul li a").click(function(e){
		e.preventDefault();
		var subsidiaryID = $(this).attr("href").substring(1);
		//var subsidiaryName = $(this).parent().parent().parent().find(".livesearch").attr("id").replace(/[^\d.]/g, "");
		if($(this).hasClass("selected-subsidiary")) {
			$(this).removeClass("selected-subsidiary");
			$(this).next().remove();
		} else {
			$(this).addClass("selected-subsidiary");
			$(this).after(function() {
				return '<input type="hidden" name="subsidiary_of" value="' + subsidiaryID + '">';
			});
		}

		return false;
	});

$("li.subsidiary_of span ul li a").click(function(e){
		e.preventDefault();
		var subsidiaryID = $(this).attr("href").substring(1);
		//var subsidiaryName = $(this).parent().parent().parent().find(".livesearch").attr("id").replace(/[^\d.]/g, "");
		if($(this).hasClass("selected-subsidiary")) {
			$(this).removeClass("selected-subsidiary");
			$(this).next().remove();
		} else {
			$(this).addClass("selected-subsidiary");
			$(this).after(function() {
				return '<input type="hidden" name="subsidiary_of" value="' + subsidiaryID + '">';
			});
		}

		return false;
	});

/* Collapse existing investor fields on page load */
$(".form.existing-investor:not(.empty) li.investor span ul li a:not(.selected-investor)").hide();




});





/* sinnwerkstatt script */

var geocoders = new Array();
var maps = new Array();
var markers = new Array();
var autocompletes = new Array();
var latChanged = new Array();
var lonChanged = new Array();

function initializeMap (el, index) {
  //MAP
  var latlng = new google.maps.LatLng(41.659,-4.714);
  var options = {
    zoom: 16,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };
  maps[index] = new google.maps.Map(el, options);
  //GEOCODER
  geocoders[index] = new google.maps.Geocoder();

  markers[index] = new google.maps.Marker({
    map: maps[index],
    draggable: true
  });
  var lat = $(el).parents("ul").find(".point_lat input").val();
  var lon = $(el).parents("ul").find(".point_lon input").val();
  var latLng = new google.maps.LatLng(lat, lon);
  maps[index].setCenter(latLng);
  markers[index].setPosition(latLng);
  latChanged[index] = lat;
  lonChanged[index] = lon;
  if(lat.length == 0) {
    maps[index].setZoom(2);
  } else {
    maps[index].setZoom(8);
  }
  // changed lan or lon value, center map and request target Country
  $(el).parents("ul").find(".point_lat input, .point_lon input").change(function() {
    var accuracy = $(this).parents("ul").find(".level_of_accuracy select :selected").first().val();
    var value = $(this).val();
    if ($(this).parents("li").hasClass("point_lat")) {
      latChanged[index] = value;
    } else {
      lonChanged[index] = value;
    }
    if (accuracy == "40" && latChanged[index] != null && latChanged[index] != "" && lonChanged[index] != null && lonChanged[index] != "") {
      var latLng = new google.maps.LatLng(latChanged[index], lonChanged[index]);
      maps[index].setCenter(latLng);
      maps[index].setZoom(8);
      markers[index].setPosition(latLng);
      geocoders[index].geocode({"latLng" : latLng, "language": "en"}, function(results, status) {
        for(var i = 0; i < results[0].address_components.length; i++) {
            if (results[0].address_components[i].types.indexOf("country") != -1) {
              country = results[0].address_components[i].short_name;
              $(el).parents("ul").find(".target_country option[title='" + country + "']").attr('selected', 'selected');
              $(el).parents("ul").find(".target_country option:not([title='" + country + "'])").removeAttr("selected");
            }
          };
      });
    }
  });
  //switched level of accuracy fire event on lan and lon input fields
  $(el).parents("ul").find(".level_of_accuracy select").change(function() {
    if ($(this).find(":selected").val() == "40") {
      $(this).parents("ul").find(".point_lat input, .point_lon input").change();
    }
  });
  google.maps.event.addListener(markers[index], 'drag', function() {
  geocoders[index].geocode({'latLng': markers[index].getPosition(), "language": "en"}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        $(el).parents("ul").find(".point_lat input").val(markers[index].getPosition().lat());
        $(el).parents("ul").find(".point_lon input").val(markers[index].getPosition().lng());
      }
    }
  });
});
}

function cloneYBDfield(link) {
  var wrap = link.parents(".field .input-append"),
    inputs = wrap.find(":input"),
    input_data = $(inputs[inputs.size()-2]).clone(),
    input_year = $(inputs[inputs.size()-1]).clone(),
    helptext = wrap.find(".helptext:last").clone(),
    prefix = input_data.attr("id");
  prefix = prefix.slice(0, prefix.lastIndexOf("_")+1);
  input_data.attr("id", prefix + (parseInt(input_data.attr("id").replace(prefix, ""))+2));
  input_data.attr("name", prefix.slice(3) + (parseInt(input_data.attr("name").replace(prefix.slice(3), ""))+2));
  input_data.val("");
  input_year.attr("id", prefix + (parseInt(input_year.attr("id").replace(prefix, ""))+2));
  input_year.attr("name", prefix.slice(3) + (parseInt(input_year.attr("name").replace(prefix.slice(3), ""))+2));
  input_year.val("");
  link.before(input_data);
  link.before(input_year);
  link.before(helptext);
  link.next().show();
}

function removeYBDfield(link) {
  len = link.prevAll(":input").length;
  if (len > 2) {
    link.prev().prev("span").remove();
    link.prev().prev(":input").remove();
    link.prev().prev(":input").remove();
  }
  if (len == 4) {
    link.hide();
  }
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    traditional: true // don't use brackets for array params
});

function update_widget (el, key_id, form) {
  var value = form.find("input[type='hidden']").val(),
      name = el.find(":input").attr("name"),
      op = el.parents("li").prev().find("option:selected").val();
  // year based fields delete suffix (e.g. _0)
  name = name.replace(/_\d+$/, "");
  $.get("/ajax/widget/" + doc_type + "/", {key_id:  key_id, value: value, name: name, operation: op}, function (data) {
    el.html(data);
  });
};

function update_year_based_history (el, id) {
  var field = el.attr("id");
  $.get("/ajax/history/" + id, {field: field}, function (data) {
    el.html(data);
  });
};

function init_google_maps(el, index) {
  el.autocomplete({
        //This bit uses the geocoder to fetch address values
        source: function(request, response) {
          var accuracy = el.parents("ul").find(".level_of_accuracy select :selected").first().val();
          // only lookup name when level of accuracy is not exact coordinates
          if (accuracy != "40") {
            geocoders[index].geocode( {'address': request.term, "language": "en" }, function(results, status) {
              response($.map(results, function(item) {
                country = "";
                for(var i = 0; i < item.address_components.length; i++) {
                  if (item.address_components[i].types.indexOf("country") != -1) {
                    country = item.address_components[i].short_name;
                  }
                };
                return {
                  label:  item.formatted_address,
                  value: item.formatted_address,
                  latitude: item.geometry.location.lat(),
                  longitude: item.geometry.location.lng(),
                  country: country
                }
              }));
            })
          }
        },
        //This bit is executed upon selection of an address
        select: function(event, ui) {
          el.parents("ul").find(".point_lat input").val(ui.item.latitude).change();
          el.parents("ul").find(".point_lon input").val(ui.item.longitude).change();
          //$("#id_spatial_data-target_country option:selected").removeAttr("selected"); - doesn't work in FF 14
          el.parents("ul").find(".target_country option[title='" + ui.item.country + "']").attr('selected', 'selected');
          el.parents("ul").find(".target_country option:not([title='" + ui.item.country + "'])").removeAttr("selected");
          var location = new google.maps.LatLng(ui.item.latitude, ui.item.longitude);
          markers[index].setPosition(location);
          maps[index].setCenter(location);
        }
      });
};


$(document).ready(function () {
  $("a.history").click(function(e) {
    var id = $("input[name='deal_id']").val();
    update_year_based_history($(this).next("div"), id);
    e.preventDefault();
  });
  $("#browse .rule-links a").click(function () {
    $(":input[name=current-form]").val($(this).attr("href").substr(1));
  }).filter("[href=#"+$(":input[name=current-form]").val()+"]").click();
  $(":checkbox[name=select-all]").click(function() {
    $(this).parents("table").find(":checkbox[name=selects]").attr("checked", this.checked);
  });
  // google maps
  $(".form:visible .field.location .map").each(function (i) {
    initializeMap(this, i);
    init_google_maps($(this).prev("input"), i);
  });
  //$("#add-spatial-data").click(function () {
  //  var index = $(".spatial :input[name=spatial_data-TOTAL_FORMS]").val() - 1;
  //  initializeMap($(".form:visible .field.location .map").last()[0], index);
  //  init_google_maps($(".form:visible .field.location input").last(), index);
  //});

});
