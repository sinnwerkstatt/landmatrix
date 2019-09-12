
function Factbook(data, dimensions, dimsUnit, dependencyData) {
  this.dependencyData = dependencyData;
  this.dimsUnit = dimsUnit;
  this.numericFilter = {};
  this.ordinalFilter = {};
  this.dependencyFilter = {};
  this.data = data;
  this.dimensions = dimensions;
  this.countries = {};
  this.domain = {};
  
  for (var i in this.dimensions) {
    var min = 100000000,
        max = 0,
        k = this.dimensions[i];
    for (var j in this.data) {
      if (this.data[j][k] < min)
        min = this.data[j][k];
      else if (this.data[j][k] > max)
        max = this.data[j][k];
    }
    this.domain[k] = {'min': min, 'max': max};
  }
  for (var i in this.data) {
    this.ordinalFilter[this.data[i]['Name']] = undefined;
    this.countries[this.data[i]['Name']] = i;
  }
}

Factbook.prototype.getConnectingCountries = function(country){
    var result = [];
    if (this.dependencyData[country]){
        for (country2 in this.dependencyData[country]){
            // absolute filter
            if (dependencyData[country][country2].d>absoluteGraphThreshold){
                // check if a filter is present
                if (factbook.dependencyFilter.min && factbook.dependencyFilter.max){
                    // check against filter values
                    if (dependencyData[country][country2].d < factbook.dependencyFilter.max
                        && dependencyData[country][country2].d > factbook.dependencyFilter.min){
                        result.push(country2);
                    }
                } else {
                    result.push(country2);
                }
            }
        }
        return result;
    }
    return result;
}

Factbook.prototype.isFiltered = function(d) {
  if (!(d.Name in this.ordinalFilter))
    return true;
  for (var t in this.numericFilter) {
    if (d[t] < this.numericFilter[t].min
	    || d[t] > this.numericFilter[t].max) {
      return true;
    }
  }
  return false;
}

Factbook.prototype.assertFilter = function(t) {
  if (!(t in this.numericFilter))
    this.numericFilter[t] = {
      min: this.domain[t].min,
      max: this.domain[t].max};
}

Factbook.prototype.resetFilter = function(t) {
  if (arguments.length == 1) {
    var newNumericFilter = {};
    for (var k in this.numericFilter) {
      if (k != t)
        newNumericFilter[k] = {
          min: this.numericFilter[k].min,
          max: this.numericFilter[k].max};
    }
    this.numericFilter = newNumericFilter;
  }
  else {
    this.ordinalFilter[t] = {};
    for (var k in this.countries) {
      this.ordinalFilter[k] = undefined;
    }
  }
}

Factbook.prototype.getFilterBounds = function(t) {
  return (t in this.numericFilter) ? this.numericFilter[t] : this.domain[t];
}

Factbook.prototype.getFiltered = function() {
  var filtered = [];
  for (var i = 0; i < this.data.length; i++) {
    if (this.isFiltered(this.data[i]))
      filtered.push(this.data[i]);
  }
  return filtered;
}

Factbook.prototype.getUnfiltered = function() {
  var unfiltered = [];
  for (var i = 0; i < this.data.length; i++) {
    if (!this.isFiltered(this.data[i]))
      unfiltered.push(this.data[i]);
  }
  return unfiltered;
}

Factbook.prototype.getFilteredCountries = function() {
  var filtered = {};
  for (var i = 0; i < this.data.length; i++) {
    if (this.isFiltered(this.data[i]))
      filtered[this.data[i].Name] = undefined;
  }
  return filtered;
}

Factbook.prototype.getUnfilteredCountries = function() {
  var unfiltered = {};
  for (var i = 0; i < this.data.length; i++) {
    if (!this.isFiltered(this.data[i]))
      unfiltered[this.data[i].Name] = undefined;
  }
  return unfiltered;
}

Factbook.prototype.getCountryData = function(o) {
  if (typeof(o) == "string") {
    if (!(o in this.countries)) {
      if (debug) console.log("lib_factbook.js: '" + o + "' not in Factbook data.");
      return [];
    }
    return Array(this.data[this.countries[o]]);
  }
  else {
    var data = [];
    for (var i = 0; i < o.length; i++) {
      if (o[i] in this.countries)
        data.push(this.data[this.countries[o[i]]]);
      else if (debug)
        console.log("lib_factbook.js: '" + o + "' not in Factbook data.");
    }
    return data;
  }
}

Factbook.prototype.filterIsZeroSpan = function(t) {
  return this.numericFilter[t].min == this.numericFilter[t].max;
}

Factbook.prototype.filterIsModified = function(t) {
  if (!(t in this.numericFilter))
    return false;
  return (this.numericFilter[t].min != this.domain[t].min
    || this.numericFilter[t].max != this.domain[t].max);
}