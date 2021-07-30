export function linebreaks(value) {
  let paras = value.split(/\n{2,}/);
  paras = paras.map((p) => `<p>${p.replace("\n", "<br>")}</p>`);
  return paras.join("\n");
}

export function thousandsep(value) {
  if (value === undefined) return;
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}
