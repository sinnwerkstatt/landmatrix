$(document).ready(function () {
    (function() {
        'use strict';

        function LocationWidget(options) {
            // defaults
            this.options = {
                geocoder: new google.maps.Geocoder()
            }; 
            for (var property in options) {
                if (options.hasOwnProperty(property)) {
                    this.options[property] = options[property];
                }
            }
            this.locationField = document.getElementById(this.options.id);
            var autocomplete = new google.maps.places.Autocomplete(this.locationField);

            // Google maps doesn't let us bind this for event handlers easily,
            // so just use a closure
            if (this.options.mapWidget) {
                var mapWidget = this.options.mapWidget;

                var onPlaceChanged = function() {
                    var place = autocomplete.getPlace();
                    if (place.geometry) {
                        mapWidget.updateFromPlaceData(place);
                    }
                    else {
                        $('#alert_placeholder').html(
                            '<div class="alert alert-warning alert-dismissible" role="alert">' +
                            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                            '<span aria-hidden="true">&times;</span></button><span>' +
                            'Sorry, that place cannot be found.</span></div>');
                    }
                };

                autocomplete.addListener('place_changed', onPlaceChanged);
            }
            this.autocomplete = autocomplete;
        }

        window.LocationWidget = LocationWidget;
    })();
});

