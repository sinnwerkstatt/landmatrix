/**
 * OpenLayers 3 Layer Switcher Control.
 * See [the examples](./examples) for usage.
 * @constructor
 * @extends {ol.control.Control}
 * @param {Object} opt_options Control options, extends olx.control.ControlOptions adding:
 *                              **`tipLabel`** `String` - the button tooltip.
 * This control has been heavily customized, and is no longer compatible with
 * the original.
 *
 */
ol.control.LayerSwitcher = function(opt_options) {

    var options = opt_options || {};

    var tipLabel = options.tipLabel ?
        options.tipLabel : 'Legend';

    this.mapListeners = [];

    this.hiddenClassName = 'ol-unselectable ol-control layer-switcher';
    if (ol.control.LayerSwitcher.isTouchDevice_()) {
        this.hiddenClassName += ' touch';
    }
    this.shownClassName = this.hiddenClassName + ' shown';

    var element = document.createElement('div');
    element.className = this.hiddenClassName;

    var button = document.createElement('button');
    button.setAttribute('title', tipLabel);
    button.setAttribute('type', 'button'); // Don't submit forms on click!
    element.appendChild(button);

    var collapse = document.createElement('div');
    collapse.className = 'legendstuff';

    var formdiv = document.createElement('div');

    if (options.search) {
        var formgroup = document.createElement('div');
        formgroup.setAttribute('class', 'searchWrapper');

        var searchfield = document.createElement('input');
        searchfield.setAttribute('class', 'mapsearch');
        searchfield.setAttribute('type', 'search');

        var searchicon = document.createElement('span');
        searchicon.className = 'lm lm-search searchAddon';

        formgroup.appendChild(searchfield);
        formgroup.appendChild(searchicon);

        collapse.appendChild(formgroup);        
    }

    this.layerpanel = document.createElement('div');
    // TODO: Complete the collapse panel combo
    this.layerpanel.className = 'panel';
    this.layerpanel.setAttribute('class', 'layers');
    formdiv.appendChild(this.layerpanel);

    collapse.appendChild(formdiv);
    element.appendChild(collapse);

    var this_ = this;

    $(button).on('click', function(event) {
        $(this).siblings('.legendstuff').toggleClass('hidden');
    });
    $(collapse).mouseout().toggleClass('hidden');

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });

};

ol.inherits(ol.control.LayerSwitcher, ol.control.Control);

/**
 * Show the legend panel.
 */
ol.control.LayerSwitcher.prototype.showPanel = function () {
    if (this.element.className != this.shownClassName) {
        this.element.className = this.shownClassName;
        //this.renderPanel(); // CAREFUL. This destroys the whole custom legend operation for deals.
        // I wonder WHY exactly this is here, it seems to work just fine without - i personally never saw a reason
        // to rerender previously hidden stuff. Does it get moldy back there on some browsers?
    }
};

/**
 * Hide the legend panel.
 */
ol.control.LayerSwitcher.prototype.hidePanel = function () {

    if (this.element.className != this.hiddenClassName) {
        this.element.className = this.hiddenClassName;
    }
};

/**
 * Show a layer panel.
 */
ol.control.LayerSwitcher.prototype.toggleLayerPanel = function () {
    var chevron = $(this.lastElementChild);

    var collapse = $(this.nextSibling);
    if (collapse.hasClass('hidden') === true) {
        chevron.removeClass('lm-chevron-right').addClass('lm-chevron-down');
        collapse.removeClass('hidden');
    } else {
        chevron.removeClass('lm-chevron-down').addClass('lm-chevron-right');
        collapse.addClass('hidden');
    }

};

/**
 * Hide a layer panel.
 */
ol.control.LayerSwitcher.prototype.hideLayerPanel = function (panelname) {
    $(panelname).addClass('hidden');
};


/**
 * Re-draw the layer panel to represent the current state of the layers.
 */
ol.control.LayerSwitcher.prototype.renderPanel = function () {

    this.ensureTopVisibleBaseLayerShown_();

    while (this.layerpanel.firstChild) {
        this.layerpanel.removeChild(this.layerpanel.firstChild);
    }

    this.renderLayers_(this.getMap(), this.layerpanel);

};

/**
 * Set the map instance the control is associated with.
 * @param {ol.Map} map The map instance.
 */
ol.control.LayerSwitcher.prototype.setMap = function (map) {
    // Clean up listeners associated with the previous map
    for (var i = 0, key; i < this.mapListeners.length; i++) {
        this.getMap().unByKey(this.mapListeners[i]);
    }
    this.mapListeners.length = 0;
    // Wire up listeners etc. and store reference to new map
    ol.control.Control.prototype.setMap.call(this, map);

    if (map) {
        var this_ = this;
        /*this.mapListeners.push(map.on('pointerdown', function () {
            $('#legendstuff').addClass('hidden');
        })); */
        this.renderPanel();
    }
};

/**
 * Ensure only the top-most base layer is visible if more than one is visible.
 * @private
 */
ol.control.LayerSwitcher.prototype.ensureTopVisibleBaseLayerShown_ = function () {
    var lastVisibleBaseLyr;
    ol.control.LayerSwitcher.forEachRecursive(this.getMap(), function (l, idx, a) {
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
ol.control.LayerSwitcher.prototype.setVisible_ = function (lyr, visible) {
    var map = this.getMap();
    lyr.setVisible(visible);
    if (visible && lyr.get('type') === 'base') {
        // Hide all other base layers regardless of grouping
        ol.control.LayerSwitcher.forEachRecursive(map, function (l, idx, a) {
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
ol.control.LayerSwitcher.prototype.renderLayer_ = function (lyr, idx) {

    var this_ = this;
    var lyrTitle = lyr.get('title');
    var lyrId = lyr.get('title').replace(' ', '-') + '_' + idx;

    // Layer group?
    if (lyr.getLayers && !lyr.mapTypeId_) {
        var item = document.createElement('div');
        item.className = 'layer';


        var collapsename = lyrId + '_collapse';

        var label = document.createElement('a');

        item.className = 'layer-group';

        label.setAttribute('role', "button");
        label.setAttribute('aria-controls', collapsename);
        label.setAttribute('aria-expanded', false);

        label.innerHTML = '<i class="lm lm-chevron-down"></i>' + lyrTitle;
        label.onclick = this.toggleLayerPanel;

        item.appendChild(label);


        var ul = document.createElement('ul');
        ul.className = 'layercollapse';
        item.appendChild(ul);

        this.renderLayers_(lyr, ul);

    } else {
        var item = document.createElement('li');
        item.className = 'layer';

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
        input.onchange = function (e) {
            this_.setVisible_(lyr, e.target.checked);
        };
        item.appendChild(input);

        label.htmlFor = lyrId;

        if (lyrTitle === "Markers") {
            label.id = 'legendLabel';
        }

        if (lyrTitle.indexOf('area') > -1) {
            label.className = 'areaLabel';
        }

        label.innerHTML = lyrTitle;

        item.appendChild(label);

        if (lyrTitle === "Markers") {
            var legend = document.createElement('ul');
            legend.id = 'legend';
            item.appendChild(legend);
        }
    }

    return item;

};

/**
 * Render all layers that are children of a group.
 * @private
 * @param {ol.layer.Group} lyr Group layer whos children will be rendered.
 * @param {Element} elm DOM element that children will be appended to.
 */
ol.control.LayerSwitcher.prototype.renderLayers_ = function (lyr, elm) {
    var lyrs = lyr.getLayers().getArray().slice().reverse(),
        collectBaseLayers = !lyr.get('title'),
        baseLayers = [],
        i = 0, l;
    for (i = 0; i < lyrs.length; i++) {
        l = lyrs[i];
        if (collectBaseLayers && l.get('type') == 'base') {
            baseLayers.push(l);
        } else if (l.get('title')) {
            elm.appendChild(this.renderLayer_(l, i));
        }
    }
    // Group base layers into one group
    if (baseLayers.length > 0) {
        var baseGroup = new ol.layer.Group({
            title: 'Base Layers',
            layers: baseLayers
        });
        elm.appendChild(this.renderLayer_(baseGroup, i+1));
    }
};

/**
 * **Static** Call the supplied function for each layer in the passed layer group
 * recursing nested groups.
 * @param {ol.layer.Group} lyr The layer group to start iterating from.
 * @param {Function} fn Callback which will be called for each `ol.layer.Base`
 * found under `lyr`. The signature for `fn` is the same as `ol.Collection#forEach`
 */
ol.control.LayerSwitcher.forEachRecursive = function (lyr, fn) {
    lyr.getLayers().forEach(function (lyr, idx, a) {
        fn(lyr, idx, a);
        if (lyr.getLayers) {
            ol.control.LayerSwitcher.forEachRecursive(lyr, fn);
        }
    });
};

/**
* @private
* @desc Apply workaround to enable scrolling of overflowing content within an
* element. Adapted from https://gist.github.com/chrismbarr/4107472
*/
ol.control.LayerSwitcher.enableTouchScroll_ = function(elm) {
   if(ol.control.LayerSwitcher.isTouchDevice_()){
       var scrollStartPos = 0;
       elm.addEventListener("touchstart", function(event) {
           scrollStartPos = this.scrollTop + event.touches[0].pageY;
       }, false);
       elm.addEventListener("touchmove", function(event) {
           this.scrollTop = scrollStartPos - event.touches[0].pageY;
       }, false);
   }
};

/**
 * @private
 * @desc Determine if the current browser supports touch events. Adapted from
 * https://gist.github.com/chrismbarr/4107472
 */
ol.control.LayerSwitcher.isTouchDevice_ = function() {
    try {
        document.createEvent("TouchEvent");
        return true;
    } catch(e) {
        return false;
    }
};
