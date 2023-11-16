import type { Feature } from "geojson"
import * as R from "ramda"

import { addTempIds, setProperty, upsertProperties } from "./geojsonHelpers"

describe("geojsonHelpers", () => {
  test("upsertProperties", () => {
    expect(upsertProperties({}, FEATURE_WITHOUT_PROPS)).toHaveProperty("properties", {})

    expect(
      R.pipe(
        upsertProperties({ type: "area", description: "bad feature" }),
        upsertProperties({ type: "point", id: 12345 }),
      )(FEATURE_WITHOUT_PROPS),
    ).toHaveProperty("properties", {
      type: "point",
      description: "bad feature",
      id: 12345,
    })
  })

  test("setProperty", () => {
    expect(setProperty("area", undefined, FEATURE_WITHOUT_PROPS)).toHaveProperty(
      "properties",
      { area: undefined },
    )

    expect(
      R.pipe(
        setProperty("area", "production_area"),
        setProperty("area", "contract_area"),
        setProperty("id", 12345),
      )(FEATURE_WITHOUT_PROPS),
    ).toHaveProperty("properties", {
      area: "contract_area",
      id: 12345,
    })
  })

  test("addTempIds", () => {
    expect(addTempIds([])).toHaveUniqueIds()

    const one_feature = [FEATURE_WITHOUT_PROPS]
    expect(one_feature).not.toHaveProperty("0.id")
    expect(addTempIds(one_feature)).toHaveProperty("0.id")

    expect(one_feature).toHaveUniqueIds()
    expect(addTempIds(one_feature)).toHaveUniqueIds()

    const two_features = [FEATURE_WITHOUT_PROPS, FEATURE_WITHOUT_PROPS]
    expect(two_features).not.toHaveUniqueIds()
    expect(addTempIds(two_features)).toHaveUniqueIds()

    const thousand_features = R.times(R.always(FEATURE_WITHOUT_PROPS), 1000)
    expect(thousand_features).not.toHaveUniqueIds()
    expect(addTempIds(thousand_features)).toHaveUniqueIds()
  })
})

expect.extend({
  toHaveUniqueIds: (features: Feature[]) => {
    const getUniqueIds = R.pipe(R.map(R.prop("id")), R.uniq)
    return getUniqueIds(features).length === features.length
      ? {
          pass: true,
          message: () => `Expected ${features.length} features not to have unique ids.`,
        }
      : {
          pass: false,
          message: () => `Expected ${features.length} features to have unique ids.`,
        }
  },
})

const FEATURE_WITHOUT_PROPS: Feature = {
  type: "Feature",
  geometry: {
    type: "Point",
    coordinates: [6.455027, 3.384082],
  },
  properties: null,
}
