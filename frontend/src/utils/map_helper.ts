import { primary_color } from "$utils/colors";
import type { Marker } from "leaflet";

export function styleCircle(
  circle: Marker,
  size: number,
  innerHTML: string,
  dealsCount = true,
  maxFactor = 40
): void {
  const circle_elem = circle.getElement();
  if (!circle_elem) return;

  const innertextnode = document.createElement("span");
  innertextnode.className = "landmatrix-custom-circle-text";

  innertextnode.innerHTML = innerHTML;
  circle_elem.append(innertextnode);

  const hoverlabel = document.createElement("span");
  hoverlabel.className = "landmatrix-custom-circle-hover-text";
  circle_elem.append(hoverlabel);

  let factor;
  if (dealsCount) {
    hoverlabel.innerHTML = `<b>${size.toLocaleString()}</b> locations`;
    factor = Math.max(Math.log(size) * 17, maxFactor);
  } else {
    hoverlabel.innerHTML = `${size.toLocaleString()} hectares`;
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
