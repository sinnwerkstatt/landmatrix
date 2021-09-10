export function a_download(data, name) {
  const a = document.createElement("a");
  a.href = data;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

export function chart_download(svg, filetype = "image/svg", name = "Chart.svg") {
  let serialized = new XMLSerializer().serializeToString(svg);
  let source = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + serialized;
  let data = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);

  if (filetype === "image/svg") {
    a_download(data, name);
  } else {
    let canvas = document.createElement("canvas");
    let context = canvas.getContext("2d");
    canvas.width = 800;
    canvas.height = 800;
    context.clearRect(0, 0, canvas.width, canvas.height);

    let image = new Image();
    image.onload = function () {
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      let canvasUrl = canvas.toDataURL(filetype);
      a_download(canvasUrl, name);
    };
    image.src = data;
  }
}
