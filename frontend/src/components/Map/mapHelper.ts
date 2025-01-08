import { Feature, Overlay } from "ol"
import type { Coordinate } from "ol/coordinate"
import { pointerMove } from "ol/events/condition"
import { Point } from "ol/geom"
import { Select } from "ol/interaction"
import { Circle, Fill, Icon, Stroke, Style, Text } from "ol/style"
import { mount } from "svelte"
import { writable } from "svelte/store"

import MapMarkerPopup from "$components/Map/MapMarkerPopup.svelte"

import marker2x from "./marker-icon-2x.png"

// const markerSVG = (color = "#fc941d") => `<svg
//   xmlns="http://www.w3.org/2000/svg"
//   viewBox="0 0 24 24"
//   fill="${encodeURIComponent(color)}"
//   width="32"
//   height="32"
//   stroke="black"
//   stroke-width="0.5"
// >
//   <path
//     fill-rule="evenodd"
//     d="m11.54 22.351.07.04.028.016a.76.76 0 0 0 .723 0l.028-.015.071-.041a16.975 16.975 0 0 0 1.144-.742 19.58 19.58 0 0 0 2.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 0 0-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 0 0 2.682 2.282 16.975 16.975 0 0 0 1.145.742ZM12 13.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"
//     clip-rule="evenodd"
//   />
// </svg>
// `

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

export const displayDealsCount = writable(true)
const wrapText = (text: string, maxWidth: number) => {
  const words = text.split(" ")
  const lines = []
  let currentLine = words[0]

  for (let i = 1; i < words.length; i++) {
    const word = words[i]
    const width = word.length * 6 // Approximate width per character

    if (width + currentLine.length * 6 < maxWidth) {
      currentLine += " " + word
    } else {
      lines.push(currentLine)
      currentLine = word
    }
  }
  lines.push(currentLine)
  return lines.join("\n")
}
export const createStyledPoint = (
  coordinates: Coordinate,
  radius: number,
  defaultText: string,
  hoverText?: string,
) => {
  const feature = new Feature({ geometry: new Point(coordinates) })
  feature.setProperties({ hoverText: hoverText, radius })

  const defaultStyle = new Style({
    image: new Circle({
      radius: radius,
      fill: new Fill({ color: "hsl(32, 97%, 70%)" }),
      stroke: new Stroke({ color: "hsl(32, 97%, 55%)", width: 2 }),
    }),
    text: new Text({
      text: wrapText(defaultText, radius * 1.5),
      fill: new Fill({ color: "#000000" }),
      stroke: new Stroke({ color: "#ffffff", width: 3 }),
      scale: 1.4,
      textAlign: "center",
      textBaseline: "middle",
    }),
  })

  feature.setStyle(defaultStyle)

  return feature
}
export const regionHoverInteraction = new Select({
  condition: pointerMove,
  style: ft => {
    const props = ft.getProperties()
    if (!props || !props.hoverText || !props.radius) return

    return new Style({
      image: new Circle({
        radius: props.radius,
        fill: new Fill({ color: "hsl(32, 97%, 60%)" }),
        stroke: new Stroke({ color: "hsl(32, 97%, 55%)", width: 2 }),
      }),
      text: new Text({
        text: wrapText(props.hoverText, props.radius * 1.5),
        fill: new Fill({ color: "#000000" }),
        stroke: new Stroke({ color: "#ffffff", width: 3 }),
        scale: 1.4,
        textAlign: "center",
        textBaseline: "middle",
      }),
    })
  },
})

export async function createMarkerTooltipOverlay(feature: Feature<Point>) {
  const containerDiv = document.createElement("div")
  const props = feature.getProperties()
  mount(MapMarkerPopup, {
    target: containerDiv,
    props: { deal: props.deal, location: props.location },
  })
  return new Overlay({
    element: containerDiv,
    position: feature.getGeometry()!.getCoordinates(),
    positioning: "bottom-center",
    offset: [-30, -30, -30, -30],
    autoPan: { animation: { duration: 300 } },
  })
}
