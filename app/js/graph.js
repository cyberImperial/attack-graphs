let svg = d3.select("#graph-container")
      .append("svg")
      .attr("width", "1400px")
      .attr("height", "800px")
      .call(d3.zoom().on("zoom", function () {
              svg.attr("transform", d3.event.transform)
      }))
      .append("g"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

let graph = {
  "nodes": [
    {"id": "ip1"},
    {"id": "ip2"},
    {"id": "ip3"},
    {"id": "ip4"}
  ],
  "links": [
    {"source": "ip1", "target": "ip2", "value": 1},
    {"source": "ip3", "target": "ip2", "value": 1},
    {"source": "ip4", "target": "ip1", "value": 1}
  ]
}


let defs = svg.append("svg:defs");

defs.append("svg:pattern")
    .attr("width", 1)
    .attr("height", 1)
    .attr("id", "server")
    .append("svg:image")
    .attr("xlink:href", "img/server.png")
    .attr("width", 100)
    .attr("height", 100)
    .attr("x", 12)
    .attr("y", 0);

let simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(function(d) {
                    return d.id;
                }).distance(150))
                .force("charge", d3.forceManyBody().strength(-5))
                .force("center", d3.forceCenter(750, 400))
                .force("collide", d3.forceCollide(100));


let link = svg.selectAll(".link")
            .data(graph.links, function(d) {return d.target.id;})
            .enter().append("line").attr("class", "link");

let node = svg.selectAll(".node")
            .data(graph.nodes, function(d) {return d.id;})
            .enter().append("g").attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

node.append("circle")
    .attr("r", 60)
    .style("fill", "url(#server)");

node.append("title")
    .text(function(d) { return d.id; });

simulation.nodes(graph.nodes)
    .on("tick", ticked);

simulation.force("link")
    .links(graph.links);

function initializeDistance() {
  if (!nodes) return;
  for (var i = 0, n = links.length; i < n; ++i) {
    distances[i] = +distance(links[i], i, links);
  }
}

function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
            return "translate(" + d.x + ", " + d.y + ")";
        });
  }

function dragstarted(d) {
    if (!d3.event.active)  {
        simulation.alphaTarget(0.3).restart();
    }
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    //if (!d3.event.active) {
      //  simulation.alphaTarget(0);
    //}
    //d.fx = null;
    //d.fy = null;
}
