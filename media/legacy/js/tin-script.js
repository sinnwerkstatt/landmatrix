$(document).ready(function(){


/* Use of produce: Automatic percentage check */
/*

$("input#id_advanced_produce_info-domestic_use").change(function () {
      var value1 = $(this).val();
     $("input#id_advanced_produce_info-export").val(100-value1);
    }).change();
    
$("input#id_advanced_produce_info-export").change(function () {
      var value2 = $(this).val();
     $("input#id_advanced_produce_info-domestic_use").val(100-value2);
    }).change();
*/


/* Disable all subchecks by default */

$("body#add span.input-append ul li ul li label input:checkbox, body#browse span.input-append ul li ul li label input:checkbox").prop("disabled" , true);


/* Enable them again on checking the parent input */

$("input#id_general_information-intention_0,input#id_general_information-intention_1,input#id_water-source_of_water_extraction_1").click(function(){  
    if($(this).is(":checked")) {
      $(this).parent().parent().children("ul").find("input:checkbox").prop("disabled",false);
    }
    else {
      $(this).parent().parent().children("ul").find("input:checkbox").prop("disabled",true).prop("checked",false);
    }
  });


/* Data sources - hide fields if option not selected */

/* $("select[id^=id_data_sources]").parent().parent().parent().find("li.name, li.company, li.email, li.phone").css("display","none"); */

$("select[id*=data_sources]").each(function(){
	if ( $(this).find("option:eq(5), option:eq(6)").is(":selected") ){
	$(this).parent().parent().parent().find("li.name, li.company, li.email, li.phone").show();
}
});


/*


if ( $("select[id^=data_sources]").find("option:eq(0), option:eq(1), option:eq(2), option:eq(3), option:eq(4)").is(":selected") ){
	$("select[id^=data_sources]").parent().parent().parent().find("li.name, li.company, li.email, li.phone").css("display","none");
}
*/


/* Data sources - Show fields based on selection */

$("select[id*=data_sources]").change(function (){
	if ( $(this).find("option:eq(6), option:eq(5)").is(":selected") ){
		$(this).parent().parent().parent().find("li.name, li.company, li.email, li.phone").slideDown("fast");
	}
	else {
		$(this).parent().parent().parent().find("li.name, li.company, li.email, li.phone").slideUp("fast");
	}
});


/* Data sources - enabling hide-show for new boxes */

$("a#add-data-source").click(function (){
	$("select[id*=data_sources]").change(function (){
		if ( $(this).find("option:eq(6), option:eq(5)").is(":selected") ){
			$(this).parent().parent().parent().find("li.name, li.company, li.email, li.phone").slideDown("fast");
		}
		else {
			$(this).parent().parent().parent().find("li.name, li.company, li.email, li.phone").slideUp("fast");
		}
	});
});

/* Deselecting radio buttons */

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


/* Leasing fees, purchase fees - area only visible if "for specified area" is selected */

$("li.annual_leasing_fee_area, li.purchase_price_area").css("display","none");

$("select#id_general_information-purchase_price_type").change(function (){
	if ( $(this).find("option:eq(1)").is(":selected") ){
		$("li.purchase_price_area").slideDown("fast");
	}
	else {
		$("li.purchase_price_area").slideUp("fast");
		$("li.purchase_price_area span input").val("");
	}
});

$("select#id_general_information-annual_leasing_fee_type").change(function (){
	if ( $(this).find("option:eq(1)").is(":selected") ){
		$("li.annual_leasing_fee_area").slideDown("fast");
	}
	else {
		$("li.annual_leasing_fee_area").slideUp("fast");
		$("li.annual_leasing_fee_area span input").val("");
	}
});

/* contract farming - everything invisible until "Yes" selected */

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

/* Quick placeholder for year-based data year field */

$("input.year-based-year").prop("placeholder","Year");


/* Employment: toggle visibility of subfields on click*/


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



$("tr:odd").addClass("odd");
$("tr:even").addClass("even");

$("div#deletions, div#inserts, div#updates, body#browse div.rule").addClass("tab-pane");
$("div.widgets, div.rules").addClass("tab-content");

$("body#manage #container ul,body#browse ul.rule-links").addClass("manage-nav nav nav-tabs");

$('ul.manage-nav li a[href="#updates"], ul.rule-links li a[href="#1"]').tab("show");

$('ul.manage-nav li a[href="#updates"]').click(function (e) {
  e.preventDefault();
  $(this).tab("show");
});

$('ul.manage-nav li a[href="#inserts"]').click(function (e) {
  e.preventDefault();
  $(this).tab("show");
});

$('ul.manage-nav li a[href="#deletions"]').click(function (e) {
  e.preventDefault();
  $(this).tab("show");
});

$('ul.rule-links li a[href="#1"]').click(function (e) {
  e.preventDefault();
  $(this).tab("show");
});

$('ul.rule-links li a[href="#empty"]').click(function (e) {
  e.preventDefault();
  $(this).tab("show");
});

/* Sticky headers for the browsing tables - WIP */

/*
clone = $('body#browse div#container thead').clone();
    $('body#browse div#container thead').after(clone);
    $('body#browse div#container thead:last').hide();

    offset = $('body#browse div#container thead:first').offset();
    var fromtop = offset.top;

    $(document).scroll(function() {
        doc = $(this);
        dist = $(this).scrollTop();

        if (dist >= fromtop - 120) {
            $('body#browse div#container thead:last').show();
            $('body#browse div#container thead:first').css({
                'position': 'fixed','width':'960px','z-index':'100','top':'120px','margin-left':'-1px'
            });
        } else {
            $('body#browse div#container thead:first').css({
                'position': 'static'
            });
            $('body#browse div#container thead:last').hide();
        }
    });
*/

$('#id_spatial_data-location').keyup(function (){
	map.setZoom(8);
});

/* Adding  bottom border on last investor */

$("div.forms a.add-row, div.forms a.delete-row").click(function() {
	$("ul.form[class*=investor]").removeClass("last-investor");
	$("ul.form[class*=investor]:last").addClass("last-investor");
});


$("li.intention, li.nature, li.negotiation_status, li.agreement_duration, li.implementation_status, li.contract_farming, li.community_reaction, li.community_consultation, li.community_compensation, li.community_benefits, li.land_owner, li.land_use, li.land_cover, li.water_extraction_envisaged, li.source_of_water_extraction li.tg_how_much_do_investors_pay_comment, li.source_of_water_extraction, li.lease_type, li.on_the_lease_farmers, li.on_the_lease_area, li.off_the_lease_farmers, li.off_the_lease_area").children("label").html('&nbsp;');




});

$(window).load(function(){

/* disabling checkboxes on "change" pages */

if($("input#id_general_information-intention_0, input#id_general_information-intention_1").is(":checked")) {
	$("input#id_general_information-intention_0, input#id_water-source_of_water_extraction_1").parent().parent().children("ul").find("input:checkbox").prop("disabled",false);
}
else {
	$("input#id_general_information-intention_0, input#id_general_information-intention_1, input#id_water-source_of_water_extraction_1").parent().parent().children("ul").find("input:checkbox").prop("disabled",true);
}


/*
	else {
		$("select[id^=id_data_sources]").parent().parent().parent().find("li.name, li.company, li.email, li.phone").css("display","none");
	}
*/

/* Centering Gmap */


/*
map.setCenter(new google.maps.LatLng($('#id_spatial_data-point_lat').val(), $('#id_spatial_data-point_lon').val() ));

if($('#id_spatial_data-point_lat').val().length == 0) {
	map.setZoom(2);
} else {
	map.setZoom(8);
}
*/
});







