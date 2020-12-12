import { primary_color } from "/colors";

export function styleCircle(
  circle,
  size,
  innerHTML,
  dealsCount = true,
  maxFactor = 40
) {
  let circle_elem = circle.getElement();

  let innertextnode = document.createElement("span");
  innertextnode.className = "landmatrix-custom-circle-text";

  innertextnode.innerHTML = innerHTML;
  circle_elem.append(innertextnode);

  let hoverlabel = document.createElement("span");
  hoverlabel.className = "landmatrix-custom-circle-hover-text";
  circle_elem.append(hoverlabel);

  let factor;
  if (dealsCount) {
    hoverlabel.innerHTML = `<b>${size}</b> locations`;
    factor = Math.max(Math.log(size) * 17, maxFactor);
  } else {
    hoverlabel.innerHTML = `${size} hectares`;
    factor = Math.max(Math.log(size) * 6, maxFactor);
  }

  Object.assign(circle_elem.style, {
    height: `${factor}px`,
    width: `${factor}px`,
    left: `-${factor / 2}px`,
    top: `-${factor / 2}px`,
    background: primary_color,
  });
}
