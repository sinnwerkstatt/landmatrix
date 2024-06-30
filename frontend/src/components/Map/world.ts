import type { Feature, Geometry } from "geojson"
import { feature } from "topojson-client"
import type { GeometryCollection, Topology } from "topojson-specification"
import worldTopology from "world-atlas/countries-110m.json"

interface CountryProps {
  name: string
}

export interface CountryFeature extends Feature<Geometry, CountryProps> {
  id: number
}

const createWorld = (topology: Topology) =>
  feature(topology, topology.objects.countries as GeometryCollection<CountryProps>)

const createLowResWorld = () => createWorld(worldTopology as unknown as Topology)

// const createHighResWorld = async () => {
//   const topology = (await import(
//     "world-atlas/countries-10m.json"
//   )) as unknown as Topology
//   return createWorld(topology)
// }
//
// export const getCountryFeature = async (id: number) =>
//   (await createHighResWorld()).features.find(f => +(f.id as string) === id)

export const createCountryFeatureList = (): CountryFeature[] =>
  createLowResWorld().features.map(asCountryFeature)

export const createCountryFeatureMap = (): { [key: number]: CountryFeature } =>
  createCountryFeatureList().reduce(idMapReducer, {})

const asCountryFeature = (
  feature: Feature<Geometry, CountryProps>,
): CountryFeature => ({
  ...feature,
  id: +(feature.id as string),
})

/* eslint-disable-next-line @typescript-eslint/no-explicit-any */
type AnyKey = keyof any

const idMapReducer = <T extends { id: AnyKey }>(
  acc: { [id in AnyKey]: T },
  value: T,
) => ({
  ...acc,
  [value.id]: value,
})
