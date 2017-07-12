var d3 = require('d3');
var utils = require('./modules/utils');
var lineGraph = require('./modules/line-graph');
var _ = require('underscore');
var $ = require('jquery');

var margin = {top: 20, right: 80, bottom: 30, left: 50};
var width = 960 - margin.left - margin.right;
var height = 500 - margin.top - margin.bottom;

var svg = lineGraph.createSVG('#visualisation', width, height, {margin: margin});
var graph = lineGraph.createGraph(svg, {margin: margin});

function dataDateFunc(scaler, dateKey) {
  return function(d) {
    return scaler(utils.formatD3DateEST(d[dateKey]));
  };
}

function heightDataFunc(scaler, dataKey) {
  return function(d) {
    return scaler(d[dataKey] * 3.28084);
  }
}

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var swell_ht_line = d3.svg.line()
    .interpolate("monotone")
    .x(dataDateFunc(x, 'date'))
    .y(heightDataFunc(y, 'swell_ht'));

var wave_ht_line = d3.svg.line()
    .interpolate("monotone")
    .x(dataDateFunc(x, 'date'))
    .y(heightDataFunc(y, 'wave_height'));

var wind_ht_line = d3.svg.line()
    .interpolate("monotone")
    .x(dataDateFunc(x, 'date'))
    .y(heightDataFunc(y, 'wind_ht'));

var dots = [
    {
      data: [],
      cxCallback: dataDateFunc(x, 'date'),
      cyCallback: heightDataFunc(y, 'swell_ht'),
      options: {
        selector: 'data-swell-ht-dots',
        strokeColor: '#91dc85',
        fillColor: 'white',
        strokeWidth: 1,
        radius: 3,
        transitionDuration: 1000
      }
    },
    {
      data: [],
      cxCallback: dataDateFunc(x, 'date'),
      cyCallback: heightDataFunc(y, 'wind_ht'),
      options: {
        selector: 'data-wind-ht-dots',
        strokeColor: '#9ee8ff',
        fillColor: 'white',
        strokeWidth: 1,
        radius: 3,
        transitionDuration: 1000
      }
    },
    {
      data: [],
      cxCallback: dataDateFunc(x, 'date'),
      cyCallback: heightDataFunc(y, 'wave_height'),
      options: {
        selector: 'data-swell-ht-dots',
        strokeColor: '#cb4343',
        fillColor: 'white',
        strokeWidth: 1,
        radius: 3,
        transitionDuration: 1000
      }
    }
  ];

var paths = [
    {data: [], lineCallback: swell_ht_line, options: {strokeColor: '#91dc85', selector: 'data-swell-ht-line'}},
    {data: [], lineCallback: wave_ht_line, options: {strokeColor: '#cb4343', selector: 'data-wave-ht-line'}},
    {data: [], lineCallback: wind_ht_line, options: {strokeColor: '#9ee8ff', selector: 'data-wind-ht-line'}}
  ];


var data = $('#buoy-options').serialize();
$.ajax({
  url: '/buoy_info',
  data: data,
  processData: false,
  contentType: false,
  success: function(data) {
    x.domain(d3.extent(data, function(d) { return utils.formatD3DateEST(d.date); }));
    y.domain([0, d3.max(data, function(d) {return d.wave_height * 3.28084 + .5})]);

    graph.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    graph.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Height (ft)");

    _.each(paths, function(path) {
      path.data = data;
    });

    graph = lineGraph.createPaths(graph, paths);

    _.each(dots, function(dot) {
      dot.data = data;
    });

    graph = lineGraph.createDots(graph, dots);

    var key = [
        {name: "Primary Wave Height", color: "#cb4343"},
        {name: "Swell Wave Height", color: "#91dc85"},
        {name: "Wind Wave Height", color: "#33c3f0"}
    ];

    var legendOptions = {
      fillColor: "white",
      width: width,
      key: key
    };
    svg = lineGraph.createLegend(key, svg, legendOptions);
  }
});

document.body.addEventListener('change', function(e) {
  if(e.target.hasAttribute('data-buoy-option')) {
    var data = $('#buoy-options').serialize();

    $.ajax({
      url: '/buoy_info',
      data: data,
      dataType: 'json',
      processData: false,
      contentType: false,
      success: function(data) {
        x.domain(d3.extent(data, function(d) { return utils.formatD3DateEST(d.date); }));
        y.domain([0, d3.max(data, function(d) {return d.wave_height * 3.28084 + .5})]);

        graph.selectAll("g.x.axis")
            .call(xAxis);

        graph.selectAll("g.y.axis")
            .call(yAxis);

        _.each(paths, function(path) {
          path.data = data;
        });

        graph = lineGraph.updatePaths(graph, paths);

        _.each(dots, function(dot) {
          dot.data = data;
        });

        graph = lineGraph.updateDots(graph, dots);
      }
    });
}});
