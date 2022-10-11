let currentAvailableId = 7;
let currentMode = "CREATE_NODE";
let selectedNode = null;
let selectedPort = null;
let moving = false;
let xValue = 0;
let yValue = 0;

function setup() {
  createCanvas(800, 800);
  mainPortsOffsets.set("mainControlIn", {
    xOff: width * 0.5 - mainPortSize * 0.5,
    yOff: screenPadding - mainPortSize * 0.5,
  });
  mainPortsOffsets.set("mainControlOutL", {
    xOff: width * 0.3 + mainPortSize * 0.5,
    yOff: height - screenPadding * 1.5,
  });
  mainPortsOffsets.set("mainControlOutR", {
    xOff: width - width * 0.3 - mainPortSize * 0.5,
    yOff: height - screenPadding * 1.5,
  });
  mainPortsOffsets.set("mainDataOut", {
    xOff: screenPadding - mainPortSize * 0.5,
    yOff: height * 0.5 - mainPortSize * 0.5,
  });
  mainPortsOffsets.set("mainDataInUp", {
    xOff: width - screenPadding * 1.5,
    yOff: height * 0.3 - mainPortSize * 0.6,
  });
  mainPortsOffsets.set("mainDataInDown", {
    xOff: width - screenPadding * 1.5,
    yOff: height - height * 0.3,
  });

  nodePortOffsets.set("controlIn", { xOff: 25, yOff: -15 });
  nodePortOffsets.set("controlOutL", { xOff: 10, yOff: 70 });
  nodePortOffsets.set("controlOutR", { xOff: 40, yOff: 70 });
  nodePortOffsets.set("dataOut", { xOff: -15, yOff: 25 });
  nodePortOffsets.set("dataInUp", { xOff: 65, yOff: 10 });
  nodePortOffsets.set("dataInDown", { xOff: 65, yOff: 45 });
  //evalState(memory, state, 6, 1);

  document.getElementById("executer").addEventListener("click", () => {
    execute(state);
  });

  // );
}

function draw() {
  background(backgroundColor);
  drawMainNode();

  state.nodeDataArray.forEach(drawNode);
  state.linkDataArray.forEach(drawConnection);
  if (moving && selectedNode) {
    let nodeToMove = state.nodeDataArray.find((e) => e.id === selectedNode.id);
    if (
      mouseX < 800 - (screenPadding + nodeSize) &&
      mouseX > 0 + screenPadding &&
      mouseY < 800 - (screenPadding + nodeSize) &&
      mouseY > 0 + screenPadding
    ) {
      nodeToMove.xpos = mouseX;
      nodeToMove.ypos = mouseY;
    }
  }
}

function mousePressed(event) {
  if (currentMode === "MOVE_NODE") {
    selectAndMoveNode();
  }
  if (currentMode === "DELETE_NODE") {
    selectAndDeleteNode();
  }
  if (currentMode === "CREATE_NODE") {
    addNodeAtMouse();
  }
  if (currentMode === "CREATE_LINK") {
    selectAndCreateLink();
  }
  if (currentMode === "DELETE_LINK") {
    selectAndDeleteLink();
  }
}
