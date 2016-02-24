$(document).ready(function () {
    console.log('Deal Detail js loaded.');
    $(".investorfield").each(function (index) {
        var investorops = $('<span><a href="stakeholder/add" target="_blank"><i class="lm lm-plus"></i></a><a href="stakeholder/edit" target="_blank"><i class="lm lm-edit"></i></a></span>');
        this.append(investorops);
    });
});
