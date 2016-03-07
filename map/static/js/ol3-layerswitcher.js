/**
 * OpenLayers 3 Layer Switcher Control.
 * See [the examples](./examples) for usage.
 * @constructor
 * @extends {ol.control.Control}
 * @param {Object} opt_options Control options, extends olx.control.ControlOptions adding:
 *                              **`tipLabel`** `String` - the button tooltip.
 */
ol.control.LayerSwitcher = function(opt_options) {

    var options = opt_options || {};

    var tipLabel = options.tipLabel ?
      options.tipLabel : 'Legend';

    this.mapListeners = [];

    this.hiddenClassName = 'ol-unselectable ol-control layer-switcher';
    this.shownClassName = this.hiddenClassName + ' shown';

    var element = document.createElement('div');
    element.className = this.hiddenClassName;

    var button = document.createElement('button');
    button.setAttribute('title', tipLabel);
    element.appendChild(button);

    var collapse = document.createElement('div');
    collapse.setAttribute('id', 'legendstuff');
    collapse.className = 'panel-collapse collapse in';

    var form = document.createElement('form');
    form.setAttribute('role', 'form');

    var formgroup = document.createElement('div');
    formgroup.className = 'form-group has-feedback panel';

    var searchfield = document.createElement('input');
    searchfield.setAttribute('id', 'mapsearch');
    searchfield.setAttribute('class', 'control');
    searchfield.setAttribute('type', 'text');

    formgroup.appendChild(searchfield);
    form.appendChild(formgroup);

    this.legend = document.createElement('div');
    this.legend.className = 'panel';
    this.legend.setAttribute('id', 'legend');
    form.appendChild(this.legend);


    collapse.appendChild(form);


    /*var innerHTML = '<form role="form">';
    innerHTML = innerHTML + '  <div class="form-group has-feedback">';
    innerHTML = innerHTML + '    <select id="mapsearch-select" class="nav-select">';
    innerHTML = innerHTML + '    </select>';
    innerHTML = innerHTML + '  </div>';
    innerHTML = innerHTML + '</form>';

    this.search.innerHTML = innerHTML;
    element.appendChild(this.search); */


    this.layerpanel = document.createElement('div');
    // TODO: Complete the collapse panel combo
    this.layerpanel.className = 'panel';
    this.layerpanel.setAttribute('id', 'layers');
    collapse.appendChild(this.layerpanel);

    element.appendChild(collapse);

    var this_ = this;


    element.onmouseover = function(e) {
        this_.showPanel();
    };

    button.onclick = function(e) {
        this_.showPanel();
    };

    element.onmouseout = function(e) {
        e = e || window.event;
        if (!element.contains(e.toElement)) {
            this_.hidePanel();
        }
    };

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });
    initGeocoder(searchfield);

};

ol.inherits(ol.control.LayerSwitcher, ol.control.Control);

/**
 * Show the legend panel.
 */
ol.control.LayerSwitcher.prototype.showPanel = function() {
    if (this.element.className != this.shownClassName) {
        this.element.className = this.shownClassName;
        this.renderPanel();
    }
};

/**
 * Hide the legend panel.
 */
ol.control.LayerSwitcher.prototype.hidePanel = function() {
    if (this.element.className != this.hiddenClassName) {
        this.element.className = this.hiddenClassName;
    }
};

/**
 * Show a layer panel.
 */
ol.control.LayerSwitcher.prototype.toggleLayerPanel = function() {
    console.log(this);
    var chevron = $(this.lastElementChild);

    var collapse = $(this.nextSibling);
    if (collapse.hasClass('hidden') === true) {
        console.log('Uncollapsing layer group panel');
        chevron.removeClass('lm-chevron-right').addClass('lm-chevron-down');
        collapse.removeClass('hidden');
    } else {
        console.log('Collapsing layer group panel');
        chevron.removeClass('lm-chevron-down').addClass('lm-chevron-right');
        collapse.addClass('hidden');
    }

};

/**
 * Hide a layer panel.
 */
ol.control.LayerSwitcher.prototype.hideLayerPanel = function(panelname) {
    $(panelname).addClass('hidden');
};



/**
 * Re-draw the layer panel to represent the current state of the layers.
 */
ol.control.LayerSwitcher.prototype.renderPanel = function() {

    this.ensureTopVisibleBaseLayerShown_();

    while(this.layerpanel.firstChild) {
        this.layerpanel.removeChild(this.layerpanel.firstChild);
    }

    var ul = document.createElement('div');
    //ul.className = '';
    this.layerpanel.appendChild(ul);
    this.renderLayers_(this.getMap(), ul);

};

/**
 * Set the map instance the control is associated with.
 * @param {ol.Map} map The map instance.
 */
ol.control.LayerSwitcher.prototype.setMap = function(map) {
    // Clean up listeners associated with the previous map
    for (var i = 0, key; i < this.mapListeners.length; i++) {
        this.getMap().unByKey(this.mapListeners[i]);
    }
    this.mapListeners.length = 0;
    // Wire up listeners etc. and store reference to new map
    ol.control.Control.prototype.setMap.call(this, map);
    if (map) {
        var this_ = this;
        this.mapListeners.push(map.on('pointerdown', function() {
            this_.hidePanel();
        }));
        this.renderPanel();
    }
};

/**
 * Ensure only the top-most base layer is visible if more than one is visible.
 * @private
 */
ol.control.LayerSwitcher.prototype.ensureTopVisibleBaseLayerShown_ = function() {
    var lastVisibleBaseLyr;
    ol.control.LayerSwitcher.forEachRecursive(this.getMap(), function(l, idx, a) {
        if (l.get('type') === 'base' && l.getVisible()) {
            lastVisibleBaseLyr = l;
        }
    });
    if (lastVisibleBaseLyr) this.setVisible_(lastVisibleBaseLyr, true);
};

/**
 * Toggle the visible state of a layer.
 * Takes care of hiding other layers in the same exclusive group if the layer
 * is toggle to visible.
 * @private
 * @param {ol.layer.Base} The layer whos visibility will be toggled.
 */
ol.control.LayerSwitcher.prototype.setVisible_ = function(lyr, visible) {
    var map = this.getMap();
    lyr.setVisible(visible);
    if (visible && lyr.get('type') === 'base') {
        // Hide all other base layers regardless of grouping
        ol.control.LayerSwitcher.forEachRecursive(map, function(l, idx, a) {
            if (l != lyr && l.get('type') === 'base') {
                l.setVisible(false);
            }
        });
    }
};

/**
 * Render all layers that are children of a group.
 * @private
 * @param {ol.layer.Base} lyr Layer to be rendered (should have a title property).
 * @param {Number} idx Position in parent group list.
 */
ol.control.LayerSwitcher.prototype.renderLayer_ = function(lyr, idx) {

    var this_ = this;

    var item = document.createElement('div');
    item.className = '';

    var lyrTitle = lyr.get('title');
    var lyrId = lyr.get('title').replace(' ', '-') + '_' + idx;


    if (lyr.getLayers) {

        var collapsename = lyrId+'Collapse';

        var label = document.createElement('a');

        item.className = 'layer-group';

        label.setAttribute('role' ,"button");
        label.setAttribute('aria-controls', collapsename);
        label.setAttribute('aria-expanded', false);

        label.innerHTML = '<i class="lm lm-chevron-down"></i>' + lyrTitle;
        label.onclick = this.toggleLayerPanel;

        item.appendChild(label);


        var div = document.createElement('div');
        div.className = 'layercollapse';
        div.setAttribute('id', collapsename);
        var ul = document.createElement('ul');
        div.appendChild(ul);
        item.appendChild(div);

        this.renderLayers_(lyr, ul);

    } else {
        var label = document.createElement('label');

        var input = document.createElement('input');
        if (lyr.get('type') === 'base') {
            input.type = 'radio';
            input.name = 'base';
        } else {
            input.type = 'checkbox';
        }
        input.id = lyrId;
        input.checked = lyr.get('visible');
        input.onchange = function(e) {
            this_.setVisible_(lyr, e.target.checked);
        };
        item.appendChild(input);

        label.htmlFor = lyrId;
        label.innerHTML = lyrTitle;
        item.appendChild(label);

    }

    return item;

};

/**
 * Render all layers that are children of a group.
 * @private
 * @param {ol.layer.Group} lyr Group layer whos children will be rendered.
 * @param {Element} elm DOM element that children will be appended to.
 */
ol.control.LayerSwitcher.prototype.renderLayers_ = function(lyr, elm) {
    var lyrs = lyr.getLayers().getArray().slice().reverse();
    for (var i = 0, l; i < lyrs.length; i++) {
        l = lyrs[i];
        if (l.get('title')) {
            elm.appendChild(this.renderLayer_(l, i));
        }
    }
};

/**
 * **Static** Call the supplied function for each layer in the passed layer group
 * recursing nested groups.
 * @param {ol.layer.Group} lyr The layer group to start iterating from.
 * @param {Function} fn Callback which will be called for each `ol.layer.Base`
 * found under `lyr`. The signature for `fn` is the same as `ol.Collection#forEach`
 */
ol.control.LayerSwitcher.forEachRecursive = function(lyr, fn) {
    lyr.getLayers().forEach(function(lyr, idx, a) {
        fn(lyr, idx, a);
        if (lyr.getLayers) {
            ol.control.LayerSwitcher.forEachRecursive(lyr, fn);
        }
    });
};
