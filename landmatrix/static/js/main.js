$.fn.textWidth = function (text) {
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

function getParameterByName(name) {
    var urlParams;
    var match,
        pl = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) {
            return decodeURIComponent(s.replace(pl, " "));
        },
        query = name;

    urlParams = {};
    while (match = search.exec(query))
        urlParams[decode(match[1])] = decode(match[2]);
    return urlParams;
}

// Usage:
//   var data = { 'first name': 'George', 'last name': 'Jetson', 'age': 110 };
//   var querystring = EncodeQueryData(data);
//
function EncodeQueryData(data) {
    var ret = [];
    for (var d in data)
        ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
    return ret.join("&");
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function drawPie(e, d, isDataAvailability) {
    var r = Raphael(e, d, d),
        data = $(e).data("title"),
        chart;
    if (isDataAvailability) {
        data = parseFloat(data.toString().replace(/[^0-9\.]/g, ''));
        data = [data, 100 - data];
        chart = r.piechart(d / 2, d / 2, d / 2, data, {colors: ["#da891e", "#444444"], strokewidth: 0});
        c = r.circle(d / 2, d / 2, (d / 2) - 1);
        c.attr("stroke", "#ffffff");
        c.attr("stroke-width", "2");
    } else {
        data = data.replace(/[ %]/g, "").split(","),
            data = [parseFloat(data[0]), parseFloat(data[1]), parseFloat(data[2]), parseFloat(data[3])]
        chart = r.piechart(d / 2, d / 2, d / 2, data, {
            colors: ["#DA8A1C", "#EEC497", "#F6EDE1", "#84CECE"],
            strokewidth: 1,
            stroke: "#ededed"
        });
        chart.each(function () {
            //scale each sector to 0
            this.sector.scale(0, 0, this.cx, this.cy);
            //animate from 0 to default size
            this.sector.animate({transform: 's1 1 ' + this.cx + ' ' + this.cy}, 400, "linear");

        });
    }
}

function drawHorizontalLineChart(element, pct, color, width, height) {
    var r = Raphael(element, width, height);
    var bg = r.rect(0, 0, width, height).attr({fill: 'rgb(216, 216, 216)', 'stroke-width': 0});
    var fill = r.rect(0, 0, width * (pct / 100), height).attr({fill: color, 'stroke-width': 0});
}

function drawVerticalLine(paper, x, startY) {
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

function getZoomedCoords(x, y, zoomData) {
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

function showTooltip(obj, e) {
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
        var top = (pos.top + pos.height / 2 + obj.height() / 2);

    } else {
        // map bubble
        pos = obj.getBBox();
        var zoomData = $("#map").data('zoom-coords');
        if (zoomData) {
            // zoomed
            var coords = getZoomedCoords(pos.x, pos.y, zoomData);
            pos.top = $("#map").offset().top + coords.y;
            pos.left = $("#map").offset().left + coords.x;
            var top = (pos.top + pos.height / 2 + c.height());
        }
        else {
            // world map
            pos.top = $("#map").offset().top + pos.y;
            pos.left = $("#map").offset().left + pos.x;
            var top = (pos.top + pos.height / 2 + c.height()) - 20; // -20 for world map
        }

        t = obj.data && obj.data("title");
    }
    var left = (pos.left + pos.width / 2 - c.width() / 2);
    c.find("span.content").html(t);
    c.css({
        'top': top + "px",
        'left': left + "px"
    });
    t && c.show();
}

function hideTooltip(obj, e) {
    $("#tooltip-container").hide();
}

/* NUMBER FORMAT FROM https://raw.github.com/kvz/phpjs/master/functions/strings/number_format.js */
function number_format(number, decimals, dec_point, thousands_sep) {
    // Strip all characters but numerical ones.
    number = (number + '').replace(/[^0-9+\-Ee.]/g, '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function (n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

//var geocoders = new Array();
//var maps = new Array();
//var markers = new Array();
//var autocompletes = new Array();
//var latChanged = new Array();
//var lonChanged = new Array();
//var center_lat = 41.659,
//    center_lng = -4.714;
//var latlng;
//var circle,
//    circle_hectares = -1,
//    circle_radius = 0;
//
//function drawCircle (latlng, i) {
//      if (circle_hectares == -1) {
//          var query_params = get_query_params(get_base_filter(), "");
//          var json_query = "/api/hectares.json" + query_params;
//          jQuery.getJSON(json_query, function (data) {
//              circle_hectares = parseFloat(data["hectares"]);
//              circle_radius = Math.sqrt((circle_hectares * 10000) / Math.PI);
//              // Update legend
//              $(".legend li .hectares").text(number_format(circle_hectares, 0));
//              return drawCircle(latlng, i);
//          });
//      } else {
//          circle && circle.setMap(null); // Remove existing circle
//          circle = new google.maps.Circle({
//              map: maps[i],
//              center: latlng,
//              fillColor: "#ed881b",
//              fillOpacity: 0.5,
//              strokeColor: "#ed881b",
//              strokeOpacity: 1,
//              strokeWeight: 2,
//              radius: circle_radius
//          });
//      };
//};
//function initializeMap (el, index, draw_circle, lat, lng) {
//  //MAP
//  var options = {
//    zoom: 16,
//    center: latlng,
//    mapTypeId: google.maps.MapTypeId.ROADMAP
//  };
//  maps[index] = new google.maps.Map(el, options);
//  //GEOCODER
//  geocoders[index] = new google.maps.Geocoder();
//
//  markers[index] = new google.maps.Marker({
//    map: maps[index],
//    draggable: true
//  });
//  if (lat && lng) {
//    latlng = new google.maps.LatLng(lat, lng);
//  } else {
//    latlng = new google.maps.LatLng(center_lat, center_lng);
//  }
//  maps[index].setCenter(latlng);
//  draw_circle && drawCircle(latlng, index);
//  markers[index].setPosition(latlng);
//  latChanged[index] = lat;
//  lonChanged[index] = lng;
//  if (latlng.length == 0) {
//      maps[index].setZoom(2);
//  } else {
//      //maps[index].setZoom(2);
//      maps[index].setZoom(5);
//  }
//
//  // changed lan or lng value, center map and request target Country
//  $(el).parents("ul").find(".point_lat input, .point_lon input").change(function() {
//    var accuracy = $(this).parents("ul").find(".level_of_accuracy select :selected").first().val();
//    var value = $(this).val();
//    if ($(this).parents("li").hasClass("point_lat")) {
//      latChanged[index] = value;
//    } else {
//      lonChanged[index] = value;
//    }
//    if (accuracy == "40" && latChanged[index] != null && latChanged[index] != "" && lonChanged[index] != null && lonChanged[index] != "") {
//      var latLng = new google.maps.LatLng(latChanged[index], lonChanged[index]);
//      maps[index].setCenter(latLng);
//      drawCircle(latlng, index);
//      maps[index].setZoom(8);
//      markers[index].setPosition(latLng);
//      geocoders[index].geocode({"latLng" : latLng, "language": "en"}, function(results, status) {
//        for(var i = 0; i < results[0].address_components.length; i++) {
//            if (results[0].address_components[i].types.indexOf("country") != -1) {
//              country = results[0].address_components[i].short_name;
//              $(el).parents("ul").find(".target_country option[title='" + country + "']").attr('selected', 'selected');
//              $(el).parents("ul").find(".target_country option:not([title='" + country + "'])").removeAttr("selected");
//            }
//          };
//      });
//    }
//  });
//  //switched level of accuracy fire event on lan and lon input fields
//  $(el).parents("ul").find(".level_of_accuracy select").change(function() {
//    if ($(this).find(":selected").val() == "40") {
//      $(this).parents("ul").find(".point_lat input, .point_lon input").change();
//    }
//  });
//  google.maps.event.addListener(markers[index], 'drag', function() {
//  geocoders[index].geocode({'latLng': markers[index].getPosition(), "language": "en"}, function(results, status) {
//    if (status == google.maps.GeocoderStatus.OK) {
//      if (results[0]) {
//        $(el).parents("ul").find(".point_lat input").val(markers[index].getPosition().lat());
//        $(el).parents("ul").find(".point_lon input").val(markers[index].getPosition().lng());
//      }
//    }
//  });
//});
//  return maps[index];
//}
//
//function init_google_maps(el, index, draw_circle) {
//  el.autocomplete({
//        //This bit uses the geocoder to fetch address values
//        source: function(request, response) {
//          var accuracy = el.parents("ul").find(".level_of_accuracy select :selected").first().val();
//          // only lookup name when level of accuracy is not exact coordinates
//          if (accuracy != "40") {
//            geocoders[index].geocode( {'address': request.term, 'language':'en'}, function(results, status) {
//              response($.map(results, function(item) {
//                country = "";
//                for(var i = 0; i < item.address_components.length; i++) {
//                  if ($.inArray("country", item.address_components[i].types) != -1) {
//                    country = item.address_components[i].short_name;
//                  }
//                };
//                return {
//                  label:  item.formatted_address,
//                  value: item.formatted_address,
//                  latitude: item.geometry.location.lat(),
//                  longitude: item.geometry.location.lng(),
//                  country: country
//                }
//              }));
//            })
//          }
//        },
//        open: function(event, ui) { $(".ui-autocomplete").css("z-index", 10000); },
//        close: function(event, ui) { $(".ui-autocomplete").css("z-index", 1); },
//        //This bit is executed upon selection of an address
//        select: function(event, ui) {
//          el.parents("ul.form").find(".point_lat input").val(ui.item.latitude).change();
//          el.parents("ul.form").find(".point_lon input").val(ui.item.longitude).change();
//          //$("#id_spatial_data-target_country option:selected").removeAttr("selected"); - doesn't work in FF 14
//          el.parents("ul.form").find(".target_country option:selected").removeAttr("selected");
//          el.parents("ul.form").find(".target_country option[title='" + ui.item.country + "']").attr('selected', 'selected');
//          latlng = new google.maps.LatLng(ui.item.latitude, ui.item.longitude);
//          markers[index].setPosition(latlng);
//          maps[index].setCenter(latlng);
//          draw_circle && drawCircle(latlng, index);
//        }
//      });
//  if (draw_circle) {
//    google.maps.event.addListener(markers[index], 'drag', function() {
//        latlng = new google.maps.LatLng(markers[index].getPosition().lat(), markers[index].getPosition().lng());
//        drawCircle(latlng, index)
//    });
//  }
//};

var numeric_operators = ["lt", "gt", "gte", "lte", "is", "is_empty"];
var string_operators = ["not_in", "in", "is", "contains"];
var date_operators = ["lt", "gt", "gte", "lte", "is", "is_empty"];
var list_operators = ["not_in", "in", "is", "is_empty", "contains"];
/**
 *  updates the filter widget for the grid view if the field to filter by is changed
 */
//function update_widget(el, key_id, form) {
//    var value = form.find("input[type='hidden']").val(),
//        name = el.find(":input").attr("name"),
//        op = el.parents("li").prev().find("option:selected"),
//        op_value = op.val();
//    name = name.replace("_0", "");
//    $.get("/ajax/widget/values", {key_id: key_id, value: value, name: name, operation: op_value}, function (data) {
//        el.html(data);
//        var is_number = (el.find(":input[type=number]:not(.year-based-year)").length > 0);
//        var is_list = (el.find("select,ul").length > 0);
//        form.find(".operator option").each(function (index) {
//            if (is_number) {
//                $(this).attr("disabled", (jQuery.inArray($(this).val(), numeric_operators) == -1));
//            } else if (is_list) {
//                $(this).attr("disabled", (jQuery.inArray($(this).val(), list_operators) == -1));
//            } else if (is_date) {
//                $(this).attr("disabled", (jQuery.inArray($(this).val(), list_operators) == -1));
//            } else {
//                $(this).attr("disabled", (jQuery.inArray($(this).val(), string_operators) == -1));
//            }
//        });
//    });
//}

function initCountryField(field) {
    var country_select = field.select2({
        //placeholder: "",
    });
    var country_request = $.ajax({
      url: '/api/countries.json'
    });
    var group, item, option;
    country_request.then(function (data) {
        country_select.data(data);
        for (var d = 0; d < data.length; d++) {
            group = data[d];
            for (var o = 0; o < group.children.length; o++) {
                item = group.children[o];
                option = new Option(item[2], item[0], false, false);
                country_select.append(option);
            }
        }
        country_select.trigger('change');
    });
}

function initInvestorField(field, set_events) {
    set_events = typeof set_events !== 'undefined' ? set_events : true;

    field.select2({
        //placeholder: 'Select Investor',
        ajax: {
            url: '/api/investors.json',
            dataType: 'json',
            delay: 250,
            data: function (params) {
              return {
                q: params.term, // search term
                page: params.page
              };
            },
            processResults: function (data, params) {
                // parse the results into the format expected by Select2
                // since we are using custom formatting functions we do not need to
                // alter the remote JSON data, except to indicate that infinite
                // scrolling can be used
                params.page = params.page || 1;

                return {
                  results: data.results,
                  pagination: {
                    more: (params.page * 30) < data.count
                  }
                };
            },
            cache: true,
        },
        minimumInputLength: 3,
        allowClear: true,
        placeholder: ""
    }).on("select2:unselecting", function (e) {
        $(this).val("");
        $(this).find('option:selected').removeAttr('selected');
        // parent company formset / tertiary investor/lender formset: delete
        $(this).parents('.dynamic-form').find('.DELETE input').val('1')
    });
    if (set_events) {
        field.on('change', function () {
            generateButtons($(this));
            loadInvestorNetwork($(this).val());
        }).trigger('change');
    }
}

function show_reply_form(event) {
    var $this = $(this);
    var comment_id = $this.data('comment-id');
    $('#id_parent').val(comment_id);
    $('#form-comment').insertAfter($this.closest('.comment'));
    $('#cancel-reply').show();
    $(this).parents('.panel-body').find('h3').text('Reply to comment');
};

function cancel_reply_form(event) {
    $('#id_comment').val('');
    $('#id_parent').val('');
    $('#form-comment').appendTo($('#wrap_write_comment'));
    $('#cancel-reply').hide();
    $(this).parents('.panel-body').find('h3').text('Add a comment');
}


$(document).ready(function () {
    function setupSharePopover() {
        $("#btn-share").popover({
            html: true,
            container: '#btn-share',
            content: function () {
                return $('#share').html();
            },
            template: '<div class="popover" role="tooltip"><div class="popover-content"></div></div>'
        });


        $(document).click(function (event) {
            // hide share button popover
            if (!$(event.target).closest('#btn-share').length) {
                $('#btn-share').popover('hide')
            }
        });

        $("a.twitter").attr("href", "https://twitter.com/home?status=" + window.location.href);
        $("a.facebook").attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + window.location.href);
        $("a.google-plus").attr("href", "https://plus.google.com/share?url=" + window.location.href);
    }

    function setupDownloadPopover() {
        $("#btn-download").popover({
            html: true,
            container: '#btn-download',
            content: function () {
                return $('#download').html();
            },
            template: '<div class="popover" role="tooltip"><div class="popover-content"></div></div>'
        });

        $(document).click(function (event) {
            // hide download button popover
            if (!$(event.target).closest('#btn-download').length) {
                $('#btn-download').popover('hide');
            }
        });
    }

    setupSharePopover();
    setupDownloadPopover()

    /*// Set width of headings to make them horizontally centerable
    $("h1.separator span").each(function () {
        $(this).css("width", $(this).textWidth() + 80);
    });
    $("h2.separator span").each(function () {
        $(this).css("width", $(this).textWidth() + 30);
    });*/
    // Toogle links for collapsible sections
    $(".collapsible .toggle").click(function (e) {
        e.preventDefault();
        $(this).parents(".collapsible").toggleClass("collapsed");
        $.get("/ajax/toggle-subnav-collapsed/");
        return false;
    });
    // Previous/next links in subnav
    $("h1 .prev").click(function (e) {
        e.preventDefault();
        var prev = $(".subnav .active").prev();
        if (prev.length == 0) prev = $(".subnav li").last();
        window.location.href = prev.find("a:not(.image)").attr("href");
        return false;
    });
    $("h1 .next").click(function (e) {
        e.preventDefault();
        var next = $(".subnav .active").next();
        if (next.length == 0) next = $(".subnav li").first();
        window.location.href = next.find("a:not(.image)").attr("href");
        return false;

    });


    //FIXME cleanup js
    // Replace title attributes to prevent the default tooltip
    $('a[title]').each(function () {
        var e = $(this);
        e.data('title', e.attr('title'));
        e.removeAttr('title');
    });
    $(".tooltip").hover(function (e) {
        return showTooltip(this, e)
    }, function (e) {
        return hideTooltip(this, e)
    });
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
        var val = parseFloat($(this).data("title").toString().replace(/[^0-9\.]/g, '')) * 10;
        drawHorizontalLineChart(this, val, color, 90, 10);
    });
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

    var togglePage = function (selector) {
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

    // Form fields
    $('[placeholder]').focus(function () {
        var input = $(this);
        if (input.val() == input.attr('placeholder')) {
            input.val('');
            input.removeClass('placeholder');
        }
    }).blur(function () {
        var input = $(this);
        if (input.val() == '' || input.val() == input.attr('placeholder')) {
            input.addClass('placeholder');
            input.val(input.attr('placeholder'));
        }
    }).blur();
    $('[placeholder]').parents('form').submit(function () {
        $(this).find('[placeholder]').each(function () {
            var input = $(this);
            if (input.val() == input.attr('placeholder')) {
                input.val('');
            }
        })
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
        if (hash.substring(0, 6) != '#pages') {
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

    //$(".get-the-detail .map").each(function (i) {
    //  initializeMap(this, i, false, $($(this).parents("tr").siblings().find(".point_lat")[i]).val(), $($(this).parents("tr").siblings().find(".point_lon")[i]).val());
    //});
    // enable hover of subnav to change entry-point graphics
    $(".get-the-detail .subnav li").hover(function () {
        $(".entry-point span").removeClass().addClass("entry-point-" + $(this).attr("class").split(" ")[0]);
    });
    //$(".public .form:not(.empty) .map").each(function (i) {
    //    initializeMap(this, i, false, $(this).parents("ul.form").find(".point_lat").val(), $(this).parents("ul.form").find(".point_lon").val());
    //    init_google_maps($(this).prev("input"), i, false);
    //});
    //$("#add-spatial-data").click(function () {
    //  var index = $(".spatial :input[name=spatial_data-TOTAL_FORMS]").val() - 1;
    //  initializeMap($(".form:visible .field.location .map").last()[0], index);
    //  init_google_maps($(".form:visible .field.location input").last(), index);
    //});
    // tooltips
    $('.toggle-tooltip:not(.left,.bottom)').tooltip({placement: "top", html: true});
    $('.toggle-tooltip.left').tooltip({placement: "left", html: true});
    $('.toggle-tooltip.bottom').tooltip({placement: "bottom", html: true});

    $('.comment-reply-link').click(show_reply_form);
    $('#cancel-reply').click(cancel_reply_form);
});