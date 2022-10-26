function checkMouseOverSquare(square) {
  if (
    mouseX < square.x + square.size &&
    mouseX > square.x &&
    mouseY > square.y &&
    mouseY < square.y + square.size
  ) {
    return true;
  } else {
    return false;
  }
}

function checkMouseInsideScreenPadding() {
  return checkMouseOverSquare({
    x: screenPadding,
    y: screenPadding,
    size: width - screenPadding * 2,
  });
}

function checkMouseOverNodePadding(node) {
  if (
    mouseX <
      node.xpos - (nodeSize / 2 + mousePadding / 2) + nodeSize + mousePadding &&
    mouseX > node.xpos - (nodeSize / 2 + mousePadding / 2) &&
    mouseY > node.ypos - (nodeSize / 2 + mousePadding / 2) &&
    mouseY <
      node.ypos - (nodeSize / 2 + mousePadding / 2) + nodeSize + mousePadding
  ) {
    return true;
  } else {
    return false;
  }
}
