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
    svg .municipality.p0 { fill: #FFFFD5FF; }
    svg .municipality.p1 { fill: #FFFF80FF; }
    svg .municipality.p2 { fill: #FFFF2AFF; }
    svg .municipality.p3 { fill: #FFFF00FF; }
    svg .municipality.p4 { fill: #FFDF00FF; }
    svg .municipality.p5 { fill: #FFBF00FF; }
    svg .municipality.p6 { fill: #FF9F00FF; }
    svg .municipality.p7 { fill: #FF8000FF; }
    svg .municipality.p8 { fill: #FF6000FF; }
    svg .municipality.p9 { fill: #FF4000FF; }
    svg .municipality.p10 { fill: #FF2000FF; }
    svg .municipality.p11 { fill: #FF0000FF; }

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