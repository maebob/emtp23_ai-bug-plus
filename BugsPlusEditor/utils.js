function getNodeAtMouse() {
  for (const node of state.nodeDataArray) {
    if (checkMouseOverSquare({ x: node.xpos, y: node.ypos, size: 80 })) {
      return node;
    }
  }
  return null;
}

function getPortAtMouse() {
  for (const [key, value] of mainPortsOffsets) {
    if (
      checkMouseOverSquare({ x: value.xOff, y: value.yOff, size: mainPortSize })
    ) {
      return [{ id: 0 }, key];
    }
  }
  for (const node of state.nodeDataArray) {
    for (const [key, value] of nodePortOffsets) {
      let xpos = node.xpos + value.xOff;
      let ypos = node.ypos + value.yOff;
      if (checkMouseOverSquare({ x: xpos, y: ypos, size: 20 })) {
        return [node, key];
      }
    }
  }
  return [null, null];
}
function checkValidPositionAtMouse() {
  if (!checkMouseInsideScreenPadding()) return false;
  for (const n of state.nodeDataArray) {
    if (checkMouseOverNodePadding(n)) return false;
  }
  return true;
}
function checkValidPorts(from, to) {
  if (from === "mainDataInUp" && to === "dataInUp") return true;
  if (from === "mainDataInUp" && to === "dataInDown") return true;
  if (from === "mainControlIn" && to === "controlIn") return true;
  if (from === "dataOut" && to === "dataInDown") return true;
  if (from === "dataOut" && to === "dataInUp") return true;
  if (from === "controlOutL" && to === "controlIn") return true;
  if (from === "controlOutR" && to === "controlIn") return true;

  if (
    from.toLowerCase().includes("data") &&
    from.toLowerCase().includes("out") &&
    to.toLowerCase().includes("data") &&
    to.toLowerCase().includes("in")
  )
    return true;
  if (
    from.toLowerCase().includes("control") &&
    from.toLowerCase().includes("out") &&
    to.toLowerCase().includes("control") &&
    to.toLowerCase().includes("in")
  )
    return true;
  return false;
}
