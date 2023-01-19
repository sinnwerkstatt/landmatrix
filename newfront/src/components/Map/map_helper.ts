import type { Marker } from "leaflet"
import { writable } from "svelte/store"

const primary_color = "#fc941f"

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
  const circle_elem = circle.getElement()
  if (!circle_elem) return

  const innertextnode = document.createElement("span")
  innertextnode.className = "inline group-hover:hidden"

  innertextnode.innerHTML = innerHTML
  circle_elem.append(innertextnode)

  const hoverlabel = document.createElement("span")
  hoverlabel.className = "hidden p-1 group-hover:inline"
  circle_elem.append(hoverlabel)

  let factor
  if (dealsCount) {
    hoverlabel.innerHTML = `<b>${size.toLocaleString("fr")}</b> locations`
    factor = Math.max(Math.log(size) * 17, maxFactor)
  } else {
    hoverlabel.innerHTML = `${size.toLocaleString("fr")} hectares`
    factor = Math.max(Math.log(size) * 6, maxFactor)
  }

  Object.assign(circle_elem.style, {
    height: `${factor}px`,
    width: `${factor}px`,
    left: `-${factor / 2}px`,
    top: `-${factor / 2}px`,
    background: primary_color,
  })
}
