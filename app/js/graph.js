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
            console.log(data.hosts);
            let totalVuls = 0, vuls = [];
            data.hosts.forEach(function(item, index) {
                let services = [];
                if (item.running.Host !== undefined) {
                  services = item.running.Host.RunningServices;
                }
                console.log(services);
                for (var i = 0; i < services.length; i++) {
                    if(services[i].Vulnerability instanceof Array) {
                        totalVuls += services[i].Vulnerability.length;
                        services[i].Vulnerability.forEach(function(item, index) {
                           vuls.push(item);
                        });
                    }
                }
            });
            document.getElementById("devices").innerHTML = "Devices: " + (data.hosts.length - 1);
            document.getElementById("detectedLinks").innerHTML = "Active Links: " + data.links.length;
            document.getElementById("vulnerabilities").innerHTML = "Vulnerabilities (" + totalVuls + ")";
            // console.log(vuls);
            //vuls.push({id: "CVE-2124", impact: {baseMetricV2: {}}, description: "Double free vulnerability in inspect-fs.c in Libgu… denial of service (crash) via empty guest files."});

            let vulHtml = "<br>";
            vuls.forEach(function(item, index) {
              //  console.log(JSON.stringify(item))
                let tid = "det-" + (index + 1);
                vulHtml += "<li class=\"list-group-item\">\
                    \<div class=\"row toggle\" id=\"dropdown-" + tid + "\" data-toggle=\"" + tid + "\">\
                    \<div class=\"col-lg-10\">" + item.id + "</div>\
                    \<div class=\"col-lg-2\"><i class=\"fa fa-chevron-down pull-right\"></i></div>\
                    \</div>\
                    \<div id=\"" + tid + "\" class=\"row collapse\"><hr><ul><li>" +
                    "Score: " + item.impact.baseMetricV2.impactScore + "</li><li>" +
                    "CVSS v2: " + item.impact.baseMetricV2.exploitabilityScore + "</li><li>" +
                    "Description: " + item.description + "</li></ul></div>\
                    \</li>";
            });
            document.getElementById("detail-2").innerHTML = vulHtml;

            let graph = {};
            graph.nodes = data.hosts;
            graph.links = data.links;

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
                    let services = [];
                    if (d.running.Host !== undefined) {
                      services = d.running.Host.RunningServices;
                    }
                    if (typeof d.running.Host === 'object' && d.ip != "255.255.255.255") {
                        var result = "";
                        if(services.length > 0) {
                            result += "<br><strong style='color:#7479d0'>Running Services:</strong><br><ul>";
                            for (var i = 0; i < services.length; i++) {
                                result += "<li>";
                                // Usual display attributes
                                if (services[i].Port.portid != "attributeMissing") {
                                    result += "<strong style='color:#7479d0'> Port : </strong><span>" + services[i].Port.portid;
                                }
                                if (services[i].Port.protocol != "attributeMissing") {
                                    result += "&nbsp;<span>&#124;</span><strong style='color:#7479d0'> Protocol : </strong><span>" + services[i].Port.protocol;
                                }
                                if (services[i].Service.name != "attributeMissing") {
                                    result += "<br><strong style='color:#7479d0'> Service : </strong><span>" + services[i].Service.name;
                                }
                                if (services[i].Service.product != "attributeMissing") {
                                    result += "&nbsp;<span>&#124;</span><strong style='color:#7479d0'> Product : </strong><span>" + services[i].Service.product;
                                }
                                if (services[i].Service.version != "attributeMissing") {
                                    result += "&nbsp;<span>&#124;</span><strong style='color:#7479d0'> Version : </strong><span>" + services[i].Service.version;
                                }
                                if (services[i].Service.reason != "attributeMissing") {
                                    result += "<br><strong style='color:#7479d0'> Details : </strong><span>" + services[i].Service.reason;
                                }
                                result += "</li>";
                            }
                            result += "</ul>";
                        }
                        return "<strong style='color:#7479d0'>Host : </strong><span>" + d.ip + "</span>&nbsp;<span>&#124;&nbsp;</span><strong style='color:#7479d0'>Operating System : </strong>" + d.running.Host.os + result;
                    } else {
                        if(d.ip != "255.255.255.255") {
                            return "<strong style='color:#7479d0'>Host : </strong><span>" + d.ip + "</span>&nbsp;<span>&#124;&nbsp;</span><strong style='color:#7479d0'>Operating System : </strong>unavailable";
                        } else {
                            return "<strong style='color:#7479d0'>Internet</strong>&nbsp;<span>&#124;&nbsp;</span><strong>Attacker's Location</strong>";
                        }
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
            .attr("class", "link-attack-graph")
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
            )
            .append("svg:image")
            .attr("xlink:href", function(d) {
                // console.log(d);
                // if(d.fact === "attackerLocated(internet)") {
                //     return "img/blackhat.png";
                // }
                if(d.fact === "attackerLocated(internet)") {
                    return "img/internet.png"
                } else if(d.fact.match(/RULE/g) === null) {
                    return "img/server.png"
                } else {
                   return "img/circle.svg"
                }
          })
            .attr("width", 40)
            .attr("height", 40)
            .attr("x", -10)
            .attr("y", -10);

        let tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function (d) {
                // console.log(d);
                if (d.type != "AND") {
                    var result = "<br><strong style='color:#7479d0'> Fact : </strong><span>" + d.fact + "<hr>";
                    return result;
                }
            });

        svg.call(tip);

        node.on("mouseover", function (d) {
            if (showTooltip && d.type != "AND") {
                tip.show(d, this);
            }
        }).on("mouseout", function (d) {
            tip.hide();
        });

        // node.append("circle")
        //     .attr("r", 5)
        //     .style("fill", function (d, i) {return colors(i);})

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
