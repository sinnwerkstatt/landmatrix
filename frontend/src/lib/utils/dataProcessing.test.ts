import {
  customIsNull,
  discardEmptySubmodels,
  isEmptySubmodel,
  sieveSubmodel,
  sum,
} from "$lib/utils/dataProcessing"

const OBJ_WITH_EMPTY_FIELDS = {
  undefinedField: undefined,
  nullField: null,
  emptyStringField: "",
  emptyArrayField: [],
  emptyObjectField: {},
}

const OBJ_WITH_NON_EMPTY_FIELDS = {
  stringField: "abc",
  numberField: 123,
  arrayField: ["abc", 123],
  objectField: { nested: {} },
}

test("sum", () => {
  expect(sum([], "value")).toEqual(0)
  expect(sum([{ value: 2 }], "value")).toEqual(2)
  // @ts-expect-error test invalid key
  expect(sum([{ value: 2 }], "invalidKey")).toEqual(NaN)
  expect(
    sum([{ value: 2 }, { value: -5 }, { value: 0 }, { value: 4 }], "value"),
  ).toEqual(1)
})

test("customIsNull", () => {
  expect(customIsNull(undefined), "Undefined is null").toBeTruthy()
  expect(customIsNull(null), "Null is null").toBeTruthy()
  expect(customIsNull(""), "Empty string is null").toBeTruthy()
  expect(customIsNull([]), "Empty array is null").toBeTruthy()
  expect(customIsNull({}), "Empty object is null").toBeTruthy()

  expect(customIsNull(0), "0 is not null").toBeFalsy()
  expect(customIsNull(1000), "1000 is not null").toBeFalsy()
  expect(customIsNull("abc"), "'abc' is not null").toBeFalsy()
  expect(customIsNull(["abc", 123]), "Non empty array is not null").toBeFalsy()
  expect(customIsNull({ abc: 123 }), "Non empty obj is not null").toBeFalsy()
})

describe("sieveSubmodel", () => {
  test("Empty object is empty :$", () => {
    expect(sieveSubmodel({})).toEqual([])
  })

  test("Sieve out empty entries", () => {
    expect(sieveSubmodel({ id: 0, nid: null })).toEqual([["id", 0]])
  })

  test("Takes optional array of keys to ignore", () => {
    expect(sieveSubmodel({ id: 0, nid: null }, ["id"])).toEqual([])
  })
})

describe("isEmptySubmodel", () => {
  test("Empty object is empty", () => {
    expect(isEmptySubmodel({})).toBeTruthy()
  })

  test("Object with empty fields is empty", () => {
    expect(isEmptySubmodel(OBJ_WITH_EMPTY_FIELDS)).toBeTruthy()
  })

  test("Object with non empty fields is not empty", () => {
    expect(isEmptySubmodel(OBJ_WITH_NON_EMPTY_FIELDS)).toBeFalsy()
  })

  test("Takes optional array of keys to ignore", () => {
    expect(
      isEmptySubmodel(
        OBJ_WITH_NON_EMPTY_FIELDS,
        Object.keys(OBJ_WITH_NON_EMPTY_FIELDS),
      ),
    ).toBeTruthy()
  })

  test("Always discards id and nid keys", () => {
    expect(isEmptySubmodel({ id: 1, nid: "sdf823uc" })).toBeTruthy()
    expect(isEmptySubmodel({ id: 1, nid: "sdf823uc" }, [])).toBeTruthy()
  })
})

describe("discardEmptySubmodels", () => {
  test("Filter empty submodels from a list", () => {
    expect(
      discardEmptySubmodels([OBJ_WITH_NON_EMPTY_FIELDS, OBJ_WITH_EMPTY_FIELDS]),
    ).toEqual([OBJ_WITH_NON_EMPTY_FIELDS])
  })

  test("Takes optional array of keys to ignore", () => {
    expect(
      discardEmptySubmodels(
        [OBJ_WITH_NON_EMPTY_FIELDS, OBJ_WITH_EMPTY_FIELDS],
        Object.keys(OBJ_WITH_NON_EMPTY_FIELDS),
      ),
    ).toEqual([])
  })

  test("Always discards id and nid keys", () => {
    expect(discardEmptySubmodels([{ id: 1, nid: "sdf823uc" }])).toEqual([])
    expect(discardEmptySubmodels([{ id: 1, nid: "sdf823uc" }], [])).toEqual([])
  })
})
