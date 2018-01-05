const jquery = require("jquery");
const host = "http://127.0.0.1:29003/graph";

let svg = d3.select("#graph-container")
        .append("svg")
        .attr("width", "1278px")
        .attr("height", "800px")
        .call(d3.zoom().on("zoom", function () {
            svg.attr("transform", d3.event.transform)
        }))
        .append("g"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

let graph = {};
let showTooltip = true;
let reachabilityMode = true;

function getReachability() {
    // remove all elements to redraw the graph on refresh
    svg.selectAll("*").remove();

    // get the new data
    jquery.ajax({
        type: "GET",
        url: host,
        success: function (data) {
            data = JSON.parse(data.replace(/\'/g, "\""));
            // console.log(data.hosts);
            // console.log(data.links);
            document.getElementById("devices").innerHTML = "Devices: " + (data.hosts.length - 1);
            document.getElementById("detectedLinks").innerHTML = "Active Links: " + data.links.length;
            let graph = {};
            graph.nodes = data.hosts;
            graph.links = data.links;
            let total = 0;

            // let defs = svg.append("svg:defs");
            //
            // defs.append("svg:pattern")
            //     .attr("width", 1)
            //     .attr("height", 1)
            //     .attr("id", "server");

            let simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(function (d) {
                    return d.ip;
                }).distance(150))
                .force("charge", d3.forceManyBody().strength(-5))
                .force("center", d3.forceCenter(650, 400))
                .force("collide", d3.forceCollide(100));

            let link = svg.selectAll(".link")
                .data(graph.links, function (d) {
                    return d.ip;
                })
                .enter().append("line").attr("class", "link");

            let node = svg.selectAll(".node")
                .data(graph.nodes, function (d) {
                    return d.ip;
                })
                .enter().append("g").attr("class", "node")

                .append("svg:image")
                .attr("xlink:href", function(d) {
                    // console.log(d);
                    if(d.ip !== "255.255.255.255") {
                        return "img/server.png";
                    } else {
                        return "img/internet.png"
                    }
                })
                .attr("width", 100)
                .attr("height", 100)
                .attr("x", -30)
                .attr("y", -30)

                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            let tip = d3.tip()
                .attr('class', 'd3-tip')
                .offset([-10, 0])
                .html(function (d) {
                    // console.log(d);
                    if (typeof d.running.Host === 'object') {
                        var result = "";
                        total += d.running.Host.RunningServices.length;
                        for (var i = 0; i < d.running.Host.RunningServices.length; i++) {

                            // Usual display attributes
                            if (d.running.Host.RunningServices[i].Port.portid != "attributeMissing") {
                                result += "<br><strong style='color:red'> Port : </strong><span>" + d.running.Host.RunningServices[i].Port.portid;
                            }
                            if (d.running.Host.RunningServices[i].Port.protocol != "attributeMissing") {
                                result += "&nbsp;<span>&#124;</span><strong style='color:red'> Protocol : </strong><span>" + d.running.Host.RunningServices[i].Port.protocol;
                            }
                            if (d.running.Host.RunningServices[i].Service.name != "attributeMissing") {
                                result += "<br><strong style='color:red'> Service : </strong><span>" + d.running.Host.RunningServices[i].Service.name;
                            }
                            if (d.running.Host.RunningServices[i].Service.product != "attributeMissing") {
                                result += "&nbsp;<span>&#124;</span><strong style='color:red'> Product : </strong><span>" + d.running.Host.RunningServices[i].Service.product;
                            }
                            if (d.running.Host.RunningServices[i].Service.version != "attributeMissing") {
                                result += "&nbsp;<span>&#124;</span><strong style='color:red'> Version : </strong><span>" + d.running.Host.RunningServices[i].Service.version;
                            }
                            if (d.running.Host.RunningServices[i].Service.reason != "attributeMissing") {
                                result += "<br><strong style='color:red'> Details : </strong><span>" + d.running.Host.RunningServices[i].Service.reason;
                            }
                            result += "<hr>";
                        }
                        return "<strong style='color:red'>Host : </strong><span>" + d.ip + "</span><hr><strong style='color:red'>Operating System : </strong>" + d.running.Host.os + result;
                    } else {
                        return "<strong style='color:red'>Host : </strong><span>" + d.ip + "</span><hr><strong style='color:red'>Operating System : </strong>unavailable";
                    }
                });

            svg.call(tip);

            node.append("circle")
                .attr("r", 60)
                .style("fill", "url(#server)");

            node.on("mouseover", function (d) {
                if (showTooltip) {
                    tip.show(d, this);
                }
            }).on("mouseout", function (d) {
                tip.hide();
            });

            node.append("title")
                .text(function (d) {
                    return d.id;
                });

            simulation.nodes(graph.nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(graph.links);

            // function initializeDistance() {
            //   if (!nodes) return;
            //   for (var i = 0, n = links.length; i < n; ++i) {
            //     distances[i] = +distance(links[i], i, links);
            //   }
            // }

            function ticked() {
                link
                    .attr("x1", function (d) {
                        return d.source.x;
                    })
                    .attr("y1", function (d) {
                        return d.source.y;
                    })
                    .attr("x2", function (d) {
                        return d.target.x;
                    })
                    .attr("y2", function (d) {
                        return d.target.y;
                    });

                node
                    .attr("transform", function (d) {
                        return "translate(" + d.x + ", " + d.y + ")";
                    });
            }

            function dragstarted(d) {
                if (!d3.event.active) {
                    simulation.alphaTarget(0.3).restart();
                }
            }

            function dragged(d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            }

            function dragended(d) {
                if (!d3.event.active) {
                    simulation.alphaTarget(0);
                }
                d.fx = null;
                d.fy = null;
            }
        }
    })
}

function getAttackGraph() {
    // remove all elements to redraw the graph on refresh
    svg.selectAll("*").remove();

    // get the new data
    var colors = d3.scaleOrdinal(d3.schemeCategory10);

    svg.append('defs').append('marker')
        .attrs({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':13,
            'refY':0,
            'orient':'auto',
            'markerWidth':5,
            'markerHeight':5,
            'xoverflow':'visible'})
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke','none');

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(100).strength(1))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    d3.json("js/graph.json", function (error, graph) {
        if (error) throw error;
        update(graph.links, graph.nodes);
    })

    function update(links, nodes) {
        link = svg.selectAll(".link")
            .data(links)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr('marker-end','url(#arrowhead)')

        link.append("title")
            .text(function (d) {return "NO TYPE (title)";});

        edgepaths = svg.selectAll(".edgepath")
            .data(links)
            .enter()
            .append('path')
            .attrs({
                'class': 'edgepath',
                'fill-opacity': 0,
                'stroke-opacity': 0,
                'id': function (d, i) {return 'edgepath' + i}
            })
            .style("pointer-events", "none");

        edgelabels = svg.selectAll(".edgelabel")
            .data(links)
            .enter()
            .append('text')
            .style("pointer-events", "none")
            .attrs({
                'class': 'edgelabel',
                'id': function (d, i) {return 'edgelabel' + i},
                'font-size': 10,
                'fill': '#aaa'
            });

        edgelabels.append('textPath')
            .attr('xlink:href', function (d, i) {return '#edgepath' + i})
            .style("text-anchor", "middle")
            .style("pointer-events", "none")
            .attr("startOffset", "50%")
            .text(function (d) {return "NO TYPE"});

        node = svg.selectAll(".node")
            .data(nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                //.on("end", dragended)
            );

        node.append("circle")
            .attr("r", 5)
            .style("fill", function (d, i) {return colors(i);})

        node.append("title")
            .text(function (d) {return d.id;});

        node.append("text")
            .attr("dy", -3)
            .text(function (d) {return d.fact+":"+d.type+":"+d.metric;});

        simulation
            .nodes(nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(links);
    }

    function ticked() {
        link
            .attr("x1", function (d) {return d.source.x;})
            .attr("y1", function (d) {return d.source.y;})
            .attr("x2", function (d) {return d.target.x;})
            .attr("y2", function (d) {return d.target.y;});

        node
            .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});

        edgepaths.attr('d', function (d) {
            return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
        });

        edgelabels.attr('transform', function (d) {
            if (d.target.x < d.source.x) {
                var bbox = this.getBBox();

                rx = bbox.x + bbox.width / 2;
                ry = bbox.y + bbox.height / 2;
                return 'rotate(180 ' + rx + ' ' + ry + ')';
            }
            else {
                return 'rotate(0)';
            }
        });
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

}

function getGraphInfo() {
    if(reachabilityMode) {
        getReachability();
    } else {
        getAttackGraph();
    }
}

getGraphInfo();
