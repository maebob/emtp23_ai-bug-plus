let state = {
  nodeDataArray: [],
  linkDataArray: [],
};

let memory = new Map();

const evalState = (memory, state, mainDataInUp, mainDataInDown) => {
  //declare memory

  //allocate memory for all ports of the child nodes
  for (const node of state.nodeDataArray) {
    for (const port of nodePortOffsets.keys()) {
      memory.set(node.id + port, null);
    }
  }

  //allocate memory for all ports of the mainNode
  memory.set("0mainDataInDown", mainDataInDown);
  memory.set("0mainDataInUp", mainDataInUp);
  memory.set("0mainControlIn", 1);
  memory.set("0mainDataOut", null);
  memory.set("0mainControlOutR", null);
  memory.set("0mainControlOutL", null);

  let currentNode = 1;
  while (currentNode !== 0) {
    let currentNodeValue = evaluateNode(memory, currentNode);
    let nextControlPort =
      currentNodeValue === 0 ? "controlOutR" : "controlOutL";
    let otherPort;
    if (nextControlPort === "controlOutL") {
      otherPort = "controlOutR";
    } else if (nextControlPort === "controlOutR") {
      otherPort = "controlOutL";
    }
    let nextNode = getNextNode(currentNode, nextControlPort);
    memory.set(currentNode + nextControlPort, 1);
    memory.set(currentNode + otherPort, 0);
    memory.set(currentNode + "controlIn", 1);
    memory.set(currentNode + "dataOut", currentNodeValue);
    currentNode = nextNode;
  }
  memory.set("0mainDataOut", getValueAtPort(memory, 3, "dataOut"));
  console.log(memory);
};

function evaluateNode(memory, node) {
  const connections = getInboundNodeConnections(node);
  const upConn = connections.find(
    (connection) => connection.toPort === "dataInUp"
  );
  const downConn = connections.find(
    (connection) => connection.toPort === "dataInDown"
  );
  if (downConn) {
    memory.set(
      node + "dataInDown",
      getValueAtPort(memory, downConn.fromNode, downConn.fromPort)
    );
  }
  if (upConn) {
    memory.set(
      node + "dataInUp",
      getValueAtPort(memory, upConn.fromNode, upConn.fromPort)
    );
  }
  //console.log(node, upConn, downConn);
  if (
    getValueAtPort(memory, node, "dataInDown") === null &&
    getValueAtPort(memory, node, "dataInUp") === 0
  ) {
    return 1;
  } else if (
    getValueAtPort(memory, node, "dataInUp") === null &&
    getValueAtPort(memory, node, "dataInDown") === 0
  ) {
    return -1;
  } else if (
    getValueAtPort(memory, node, "dataInDown") === null &&
    getValueAtPort(memory, node, "dataInUp") === null
  ) {
    return 0;
  } else if (
    getValueAtPort(memory, node, "dataInDown") !== null &&
    getValueAtPort(memory, node, "dataInUp") !== null
  ) {
    return (
      getValueAtPort(memory, node, "dataInUp") +
      getValueAtPort(memory, node, "dataInDown")
    );
  }
}

function getNextNode(node, port) {
  for (const connection of state.linkDataArray) {
    if (connection.fromNode === node && connection.fromPort === port) {
      return connection.toNode;
    }
  }
}

function getInboundNodeConnections(node) {
  return state.linkDataArray.filter((connection) => {
    return connection.toNode === node;
  });
}

function getValueAtPort(memory, nodeId, port) {
  return memory.get(nodeId + port);
}

// function evaluateNode(id) {
//   const connections = getNodeConnections(id);
//   dataUpConnection = connections.find(
//     (e) => e.fromPort === "dataInUp" || e.toPort === "dataInUp"
//   );
//   dataDownConnection = connections.find(
//     (e) => e.fromPort === "dataInDown" || e.toPort === "dataInDown"
//   );
//   if (!dataUpConnection && !dataDownConnection) {
//     return 0;
//   } else if (!dataDownConnection) {
//     return 1;
//   } else if (!dataUpConnection) {
//     return -1;
//   } else if (dataUpConnection && dataDownConnection) {
//     return evaluatePort(dataUpConnection) + evaluatePort(dataDownConnection);
//   }

//   return null;
// }
