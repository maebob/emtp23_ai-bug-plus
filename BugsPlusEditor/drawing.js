function drawMainNode() {
  fill(mainNodeColor);
  square(screenPadding, screenPadding, width - screenPadding * 2, 20);
  for (const [key, value] of mainPortsOffsets) {
    let xpos = value.xOff;
    let ypos = value.yOff;
    if (checkMouseOverSquare({ x: xpos, y: ypos, size: mainPortSize })) {
      fill(mainNodeColor);
    } else if (0 === selectedNode && selectedPort === key) {
      fill(backgroundColor);
    } else {
      fill(portColor);
    }
    let val = getValueAtPort(memory, 0, key);
    if (val || val === 0) {
      push();
      textSize(32);
      fill(255, 0, 0);
      text(val, xpos, ypos);
      pop();
    }
    square(xpos, ypos, mainPortSize, 10);
  }
}

function drawConnection(connection) {
  let fromNode;
  let toNode;
  if (connection.fromNode === 0) {
    const { xOff, yOff } = mainPortsOffsets.get(connection.fromPort);
    const toNode = state.nodeDataArray.find((e) => e.id === connection.toNode);
    let v0 = createVector(xOff + mainPortSize * 0.5, yOff + mainPortSize * 0.5);
    let v1 = createVector(
      toNode.xpos +
        nodePortOffsets.get(connection.toPort).xOff +
        portSize * 0.5,
      toNode.ypos + nodePortOffsets.get(connection.toPort).yOff + portSize * 0.5
    );
    drawArrow(v0, v1, "black");

    return;
  }
  if (connection.toNode === 0) {
    const x = mainPortsOffsets.get(connection.toPort).xOff;
    const y = mainPortsOffsets.get(connection.toPort).yOff;
    const fromNode = state.nodeDataArray.find((e) => e.id === connection.fromNode);
    let v0 = createVector(x + mainPortSize * 0.5, y + mainPortSize * 0.5);
    let v1 = createVector(
      fromNode.xpos +
        nodePortOffsets.get(connection.fromPort).xOff +
        portSize * 0.5,
      fromNode.ypos +
        nodePortOffsets.get(connection.fromPort).yOff +
        portSize * 0.5
    );
    drawArrow(v1, v0, "black");
    return;
  }

  fromNode = state.nodeDataArray.find((e) => e.id === connection.fromNode);
  toNode = state.nodeDataArray.find((e) => e.id === connection.toNode);
  if (fromNode && toNode) {
    let v0 = createVector(
      fromNode.xpos +
        nodePortOffsets.get(connection.fromPort).xOff +
        portSize * 0.5,
      fromNode.ypos +
        nodePortOffsets.get(connection.fromPort).yOff +
        portSize * 0.5
    );
    let v1 = createVector(
      toNode.xpos +
        nodePortOffsets.get(connection.toPort).xOff +
        portSize * 0.5,
      toNode.ypos + nodePortOffsets.get(connection.toPort).yOff + portSize * 0.5
    );
    drawArrow(v0, v1, "black");
  }
}

function drawNodePorts(node) {
  for (const [key, value] of nodePortOffsets) {
    let xpos = node.xpos + value.xOff;
    let ypos = node.ypos + value.yOff;
    if (checkMouseOverSquare({ x: xpos, y: ypos, size: 20 })) {
      fill(mainNodeColor);
    } else if (node.id === selectedNode && selectedPort === key) {
      fill(backgroundColor);
    } else {
      fill(portColor);
    }
    square(xpos, ypos, 25, 10);
    let val = getValueAtPort(memory, node.id, key);
    if (val || val === 0) {
      textSize(32);
      fill(255, 0, 0);
      text(val, xpos, ypos);
    }
  }
}

function drawArrow(base, vec, myColor) {
  push();
  stroke(myColor);
  strokeWeight(3);
  fill(myColor);
  translate(base.x, base.y);

  line(0, 0, vec.x - base.x, vec.y - base.y);
  let vec2 = vec.sub(base);
  rotate(vec2.heading());
  let arrowSize = 7;
  translate(vec.mag() - arrowSize, 0);
  triangle(0, arrowSize / 2, 0, -arrowSize / 2, arrowSize, 0);
  pop();
}

function drawNode(node) {
  strokeWeight(2);
  fill(nodeColor);
  square(node.xpos, node.ypos, 80, 20);
  drawNodePorts(node);
}
