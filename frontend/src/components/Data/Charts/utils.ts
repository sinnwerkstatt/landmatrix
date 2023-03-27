import { get } from "svelte/store"
import type { Selection, BaseType } from "d3"

import { filters } from "$lib/filters"
import { countries, regions } from "$lib/stores"

export type FileType = "svg" | "png" | "webp" | "json" | "csv"
export type DownloadEvent = CustomEvent<FileType>

export function fileName(title: string, suffix = ""): string {
  const $filters = get(filters)
  let prefix = "Global - "
  if ($filters.country_id)
    prefix = get(countries).find(c => c.id === $filters.country_id)?.name + " - "
  if ($filters.region_id)
    prefix = get(regions).find(r => r.id === $filters.region_id)?.name + " - "
  return prefix + title + suffix
}

export function a_download(data: string, name: string): void {
  const a = document.createElement("a")
  a.href = data
  a.download = name
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

export const downloadCSV = (csvString: string, title: string): void =>
  a_download(
    "data:text/csv;charset=utf-8," + encodeURIComponent(csvString),
    fileName(title, ".csv"),
  )

export const downloadJSON = (jsonString: string, title: string): void =>
  a_download(
    "data:application/json;charset=utf-8," + encodeURIComponent(jsonString),
    fileName(title, ".json"),
  )

export const downloadCanvas = (
  canvas: HTMLCanvasElement,
  fileType: "png" | "webp",
  title: string,
): void =>
  a_download(canvas.toDataURL(`image/${fileType}`), fileName(title, `.${fileType}`))

export const downloadSVG = (
  svg: SVGElement | null,
  fileType: "svg" | "png" | "webp",
  title: string,
): void => {
  if (!svg) return
  const name = fileName(title, `.${fileType}`)

  const serialized = new XMLSerializer().serializeToString(svg)
  const source = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + serialized
  const svgString = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source)

  if (fileType === "svg") {
    a_download(svgString, name)
  } else {
    const canvas = document.createElement("canvas")
    const context = canvas.getContext("2d")
    if (!context) return

    canvas.width = 800
    canvas.height = 400
    context.clearRect(0, 0, canvas.width, canvas.height)

    const image = new Image()
    image.onload = function () {
      context.drawImage(image, 0, 0, canvas.width, canvas.height)
      downloadCanvas(canvas, fileType, title)
    }
    image.src = svgString
  }
}

export function addMarkers(
  svg: Selection<BaseType, unknown, HTMLElement, unknown>,
  size = 10,
): void {
  const defs = svg.append("defs")
  const marker_factory = (name: string) =>
    defs
      .append("marker")
      .attr("id", name)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 0)
      .attr("refY", 0)
      .attr("markerWidth", size)
      .attr("markerHeight", size)
      .attr("orient", "auto-start-reverse")
      .attr("markerUnits", "userSpaceOnUse")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
  marker_factory("incoming-marker")
  marker_factory("outgoing-marker")
}
