var tree_margin = {top: 0, right: 320, bottom: 0, left: 0},
    tree_width = 960 - tree_margin.left - tree_margin.right,
    tree_height = 500 - tree_margin.top - tree_margin.bottom,
    parent_type = 'stakeholders',
    tree, tree_svg, tree_data;

function init_investor_form(form) {
    // Init buttons
    form.find('.add-form').click(function () {
        $(this).parents('.panel-body').find('.formset-add-form').trigger('click');
    });
    form.find('.remove-form').click(function () {
        form.find('.formset-remove-form').trigger('click');
    });


    function formatInvestor (investor) {
        return investor.text;
    }
    function formatInvestorSelection (investor) {
        return investor.text;
    }
    var investorfield = form.find('select.investorfield');
    investorfield.select2({
        ajax: {
            url: '/api/investors.json',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
        minimumInputLength: 3,
        templateResult: formatInvestor,
        templateSelection: formatInvestorSelection
    }).on('change', function () {
        generateButtons($(this));
        loadInvestorNetwork($(this).val());
    });
    generateButtons(investorfield);

    form.find('.loans_date input').attr('placeholder', 'YYYY-MM-DD');
    form.find('.loans_currency select').select2();
}

function generateButtons(field) {
    var investorId = field.val();
    var addLink = '/stakeholder/add/';
    //var parentId = $('#id_id').val();
    //if (parentId) {
    //    addLink = addLink + '?parent_id=' + parentId;
    //}

    var buttons = '<a id="add_' + $(field).attr("id") + '" class="add-investor" href="' + addLink + '" class="noul"><i class="lm lm-plus"></i></a>';
    if (field.val() !== '') {
        buttons += '<a id="change_' + $(field).attr("id") + '" class="change-investor" href="/stakeholder/' + investorId + '/" class="noul"><i class="lm lm-pencil"></i></a>';
    }
    var wrap = '<span class="investorops">' + buttons + '</span>';

    field.parent().find('.investorops').remove();
    field.parent().append(wrap);
    //field.parent().parent().parent().append('<div id="chart' + index + '"></div>');

    // Bind handlers
    $('a.add-investor').click(function (e) {
      e.preventDefault()
      showAddInvestorPopup(this);
      return False;
    });
    $('a.change-investor').click(function (e) {
      e.preventDefault()
      showChangeInvestorPopup(this);
      return False;
    });

}

function stakeholderAdded(row) {
    // Update form counters
    var form_count = 1;
    row.parent().find('h3 small').each(function () {
        $(this).text('#' + form_count++);
    });
    // Unselect selected options
    row.find("option:selected").removeAttr("selected");
    row.find(".select2").remove();
    row.find(".select2-hidden-accessible").removeClass("select2-hidden-accessible").data('select2', null);
    init_investor_form(row);
    // Scroll to the new row
    $('html, body').animate({
        scrollTop: row.offset().top
    }, 600);
}
function stakeholderRemoved(row) {
    // Update form counters
    var form_count = 1;
    row.parent().find('small').each(function () {
        $(this).text('#' + form_count++);
    });
}

$(document).ready(function () {
    $('.country select').select2();
            
    $('.parent-companies-form').formset({
        addText: '<i class="fa fa-plus"></i> {% trans "Add another" %}',
        addCssClass: 'formset-add-form hidden',
        deleteText: '<i class="fa fa-minus"></i> {% trans "Remove" %}',
        deleteCssClass: 'formset-remove-form hidden',
        prefix: 'parent-stakeholder-form',
        formCssClass: 'parent-companies-form',
        //extraClasses: ['dynamic-form'],
        added: stakeholderAdded,
        removed: stakeholderRemoved,
    }).each(function () { init_investor_form($(this)); });
    $('.parent-investors-form').formset({
        addText: '<i class="fa fa-plus"></i> {% trans "Add another" %}',
        addCssClass: 'formset-add-form hidden',
        deleteText: '<i class="fa fa-minus"></i> {% trans "Remove" %}',
        deleteCssClass: 'formset-remove-form hidden',
        prefix: 'parent-investor-form',
        formCssClass: 'parent-investors-form',
        //extraClasses: ['dynamic-form'],
        added: stakeholderAdded,
        removed: stakeholderRemoved,
    }).each(function () { init_investor_form($(this)); });


    // Init operational company field (deal add/edit)
    $(".investorfield").each(function (index) {
        var investorId = $(this).val();
        $(this).select2({
            placeholder: 'Select Investor'
        });
        /*
         var investorId = $(this).val();
         $(this).select2({
         placeholder: 'Select Investor',
         ajax: {
         url: '/api/investors.json',
         cache: true
         }
         });
         */
        generateButtons($(this), index);
        $(this).on('change', function () {
            generateButtons($(this), index);
            loadInvestorNetwork($(this).val());
        });
        loadInvestorNetwork(investorId);
    });
    var dataSwitch = $("[name='parent_type']");
    dataSwitch.bootstrapSwitch({
        onText: 'Parent&nbsp;companies',
        offText: 'Parent&nbsp;investors',
        offColor: 'info',
        onSwitchChange: function(event, state) {
            if (state) {
                parent_type = 'stakeholders';
            } else {
              console.log("investors");
                parent_type = 'investors';
            }
            createInvestorNetwork();
        }
    });
});


/* PEDIGREE */
function loadInvestorNetwork(investorId) {
    if (investorId <= 0) {
        return;
    }
    d3.json("/api/investor_network.json?operational_stakeholder=" + investorId,
        function (data) {
            tree_data = data;
            createInvestorNetwork();
        }
    );
}

//function buildHierarchy(data) {
//  // First level?
//  if (typeof data.involvement === 'undefined') {
//      parent = {"name": "root", "children": []};
//  } else {
//      parent = {"name": data.name, "children": []};
//  }
//  var items = data.parent_stakeholders,
//      children = [];
//  for (var i = 0; i < items.length; i++) {
//    var item = items[i];
//    children.push(buildHierarchy_sunburst(item));
//  }
//  parent.children = children;
//  return parent;
//};

function createInvestorNetwork() {
  tree = d3.layout.tree()
      .separation(function(a, b) { return a.parent === b.parent ? 1 : .5; })
      .children(function(d) { return parent_type == 'investors' && d.parent_investors || d.parent_stakeholders; })
      .size([tree_height, tree_width]);
  $('#investor-network').removeClass().addClass(parent_type);
  d3.select("#investor-network").select("svg").remove();
  tree_svg = d3.select("#investor-network").append("svg")
      .attr("width", tree_width + tree_margin.left + tree_margin.right)
      .attr("height", tree_height + tree_margin.top + tree_margin.bottom)
    .append("g")
      .attr("transform", "translate(" + tree_margin.left + "," + tree_margin.top + ")");

  var nodes = tree.nodes(tree_data);

  var link = tree_svg.selectAll(".link")
      .data(tree.links(nodes))
    .enter().append("path")
      .attr("class", "link")
      .attr("fill", "none")
      .attr("stroke-width", "#000000")
      .attr("stroke-opacity", "1")
      .attr("stroke-width", "2px")
      .attr("d", elbow);

  var node = tree_svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

  node.append("text")
      .attr("class", "name")
      .attr("font-weight", "bold")
      .attr("x", function (d) { if (d.involvement) { return 8; } else { return 16; } })
      .attr("y", -6)
      .text(function(d) { return d.name; });

  node.append("text")
      .attr("x", function (d) { if (d.involvement) { return 8; } else { return 16; } })
      .attr("y", 8)
      .attr("dy", ".71em")
      .attr("class", "about type")
      .attr("font-size", "80%")
      .text(function(d) {
        if (d.involvement) {
          var inv = d.involvement;
          return (parent_type == "investors" && "Parent investor" || "Parent company") + 
            (inv.percentage && " ("+inv.percentage+"%"+(inv.investment_type && " "+inv.investment_type || "")+")" || "");
        } else {
          return "Operational company";
        }
      });

  node.append("circle")
    .attr("cx", function (d) { if (d.involvement) { return 0; } else { return 9; } })
    .attr("cy", 0)
    .attr("r", 8)
    .attr("class", "circle")
    .on("click", function (d) {
        var modal = $('#stakeholder');
        modal.find('.modal-header h4').text(d.name);
        var data = [
            d.country,
            d.classification,
            d.parent_relation,
            d.homepage && '<a target="_blank" href="'+d.homepage+'">'+d.homepage+'</a>',
            d.opencorporates_link && '<a target="_blank" href="'+d.opencorporates_link+'">'+d.opencorporates_link+'</a>',
            d.comment,
          ].filter(function (val) {return val;}).join('<br>'); 
        modal.find('.modal-body p').html(data);
        modal.modal("show");
    });

  node.append("text")
      .attr("x", function (d) { if (d.involvement) { return 8; } else { return 16; } })
      .attr("y", 8)
      .attr("dy", "1.86em")
      .attr("font-size", "80%")
      .attr("class", "about involvement")
      .text(function(d) {
        if (d.involvement) {
          var inv = d.involvement;
          return [
            inv.loans_amount && inv.loans_amount + inv.loans_currency + (inv.loans_date && " ("+inv.loans_date+")"),
            inv.comment
          ].filter(function (val) {return val;}).join(', '); 
        }
      });
};

function elbow(d, i) {
  return "M" + d.source.y + "," + d.source.x
       + "H" + d.target.y + "V" + d.target.x
       + (d.target.children ? "" : "h" + tree_margin.right);
}
