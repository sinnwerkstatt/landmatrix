import type { Marker } from "leaflet"
import { Circle as CircleStyle, Fill, Icon, Style, Text } from "ol/style"
import { writable } from "svelte/store"

import marker2x from "./marker-icon-2x.png"

const PRIMARY_COLOR = "#FC941FFF"

export const olStyle2 = (radius: number, text?: string) => {
  const calcR = Math.min(Math.max(radius, 8), 30)
  return [
    new Style({
      image: new CircleStyle({
        radius: calcR,
        displacement: radius < 10 ? [1, -1] : [2, -2],
        fill: new Fill({
          color: "rgba(0, 0, 0, 0.4)",
        }),
      }),
    }),
    new Style({
      image: new CircleStyle({
        radius: calcR,
        fill: new Fill({ color: "hsla(32, 97%, 55%, 0.9)" }),
        // stroke: new Stroke({ color: "#3388ff", width: 1.25 }),
      }),
      text: text
        ? new Text({
            text: text,
            textAlign: "center",
            justify: "center",
            offsetY: 1,
            offsetX: 1,

            fill: new Fill({ color: "#000" }),
          })
        : undefined,
    }),
  ]
}

const markerSVG = (color = "#fc941d") => `<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="${encodeURIComponent(color)}"
  width="32"
  height="32"
  stroke="black"
  stroke-width="0.5"
>
  <path
    fill-rule="evenodd"
    d="m11.54 22.351.07.04.028.016a.76.76 0 0 0 .723 0l.028-.015.071-.041a16.975 16.975 0 0 0 1.144-.742 19.58 19.58 0 0 0 2.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 0 0-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 0 0 2.682 2.282 16.975 16.975 0 0 0 1.145.742ZM12 13.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"
    clip-rule="evenodd"
  />
</svg>
`
export const markerStyle = new Style({
  image: new Icon({
    opacity: 1,
    anchor: [0.5, 1],
    // anchorXUnits: "fraction",
    // anchorYUnits: "pixels",
    // src: "data:image/svg+xml;utf8," + markerSVG(),
    scale: 0.4,
    src: marker2x,
  }),
})
export const markerStyleSemi = new Style({
  image: new Icon({
    opacity: 0.4,
    anchor: [0.5, 1],
    scale: 0.4,
    src: marker2x,
    color: "gray",
  }),
})

export const LMCircleClass =
  "group opacity-90 text-sm rounded-full text-center !flex justify-center items-center drop-shadow-marker"

export const displayDealsCount = writable(true)

export function styleCircle(
  circle: Marker,
  size: number,
  innerHTML: string,
  dealsCount = true,
  maxFactor = 40,
): void {
  const circleElement = circle.getElement()
  if (!circleElement) return

  const innerTextNode = document.createElement("span")
  innerTextNode.className = "inline group-hover:hidden"

  innerTextNode.innerHTML = innerHTML
  circleElement.append(innerTextNode)

  const hoverLabel = document.createElement("span")
  hoverLabel.className = "hidden p-1 group-hover:inline"
  circleElement.append(hoverLabel)

  // TODO: Use svelte component
  let factor: number
  if (dealsCount) {
    hoverLabel.innerHTML = `<b>${size.toLocaleString("fr").replace(",", ".")}</b> locations`
    factor = Math.max(Math.log(size) * 17, maxFactor)
  } else {
    hoverLabel.innerHTML = `${size.toLocaleString("fr").replace(",", ".")} hectares`
    factor = Math.max(Math.log(size) * 6, maxFactor)
  }

  Object.assign(circleElement.style, {
    height: `${factor}px`,
    width: `${factor}px`,
    left: `-${factor / 2}px`,
    top: `-${factor / 2}px`,
    background: PRIMARY_COLOR,
  })
}
