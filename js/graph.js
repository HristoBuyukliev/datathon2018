megaData = {'nodes':[], "links":[]};

function linkKey(l) {
    return l.source+":"+l.target;
}

function addData(newData) {
    let newNodes = newData['nodes'];
    let newLinks = newData['links'];
    let existing_node_ids = new Set(megaData.nodes.map(x=>x.id))
    megaData.links = megaData.links.map(l=> {
        return {
            'source': l['source']['id'],
            'target': l['target']['id'],
            'left': l['left'],
            'right': l['right'],
            "value": 1
            }
    });
    let existing_links = new Set(megaData.links.map(linkKey));
    for (let node of newNodes) {
        if (existing_node_ids.has(node.id)) {
            console.log("found existing node", node.id)
            continue;
        }
        else {
            megaData['nodes'].push(node);
        }
    }
    for (let link of newLinks) {
        if (existing_links.has(linkKey(link) )) {
           console.log("found existing link", link.source,link.target)
            continue;
        } else {
            console.log("adding new link");
            megaData['links'].push(link);
        }

    }

}
function requestGraph(node_id = null) {
    if (node_id == null) {
        node_id = $('#node_id')[0].value;
    }
    $.getJSON( "http://localhost:5000", {node_id}, function( data ) {
        if (data['nodes']) {
            addData(data);
            showGraph(megaData, 24);
        }
    });
}

function showGraph(data, radius) {
  var svg = d3.select("#graph"),
    width = +svg.attr("width"),
    height = +svg.attr("height");
    svg.selectAll("*").remove();


  svg.append('svg:defs').append('svg:marker')
    .attr('id', 'end-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', radius/1.44)
    .attr('markerWidth', 5)
    .attr('markerHeight', 5)
    .attr('orient', 'auto')
  .append('svg:path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#000');

  svg.append('svg:defs').append('svg:marker')
      .attr('id', 'start-arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', -radius/2)
      .attr('markerWidth', 5)
      .attr('markerHeight', 5)
      .attr('orient', 'auto')
    .append('svg:path')
      .attr('d', 'M10,-5L0,0L10,5')
      .attr('fill', '#000');



  var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function(d) { return d.id; }))
      .force("charge", d3.forceManyBody())
      .force("collide", d3.forceCollide(4*radius))
      .force("center", d3.forceCenter(width / 2, height / 2));


  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(data.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return 5; })
      .style('marker-start', function(d) {
        return d.left ? 'url(#start-arrow)' : ''; })
      .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; });

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll(".node")
    .data(data.nodes)
    .enter().append("g")
      .attr("class", "node")
        .on('click', clicked)
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  node.append("image")
      .attr("xlink:href", function(d) { if (d.g5) { return "img/telenor-logo-bad.png"} else { return "img/telenor-logo.png"}})
      .attr("x", -radius)
      .attr("y", -radius)
      .attr("width", 2 * radius)
      .attr("height", 2* radius);
  node.append("text")
      .attr("dx", radius)
      .attr("dy", radius)
      .attr("fill", "#2a3990")
      .text(function(d) { return d.id.substring(0,8); });

  node.append("title")
      .text(function(d) { return d.id; });
  simulation
      .nodes(data.nodes)
      .on("tick", ticked);


  function clicked(node) {
    requestGraph(node.id);
  }
  simulation.force("link")
      .links(data.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  }
function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
}