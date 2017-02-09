function drawMap(callback) {
$("#map").empty();
m = Raphael("map", 960, svgheight, function () {
    // retrieves query params from investor-target-countries.html mean hack
	var map = this;
    var group = map.set();
    map.regionBubbles = []; // Store region data for reuse
    map.countryBubbles = [];
	map.importSVG(vectors);
	var world = map.setFinish();
	map.getXY = function (lon, lat) {
        var x_offset = -30;
        var y_offset = 10;
        var x_modifier = 1.07;
        var y_modifier = 1.03;
        var x = ((lon * x_modifier) + 180 + x_offset) * (this.width/360);
        var y = Math.abs((lat * y_modifier) - 90 + y_offset) * (this.height/180);
    	return {
            cx: x,
            cy: y
		};
	};
    var investor_target;
    var zoomOutLink = $('#map-zoom-out');
    var zoomInLink = $('#map-zoom-in');
    var clearMapOverlayLink = $('#clear-map-overlay');
    var overlayContainer = $("#overlay-container");
    var mapOverlay = $("#map-overlay");
    var getDetailsLink = $('#get-details-link');
    var tableLink = $('#table-link');
    var subheadNavLinks = $('#container').children('ul.subnav');
    var subheadTableLink = $('#subnav-table-link');
    var goToCountryLink = $('.subnav .country-table');
    var currentOrigin;

    if ($('#map').hasClass('investor-target')) {
        investor_target = $('#map').hasClass('target') ? 'target' : 'investor';
    } else {
        investor_target = '';
    };
    map.bubbles = [];
    map.drawLine = function (origin, target) {
        var box1 = origin.getBBox(),
            box2 = target.getBBox(),
            start = {x: box1.x+(box1.width/2), y: box1.y+(box1.height/2)},
            end = {x: box2.x+(box2.width/2), y: box2.y+(box2.height/2)},
            line = map.path('M' + start.x + ' ' + start.y + 'L' + end.x + ' ' + end.y).attr({'stroke': (investor_target == 'target' ? '#ed881b' : '#44b7b6'), "stroke-width":2});

        origin.lines.push(line);
    }
    map.clearBubbles = function (b) {
        currentOrigin = undefined;
        jQuery.each(map.bubbles, function(index, bubble) {
            bubble.lines && jQuery.each(bubble.lines, function(index, line) { line.remove(); });
            if (bubble !== b) {
                bubble.caption && bubble.caption.remove();
                bubble.remove();
            };
        });
        map.bubbles = [];
        b && map.bubbles.push(b);
    }

    map.showInfobox = function (bubble, origin) {
        /* Draws a box with detailed info about the clicked country */
        var box = $(".current-country"),
            name = bubble.country || bubble.name,
            deal_type, relation, heading;
        if (bubble.type == 'investor') {
            heading = "By "+name;
        } else {
            heading = "In "+name;
        }
        box.prev().fadeOut(250);
        if (box.find("strong").text() != heading || currentOrigin == undefined && origin != undefined || origin.name != currentOrigin.name) {
            // only update values when country has changed, origin has changed or a origin never was clicked
            currentOrigin = origin;
            box.find("p").fadeOut(250, function() {
                box.find("strong").text(heading);
                (bubble.type == 'investor') && box.addClass("investor") || box.removeClass("investor");
                if (origin) {
                    if (parseInt(origin.country_id) == parseInt(bubble.country_id)) {
                        if (investor_target == 'investor') { deal_type = 'deal' }
                        else { deal_type = 'deal' }
                        box.find(".related-country").hide();
                        var self_deals = box.find(".self-deals");
                        if ((bubble.transnational > 0) && (bubble.domestic > 0)) {
                            self_deals.html('whereof '+ bubble.transnational + ' transnational and ' + bubble.domestic + ' domestic').show();
                        } else {
                            self_deals.html(', ' + (bubble.transnational > 0 && ' transnational' || 'domestic') + ' only');
                        }
                        self_deals.show();
                    } else {
                        if (investor_target == 'investor') { deal_type = 'deal'; relation = 'by' }
                        else { deal_type = 'deal'; relation = 'in'; }
                        box.find(".related-country").text(relation + ' ' + (origin.name || origin.country)).show();
                        box.find(".self-deals").hide();
                    }
                } else {
                    if (investor_target == 'investor') { deal_type = 'deal'; relation = 'of';
                    } else { deal_type = 'deal'; relation = 'to'; }
                    box.find(".related-country").hide();
                    box.find(".self-deals").hide();
                }
                box.find(".total-deals").text(bubble.deals + ' ' + deal_type + (bubble.deals == 1 ? '' : 's'));
                var url = URL_PREFIX + "data/";
                if (bubble.type == 'investor') {
                    url = url + "by-investor-country/" + bubble.country_slug;
                }
                else {
                    url = url + "by-target-country" + "/" + bubble.country_slug;
                }
                box.find("a").attr("href", url);
                box.show();
                box.find("p").fadeIn(250);
            });
        }
    }
    map.onInvestorTargetBubbleClick = function (bubble, origin, toggle) {
        return function (e) {
            $(".views .show-all:not(:visible)").removeClass("disabled");
            // switch mode
            if (toggle) { investor_target = investor_target == 'investor' ? 'target' : 'investor'; };
            bubble.attr({"fill": investor_target == 'target' ?  "#ed881b" : "#44b7b6" });
    	    map.clearBubbles(bubble);
            // get affected bubbles
            url = investor_target == 'target' ? URL_PREFIX + "api/investor_countries_for_target_country.json" : URL_PREFIX + "api/target_countries_for_investor_country.json";
            url = url + '?country=' + origin.country_id;
            xhr = jQuery.ajax({
                url: url,
                dataType: 'json'
            }).done(function(data) {
                var origin_data = map.drawRelatedBubbles(data, [bubble, origin]);
                var subnav = $("ul.actions li.select").removeClass("investor target").addClass(investor_target);
                subnav.find("a.current").text(subnav.find("li." + investor_target).text());
                subnav.find("li").removeClass("current").filter("." + investor_target).addClass("current");
                $("#map").removeClass(investor_target == 'investor' ? 'target' : 'investor').addClass(investor_target);
                map.showInfobox(origin, origin_data);
            });
            e.preventDefault();
        }
    }
    map.drawBubbles = function (bubbles) {
    	jQuery.each(bubbles, function(index, bubble) {
            // Map(Countries)
            if (bubble.country_id && !investor_target) {
                var radius = 4;
                if (bubble.deals > 0) radius += (Math.log(bubble.deals));
            }
            // Map(Regions) and Investor/Target Map (Countries)
            else {
        		var radius = 8; // Min radius
                if (bubble.deals > 0) radius += (Math.log(bubble.deals) * 3) + (bubble.deals / 100);
            }
            // up by decreasing amounts. Don't log 0, as that is -Infinity
            // ((number_of_deals / max_deal_count * max_width-20) + min_width) / radius_to_width
    		var cords = map.getXY(bubble.lon, bubble.lat);
    		var a = map.circle()
    			.attr({
    				fill: investor_target ? (investor_target == 'target' ? "#ed881b" : "#44b7b6") : "#ed881b",
    				href: "#",
    				stroke: "#fff",
    				"stroke-width": 2,
    				r: 1
    			}).data('title', (investor_target ? bubble.country : bubble.name))
    			.attr(cords);
    		investor_target && (bubble.type = investor_target);
            a.animate({r: radius}, 1000, "bounce", investor_target && function () {
                // shrink so bubbles don't overlap
                a.animate({r: 8}, 1000, "backIn");
                a.caption.hide();
            });
    		var text = map.text().attr({
    			text: bubble.deals,
    			fill: "#ffffff",
    			href: "#",
    			y: cords['cy'],
    			x: cords['cx']
        	});
            text.attr({ 'font-size': (bubble.country_id && !investor_target) ? 4 : 12 });
            // set click and hover
    		jQuery.each([a,text], function (index, obj) {
        		if (investor_target) {
        		    obj.event_click = map.onInvestorTargetBubbleClick(a, bubble, false);
        		} else {
        			obj.event_click = function(e) {
            			showMapOverlay($(this["id"]), bubble);
                                e.preventDefault();
        			};
        		};
        		obj.click(obj.event_click);
				obj.block = false;
        		obj.event_mouseenter = function (e) {
					if (!obj.block) {
						obj.block = true;
	                    a.toFront().stop().animate({r: radius*1.5}, 1000, "bounce", function(){
							obj.block = false;
						}).caption.toFront();
	                    investor_target && a.caption.show() && map.showInfobox(bubble);
	                    !investor_target && showTooltip(a, e);
					}
        		};
        		obj.event_mouseleave = function (e) {
                    a.stop().animate({r: investor_target ? 8 : radius}, 1000, "bounce", function(){
						obj.block = false;
					});
                    investor_target && a.caption.hide();
                    !investor_target && hideTooltip(a, e);
        		};
        		obj.hover(obj.event_mouseenter, obj.event_mouseleave);
    		});
            a.caption = text;
            a.lines = [];
            map.bubbles.push(a);
    	});
    }
    map.drawRelatedBubbles = function (bubbles, origin) {
        var origin_r = origin[0],
            origin_data = origin[1];
        origin_data.known_deals = 0;
        origin_data.unknown_deals = 0;
        origin_data.self_deals = 0;

    	jQuery.each(bubbles, function(index, bubble) {
    	    if (bubble.country_id == origin_data.country_id) {
    	        origin_data.self_deals = parseInt(bubble.deals);
    	        return true;
    	    } else {
    	        if (!bubble.name) {
    	            origin_data.unknown_deals += parseInt(bubble.deals);
    	        } else {
    	            origin_data.known_deals += parseInt(bubble.deals);
    	        }
    	    }
        	var radius = 8; // Min radius
            // ((number_of_deals / max_deal_count * max_width-20) + min_width) / radius_to_width
            if (bubble.deals > 0) radius += (Math.log(bubble.deals) * 3) + (bubble.deals / 100);

    		var cords = map.getXY(bubble.lon, bubble.lat);
    		var a = map.circle()
    			.attr({
    				fill: investor_target == 'target' ? "#44b7b6" : "#ed881b",
    				href: "#",
    				stroke: "#fff",
    				"stroke-width": 2,
    				r: 1
    			}).attr(cords)
    			.data('title', bubble.name).data('radius', radius);
    		investor_target && (bubble.type = investor_target == 'investor' ? 'target' : 'investor');
            map.drawLine(origin_r, a);

    		var text = map.text().attr({
    			text: bubble.deals,
    			fill: "#fff",
    			href: "#",
    			y: cords['cy'],
    			x: cords['cx']
        	});
            text.attr({ 'font-size': 12 }).hide();

            // set click and hover
    		jQuery.each([a,text], function (index, obj) {
        		obj.event_click = map.onInvestorTargetBubbleClick(a, bubble, true);
        		obj.click(obj.event_click);
        		obj.event_mouseenter = function (e) {
                    a.animate({r: radius*1.5}, 1000, "bounce");
                    map.showInfobox(bubble, origin_data);
        		};
        		obj.event_mouseleave = function (e) {
                    a.animate({r: radius}, 1000, "bounce");
        		};
        		obj.hover(obj.event_mouseenter, obj.event_mouseleave);
    		});

            a.caption = text;
            a.lines = [];
            map.bubbles.push(a);
    	});
    	map.showBubbles = function showBubbles () {
    	    jQuery.each(map.bubbles, function(index, bubble) {
    	        if (bubble == origin_r) return true;
    	        bubble.animate({r: bubble.data('radius')}, 1000, "bounce").toFront();
    	        bubble.caption.show().toFront();
    	    });
    	}
    	setTimeout('map.showBubbles()', 300);

        jQuery.each([origin_r, origin_r.caption], function (index, obj) {
            obj
                .unhover(obj.event_mouseenter)
                .unclick(obj.event_click)
    		    .hover(function (e) {
                map.showInfobox(origin_data, origin_data);
    		}, function () {});
		});
		origin_r.animate({r: 8}, 1000, "backIn");
        origin_r.caption.hide();
        //origin_data.deals = origin_data.known_deals + origin_data.self_deals + origin_data.unknown_deals;
        return origin_data;
    };

    var xhr;
    if (investor_target) {
        xhr = jQuery.ajax({
            url: investor_target == 'investor' ? URL_PREFIX + "api/investor_country_summaries.json" : URL_PREFIX + "api/target_country_summaries.json",
            dataType: 'json'
        }).done(function(data) {
           map.drawBubbles(data);
           map.countryBubbles = data;
           callback();
        });
    } else {
        xhr = jQuery.ajax({
            url: URL_PREFIX + "api/target_region_summaries.json",
            dataType: 'json'
        }).done(function(data) {
            map.drawBubbles(data);
            map.regionBubbles = data;
            callback();
        });
    };

    zoomOutLink.click(function(e) {
		resetMapZoom();
        e.preventDefault();
    });

    $(".views .show-all").click(function (e) {
        map.clearBubbles();
        map.drawBubbles(map.countryBubbles);
        $(".current-country").hide();
        $(".current-country").prev().show();
        $(this).addClass("disabled");
        e.preventDefault();
        return false;
    });

    function resetMapZoom() {
        zoomOutLink.hide();
		clearMapOverlay();
        zoomInLink.show();
        map.setViewBox(0, 0, 960, ssvgheight);
        map.clearBubbles();
        map.drawBubbles(map.regionBubbles);
        $("#map").removeClass("zoomed").data('zoom-coords', null);
    }

    // Zoom map to box CENTERED ON x,y with dimensions width, height
    function zoomMap(bubble, x, y, width, height) {
        var left = x - (width / 2);
        var top = y - (height / 2);
        map.setViewBox(left, top, width, height);
        zoomOutLink.css('display', 'block');

        map.clearBubbles();
        if (bubble.region_id) {
            var xhr = jQuery.ajax({
                url: URL_PREFIX + "api/target_country_summaries.json?regions=" + bubble.region_id,
                dataType: 'json'
            }).done(function(data) {
               map.drawBubbles(data);
            });
        }
		clearMapOverlay();
        $("#map").addClass("zoomed").data('zoom-coords', { x: x, y: y, width: width, height: height });
        $(".title.map h2").text(bubble.region);
    }

    function clearMapOverlay() {
		mapOverlay.fadeOut();
		overlayContainer.fadeOut();
        subheadNavLinks.css("visibility", "visible");
    }

    clearMapOverlayLink.click(function(e) {
        clearMapOverlay();
        e.preventDefault();
    });


	function showMapOverlay(id, bubble) {

        function addCommas(nStr)
        {
        	nStr += '';
        	x = nStr.split('.');
        	x1 = x[0];
        	x2 = x.length > 1 ? '.' + x[1] : '';
        	var rgx = /(\d+)(\d{3})/;
        	while (rgx.test(x1)) {
        		x1 = x1.replace(rgx, '$1' + ',' + '$2');
        	}
        	return x1 + x2;
        }

        $('#map-overlay .investment-sectors a').each(function () {
            var link = $(this),
                c = link.attr("class"),
                n = c.charAt(c.indexOf("sector-")+7).toUpperCase();
            !link.data('initial_title') && link.data('initial_title', link.data('title'));
            link.data('title', link.data('initial_title') + '<br/>(no data available)');
            if (bubble.investment_sectors != null && bubble.investment_sectors.indexOf(n) != -1) {
                var url =  URL_PREFIX + 'data/' + (bubble.country_id ? 'by-target-country/' + bubble.country_slug : 'by-target-region/' + bubble.region_slug);
                url = url + '?investment_natures=' + n;
                link.removeClass("none").attr('href', url);
            } else {
                link.addClass("none");
            };

        });
        // get deals for each investment sector
        url = URL_PREFIX + 'api/investment_sector_deals_for_' + (bubble.country_id ? 'target_country.json?country=' + bubble.country_id :
                'target_region.json?region=' + bubble.region);
        xhr = jQuery.ajax({
            url: url,
            dataType: 'json'
        }).done(function(data) {
            var investment_sectors = $('#map-overlay .investment-sectors a');
            jQuery.each(data, function (index, investment_sector) {
                if (investment_sector.investment_sector) {
                    var e = investment_sectors.filter('.sector-' + investment_sector.investment_sector.toLowerCase());
                    e.data('title', e.data('initial_title') + '<br/>(' + investment_sector.deals + ' ' + (investment_sector.deals == 1 ? 'deal' : 'deals') + ')');
                }
            });
        });
        $("#map-overlay .pie-chart").data("title", 'Data availability: ' + bubble.availability +'%').html('<span>' + Math.round(bubble.availability) + "%</span>");

        var titleLink = $('#map-overlay .title h2 a').text(bubble.country || bubble.name);
        if (bubble.country_id) {
            var url = URL_PREFIX + 'data/by-target-country/' + bubble.country_slug;
            titleLink.unbind('click').attr('href', url);
            getDetailsLink.attr('href', url).css('display', 'block');
            tableLink.hide();
            zoomInLink.hide();
        }
        else if (bubble.region_id) {
            function onZoomClick (e) {
                var coords = map.getXY(bubble.lon, bubble.lat);
                zoomMap(bubble, coords.cx, coords.cy, 320, 187);
                subheadTableLink.attr('href', URL_PREFIX + 'data/by-target-country?regions=' + bubble.region_id);
                e.preventDefault();
            }
            zoomInLink.unbind('click').click(onZoomClick);
            titleLink.attr('href', '').unbind('click').click(onZoomClick);
            getDetailsLink.hide();
            tableLink.attr('href',  URL_PREFIX + 'data/by-target-region/' + bubble.region_slug).css('display', 'block');
        }
        var subtitle = addCommas(bubble.deals) + ' deal';
        if (bubble.deals != 1) {
            subtitle += 's';
        }
        if (bubble.hectares) {
            subtitle += ' over '+ addCommas(bubble.hectares) + ' ha';
        }
        $('#map-overlay .title h3').html(subtitle);

		overlayContainer.fadeIn(function() {
			drawPie($("#map-overlay .pie-chart")[0], 40, true);
			mapOverlay.fadeIn();
		});
        subheadNavLinks.css("visibility", "hidden");

	}
        var bg = map.rect(0, 0, 960, svgheight, 0).attr({"stroke-width": 0});
        bg.click(function (e) {
            e.preventDefault();
            $(".views .show-all").click();
            return false;
        });
    window.map = map;
});
}
