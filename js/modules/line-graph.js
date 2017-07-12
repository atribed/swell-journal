var d3 = require('d3');
var _  = require('underscore');

module.exports = {
  createSVG: function(selector, width, height, options) {
    var margin = options.margin;

    return d3.select(selector).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);
  },

  createGraph: function(svg, options) {
    var graph = svg.append("g")
        .attr("transform", "translate(" + options.margin.left + "," + options.margin.top + ")");

    return graph;
  },

  createPath: function(graph, data, lineCallback, options) {
    graph.append("path")
        .attr("class", "line")
        .attr(options.selector, "")
        .attr("d", lineCallback(data))
        .style("stroke", options.strokeColor);

    return graph;
  },

  createPaths: function(graph, paths) {
    _.each(paths, function(path) {
      graph = this.createPath(graph, path.data, path.lineCallback, path.options);
    }, this);

    return graph;
  },

  createDot: function(graph, data, cxCallback, cyCallback, options) {
    graph.selectAll("dot")
        .data(data)
        .enter().append("circle")
        .style("stroke", options.strokeColor)
        .style("stroke-width", options.strokeWidth)
        .style("fill", options.fillColor)
        .attr("r", options.radius)
        .attr(options.selector, "")
        .attr("cx", cxCallback)
        .attr("cy", cyCallback);

    return graph;
  },

  createDots: function(graph, plots) {
    _.each(plots, function(plot) {
      this.createDot(graph, plot.data, plot.cxCallback, plot.cyCallback, plot.options);
    }, this);

    return graph;
  },

  updatePath: function(graph, path) {
     graph.select('[' + path.options.selector + ']')
          .transition()
          .duration(1000)
          .attr("d", path.lineCallback(path.data));

     return graph;
  },

  updatePaths: function(graph, paths) {
    _.each(paths, function(path) {
      graph = this.updatePath(graph, path);
    }, this);

    return graph;
  },

  updateDot: function(graph, data, cxCallback, cyCallback, options) {
    var dotPts = graph.selectAll('[' + options.selector + ']').data(data);

    dotPts.enter().append("svg:circle");

    dotPts.style("stroke", options.strokeColor)
        .transition()
        .duration(options.transitionDuration)
        .attr("r", options.radius)
        .style("stroke-width", options.strokeWidth)
        .attr(options.selector, "")
        .style("fill", options.fillColor)
        .attr("cx", cxCallback)
        .attr("cy", cyCallback);

    dotPts.exit().remove();

    return graph;
  },

  updateDots: function(graph, dots) {
    _.each(dots, function(dot) {
      graph = this.updateDot(graph, dot.data, dot.cxCallback, dot.cyCallback, dot.options);
    }, this);

    return graph;
  },

  createLegend: function(key, svg, options) {
    var legend = svg.append("g")
      .attr("class", "legend")
      .attr("x", options.width - 65)
      .attr("y", 25)
      .attr("height", 100)
      .attr("width", 100);

    legend.selectAll('g').data(options.key)
        .enter()
        .append('g')
        .each(function(d, i) {
          var g = d3.select(this);
          legend.append("circle")
            .attr("r", 4)
            .style("fill", options.fillColor)
            .attr("cx", options.width - 65)
            .attr("cy", (i*25) + 4)
            .attr("width", 10)
            .attr("height", 10)
            .style("stroke", d.color)
            .style("stroke-width", "2")
            .style("fill", "white");

          legend.append("text")
            .attr("x", options.width - 50)
            .attr("y", i * 25 + 8)
            .attr("height",30)
            .attr("width",100)
            .text(d.name);
        });

    return svg;
  }
};
