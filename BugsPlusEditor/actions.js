function addNode(node) {
  if (!checkValidPositionAtMouse()) return;
  state.nodeDataArray.push(node);
  currentAvailableId++;
}

function deleteNode(id) {
  deleteAllNodeConnections(id);
  state.nodeDataArray = state.nodeDataArray.filter((e) => e.id !== id);
}

function deletePortConnection(fromNode, fromPort) {
  state.linkDataArray = state.linkDataArray.filter(
    (e) => !(e.fromNode === fromNode.id && fromPort === e.fromPort)
  );
}

function deleteAllNodeConnections(id) {
  state.linkDataArray = state.linkDataArray.filter(
    (e) => !(e.fromNode === id || e.toNode === id)
  );
}

function addNodeAtMouse() {
  addNode({
    id: currentAvailableId,
    xpos: mouseX,
    ypos: mouseY,
  });
}
function selectAndDeleteLink() {
  [selectedNode, selectedPort] = getPortAtMouse();
  if (selectedNode && selectedPort) {
    deletePortConnection(selectedNode, selectedPort);
  }
}

function selectAndDeleteNode() {
  let nodeToDelete = getNodeAtMouse();
  if (nodeToDelete) {
    deleteNode(nodeToDelete.id);
  }
}

function selectAndCreateLink() {
  let [node, port] = getPortAtMouse();
  if (node === null || selectedPort === null) {
    if (node && port) {
      selectedNode = node.id;
      selectedPort = port;
    }
  } else {
    let [secondNode, secondPort] = getPortAtMouse();

    if (secondNode && secondPort)
      if (!checkValidPorts(selectedPort, secondPort)) {
        selectedNode = null;
        selectedPort = null;
      } else {
        state.linkDataArray.push({
          fromNode: selectedNode,
          toNode: secondNode.id,
          fromPort: selectedPort,
          toPort: secondPort,
        });

        selectedNode = null;
        selectedPort = null;
      }
  }
}
function selectAndMoveNode() {
  if (!moving) {
    selectedNode = getNodeAtMouse();
    if (selectedNode) {
      moving = true;
    }
  } else {
    selectedNode = null;
    moving = false;
  }
}
