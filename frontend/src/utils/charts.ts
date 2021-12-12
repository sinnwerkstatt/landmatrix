import store from "$store";

export function fileName(title: string, suffix = ""): string {
  const filters = store.state.filters;
  let prefix = "Global - ";
  if (filters.country_id)
    prefix =
      store.getters.getCountryOrRegion({
        type: "country",
        id: filters.country_id,
      }).name + " - ";
  if (filters.region_id)
    prefix =
      store.getters.getCountryOrRegion({
        type: "region",
        id: filters.region_id,
      }).name + " - ";
  return prefix + title + suffix;
}

export function a_download(data: string, name: string): void {
  const a = document.createElement("a");
  a.href = data;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

export function chart_download(
  svg: Element | null,
  filetype = "image/svg",
  name = "Chart.svg"
): void {
  if (!svg) return;
  const serialized = new XMLSerializer().serializeToString(svg);
  const source =
    '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + serialized;
  const data = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);

  if (filetype === "image/svg") {
    a_download(data, name);
  } else {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    if (!context) return;
    canvas.width = 800;
    canvas.height = 800;
    context.clearRect(0, 0, canvas.width, canvas.height);

    const image = new Image();
    image.onload = function () {
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      const canvasUrl = canvas.toDataURL(filetype);
      a_download(canvasUrl, name);
    };
    image.src = data;
  }
}
