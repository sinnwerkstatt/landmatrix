$(document).ready(function () {
    console.log('Deal Detail js loaded.');

    // TODO: Get Investor ID from Select and replace edit url
    $(".investorfield").parent().append('<span class="investorops"><a href="/stakeholder" target="_blank"><i class="lm lm-plus"></i></a><a href="/stakeholder/25" target="_blank"><i class="lm lm-pencil"></i></a></span>');
});
