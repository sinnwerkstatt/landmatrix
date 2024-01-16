import type { Feature } from "geojson"

import LocationLegend from "$components/Deal/LocationLegend.svelte"
import LocationTooltip from "$components/Deal/LocationTooltip.svelte"

export const createTooltip = (feature: Feature): HTMLElement => {
  const container = L.DomUtil.create("div")
  new LocationTooltip({
    props: { feature },
    target: container,
  })
  return container
}

export const createLegend = () => {
  const legend = new L.Control({ position: "bottomleft" })
  legend.onAdd = () => {
    const container = L.DomUtil.create("div")
    new LocationLegend({
      props: {},
      target: container,
    })
    return container
  }
  return legend
}
