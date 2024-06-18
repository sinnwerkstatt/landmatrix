import type { Marker } from "leaflet?client"
import { writable } from "svelte/store"

const PRIMARY_COLOR = "#FC941FFF"

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
