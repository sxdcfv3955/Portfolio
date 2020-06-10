<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>지도 밀도 테스트입니당</title>
<style>
svg {
	background-color: #bfbfbf;
}

svg .municipality { fill: red; }
    svg .municipality:hover { stroke: #333; }
    svg .municipality.p0 { fill: #00FF4DFF; }
    svg .municipality.p1 { fill: #00E5FFFF; }
    svg .municipality.p2 { fill: #00C7FFFF; }
    svg .municipality.p3 { fill: #00A8FFFF; }
    svg .municipality.p4 { fill: #008AFFFF; }
    svg .municipality.p5 { fill: #006BFFFF; }
    svg .municipality.p6 { fill: #004CFFFF; }
    svg .municipality.p7 { fill: #002EFFFF; }
    svg .municipality.p8 { fill: #000FFFFF; }
    svg .municipality.p9 { fill: #0F00FFFF; }
    svg .municipality.p10 { fill: #2E00FFFF; }
    svg .municipality.p11 { fill: #4C00FFFF; }
</style>
</head>
<body>
	<div id="chart"></div>
	<script src="https://d3js.org/d3.v3.min.js"></script>
	<script src="https://d3js.org/topojson.v1.min.js"></script>
	<script src="https://d3js.org/queue.v1.min.js"></script>
	<script>
	var width = 1300,
    height = 800;

    var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height);
    
    var projection = d3.geo.mercator()
        .center([128, 36])
        .scale(8000)
        .translate([width/2, height/2]);

    var path = d3.geo.path()
        .projection(projection);
       
    var quantize = d3.scale.quantize()
        .domain([0, 10000])
        .range(d3.range(12).map(function(i) { return "p" + i; }));

    var popByName = d3.map();

    queue()
        .defer(d3.json, "https://raw.githubusercontent.com/sxdcfv3955/byun/map/kormap.json")
        .defer(d3.csv, "https://raw.githubusercontent.com/sxdcfv3955/byun/map/densityA.csv", function(d) {
            popByName.set(d.name, +d.population);
        })
        .await(ready);
    
    var zoom = d3.behavior.zoom()
    .translate(projection.translate())
    .scale(projection.scale())
    .scaleExtent([height, 200 * height])
    .on("zoom", zoomed);
    
    var g = svg.append("g")
    .call(zoom);

    function ready(error, data) {
      var features = topojson.feature(data, data.objects["municipalities-geo"]).features;

      features.forEach(function(d) {
        d.properties.population = popByName.get(d.properties.name);
        d.properties.density = d.properties.population;
        d.properties.quantized = quantize(d.properties.density);
      });

      g.selectAll("path")
       .on("click", clicked)
          .data(features)
        .enter().append("path")
          .attr("class", function(d) { return "municipality " + d.properties.quantized; })
          .attr("d", path)
          .attr("id", function(d) { return d.properties.name; })
        .append("title")
        .text(function(d) { return d.properties.name + ": " + d.properties.population + "마리" });
    }
    
    function clicked(d) {
    	  var centroid = path.centroid(d),
    	      translate = projection.translate();

    	  projection.translate([
    	    translate[0] - centroid[0] + width,
    	    translate[1] - centroid[1] + height
    	  ]);

    	  zoom.translate(projection.translate());

    	  g.selectAll("path").transition()
    	      .duration(500)
    	      .attr("d", path);
    	}

    	function zoomed() {
    	  projection.translate(d3.event.translate).scale(d3.event.scale);
    	  g.selectAll("path").attr("d", path);
    	}
    
    </script>

</body>
</html>