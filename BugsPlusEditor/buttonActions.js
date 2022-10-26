function toggleDeleteNodeMode() {
  currentMode = "DELETE_NODE";
}
function toggleMoveNodeMode() {
  currentMode = "MOVE_NODE";
}
function toggleDeleteLinkMode() {
  currentMode = "DELETE_LINK";
}
function toggleCreateNodeMode() {
  currentMode = "CREATE_NODE";
}
function toggleCreateLinkMode() {
  currentMode = "CREATE_LINK";
}
async function execute(board) {
  const xValueInput = Number(xValue);
  const yValueInput = Number(yValue);

  if (xValueInput && yValueInput) {
    memory.set("0mainDataInUp", xValue);
    memory.set("0mainDataInDown", yValue);

    fetch("http://127.0.0.1:8000/board", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        bugs: board.nodeDataArray,
        edges: board.linkDataArray,
        xValue: Number(xValue),
        yValue: Number(yValue),
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        memory.set("0mainDataOut", data);
      });
  } else {
    alert("Please enter a valid number");
  }
}

function getXValue(node) {
  xValue = document.getElementById("xValue").value;
}

function getYValue(node) {
  yValue = document.getElementById("yValue").value;
}
