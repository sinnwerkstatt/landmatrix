function drawPie (e, d, isDataAvailability) {
	var r = Raphael(e, d, d),
    	data = $(e).data("title"),
    	chart;
    if (isDataAvailability) {
        data = parseFloat(data.toString().replace(/[^0-9\.]/g,''));
        data = [data, 100-data];
    	chart = r.piechart(d/2, d/2, d/2, data, {colors: ["#da891e", "#444444"], strokewidth: 0});
        c = r.circle(d/2, d/2, (d/2)-1);
        c.attr("stroke", "#fff");
        c.attr("stroke-width", "2");
    } else {
        data = data.replace(/[ %]/g,"").split(","),
        data = [parseFloat(data[0]), parseFloat(data[1]), parseFloat(data[2]), parseFloat(data[3])]
        chart = r.piechart(d/2, d/2, d/2, data, {colors: ["#DA8A1C", "#EEC497", "#F6EDE1", "#84CECE"], strokewidth: 0});
        c = r.circle(d/2, d/2, (d/2)-1);
        c.attr("stroke", "#fff");
        c.attr("stroke-width", "2");
    }
}

function drawHorizontalLineChart (element, pct, color, width, height) {
	var r = Raphael(element, width, height);
    var bg = r.rect(0, 0, width, height).attr({ fill: 'rgb(216, 216, 216)', 'stroke-width': 0 });
    var fill = r.rect(0, 0, width * (pct / 100), height).attr({ fill: color, 'stroke-width': 0 });
}

function drawVerticalLine (paper, x, startY) {
    var start = x + " " + (startY - 10);
    var end = "0 -" + (paper.height - 40 - (paper.height - startY));
    var line = paper.path("M " + start + " l " + end).attr({
        fill: '#fff',
        stroke: '#89959e',
        'stroke-width': 2,
        'stroke-opacity': 1,
        'stroke-dasharray': "."
    });
    return line;
}

function getZoomedCoords (x, y, zoomData) {
    var fullWidth = $('#map').width();
    var fullHeight = $('#map').height();
    zoomData.left = zoomData.x - (zoomData.width / 2);
    zoomData.top = zoomData.y - (zoomData.height / 2);
    var xMod = (fullWidth / zoomData.width);
    var yMod = (fullHeight / zoomData.height);
    var coords = {};
    coords.x = (x - zoomData.left) * xMod;
    coords.y = (y - zoomData.top) * yMod;
    coords.x += 15; // This offset seems to be required
    return coords;
}

function showTooltip (obj, e) {
    if (obj == window) return false;
	var t,
	    pos,
	    c = $("#tooltip-container");
	if ($(obj).data("title")) {
        // Investment sector
	    obj = $(obj);
	    t = obj.data("title");
	    pos = obj.offset();
	    pos.width = obj.width();
	    pos.height = obj.height();
        var top = (pos.top + pos.height/2 + obj.height()/2);

	} else {
        // map bubble
	    pos = obj.getBBox();
        var zoomData = $("#map").data('zoom-coords');
        if (zoomData) {
            // zoomed
            var coords = getZoomedCoords(pos.x, pos.y, zoomData);
            pos.top = $("#map").offset().top + coords.y;
    	    pos.left = $("#map").offset().left + coords.x;
            var top = (pos.top + pos.height/2 + c.height());
        }
        else {
            // world map
            pos.top = $("#map").offset().top + pos.y;
    	    pos.left = $("#map").offset().left + pos.x;
            var top = (pos.top + pos.height/2 + c.height()) - 20; // -20 for world map
        }

        t = obj.data && obj.data("title");
	}
    var left = (pos.left + pos.width/2 - c.width()/2);
	c.find("span.content").html(t);
	c.css({
		'top': top + "px",
		'left': left + "px"
	});
	t && c.show();
}

function hideTooltip (obj, e) {
	$("#tooltip-container").hide();
}

function update_widget (el, key_id, form) {
  console.log("here");
  var value = form.find("input[type='hidden']").val(),
      name = el.find(":input").attr("name"),
      op = el.parents("li").prev().find("option:selected").val();
  console.log(name);
      console.log("Widget call returned:", data);
    el.html(data);
  });
};

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

$(document).ready(function() {
    // Replace title attributes to prevent the default tooltip
	$('[title]').each( function() {
        var e = $(this);
        e.data('title', e.attr('title'));
        e.removeAttr('title');
    });
	$(".tooltip").hover(function (e) { return showTooltip(this, e) }, function (e) { return hideTooltip(this, e) });
	// Create/replace pie charts
	$(".pie-chart").each(function () {
	    if ($(this).data("title").indexOf('100') != -1) {
	        $(this).addClass("full");
	    } else {
            if ($(this).hasClass("big")) {
                var diameter = 84;
            }
            else if ($(this).hasClass("huge")) {
                var diameter = 324;
            }
            else {
                var diameter = 42;
            }
        	drawPie(this, diameter, $(this).hasClass("data-availability"));
	    }
	});
    // draw horizontal line charts
	$(".horizontal-line-chart").each(function () {
        if ($(this).hasClass("democracy-index")) {
            var color = 'rgb(162, 185, 204)';
        }
        else {
            var color = 'rgb(197, 175, 137)';
        }
        var val = parseFloat($(this).data("title").toString().replace(/[^0-9\.]/g,'')) * 10;
        drawHorizontalLineChart(this, val, color, 90, 10);
	});


    // Sticky table header
    var t = $('table thead tr:first');
    if (t.size() > 0) {
        stickyHeaderTop = t && t.offset().top || null;
        $(window).scroll(function(){
            if( ($(window).scrollTop() + 115) > stickyHeaderTop ) {
                $('table thead tr:first').css({position: 'fixed', top: '120px', 'z-index': '4'});
                $('table').css({'margin-top': '72px'});
            } else {
                $('table thead tr:first').css({position: 'static', top: '0'});
                $('table').css({'margin-top': '0'});
            }
        });
    };
    // Toggle links
    $("a.toggle").click(function (e) {
        var l = $(this),
            t = $(l.attr("href"));
        if (t.is(":visible")) {
            t.fadeOut();
            l.text(l.text().replace("Hide", "Show"));
            t.attr("id") == 'filters' && $(".filter").fadeOut() && $(".submit").fadeOut();
        } else {
            t.fadeIn();
            l.text(l.text().replace("Show", "Hide"));
            t.attr("id") == 'filters' && $(".filter").fadeIn() && $(".submit").fadeIn();
        }
        e.preventDefault();
        return false;
    });
	// autotoggle on filtered
	if (location.href.indexOf('filtered') > -1) {
		$('.actions .button.toggle').click();
	}

    var showOverlay = function (selector) {
        var overlay = $(selector);
        $(".overlay:visible").fadeOut();
        overlay.fadeIn();
        overlay.children('.subnav').css("visibility", "visible"); // shouldn't be required..
        $("#overlay-container").fadeIn();
    };

    var hideOverlays = function () {
        $(".overlay:visible").fadeOut();
        $("#overlay-container").fadeOut();
    };

    // Show overlay links
    // $("a.show-overlay").click(function (e) {
    //     var hash = $(this).attr('href');
    //     showOverlay(hash + '-overlay');
    //     window.location.hash = hash;
    //     e.preventDefault();
    // });
    // $("a.hide-overlay").click(function (e) {
    //     hideOverlays();
    //     window.location.hash = '#_'; // Don't use #, as that jumps to top of page
    //     e.preventDefault();
    // });

    var togglePage = function(selector) {
        var page_id = selector.substring(1);
        var page = $('#' + page_id);
        $(".subnav .select span:visible").hide();
        $(".subnav .select span." + page_id).show();
        $(".subnav .select li.current").removeClass("current");
        $(".subnav .select li." + page_id).addClass("current");
        $(".page:visible").hide();
        page.fadeIn();
    }

    // Toggle page
    $("a.toggle-page").click(function (e) {
        var page = $(this).attr('href');
        togglePage(page);
        window.location.hash = '#pages-' + page.substring(6);
        e.preventDefault();
        return false;
    });
    // Select links
    $("a.select").click(function (e) {
        var l = $(this);
            t = $(l.attr("href") + " input").attr("checked", l.hasClass("all") ? true : false);
        e.preventDefault();
        return false;
    });

    // Compare filter
    $("a.filter-compare").click(function (e) {
        var checkboxes = $("table#summary tbody :checkbox");
        // Show boxes?
        if (checkboxes.filter(":visible").size() > 0) {
            checkboxes.hide();
            e.preventDefault();
            return false;
        } else {
            if (checkboxes.size() > 0) {
                checkboxes.show();
            } else {
                $("table#summary tbody tr td:first-child").each(function (i) {
                    $(this).prepend('<input type="checkbox" value="' + i + '" class="checkbox" name="compare_items" />');

                });
            }
            $("tbody").attr("id", "compare");
        }

    });

    var validHashes = ['#pages', '#pages-about', '#pages-partners', '#pages-methodology', '#pages-terminology', '#pages-disclaimer', '#report-a-deal', '#analytical-report'];
    var hash = window.location.hash;
    if (hash && (jQuery.inArray(hash, validHashes) != -1)) {
        if (hash.substring(0,6) != '#pages') {
            showOverlay(hash + '-overlay');
        }
        else {
            showOverlay('#pages-overlay');
            var page = hash.substring(7);
            if (page) {
                togglePage('#page-' + page);
            }
        }
    }

    // detail page init google maps
    $(".form:visible .field.location .map").each(function (i) {
      initializeMap(this, i);
    });
});
