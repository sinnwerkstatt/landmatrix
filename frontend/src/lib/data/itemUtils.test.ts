import {
  isDated,
  isCurrent,
  getFirstByDate,
  getLastByDate,
  parseDate,
} from "./itemUtils"

describe("isDated (typeguard)", () => {
  it("returns false if item has no date", () => {
    expect(isDated({})).toBeFalsy()
    expect(isDated({ value: 946684800000 })).toBeFalsy()
  })
  it("returns false if item has invalid date string", () => {
    expect(isDated({ date: "2020-2020" })).toBeFalsy()
  })
  it("returns true if item has valid date string", () => {
    expect(isDated({ date: "2020" })).toBeTruthy()
    expect(isDated({ date: "2020-01-31" })).toBeTruthy()
  })
})

describe("isCurrent (typeguard)", () => {
  it("returns false if item has no current flag", () => {
    expect(isCurrent({})).toBeFalsy()
    expect(isCurrent({ value: 946684800000 })).toBeFalsy()
  })
  it("returns value of current flag", () => {
    expect(isCurrent({ current: true })).toBeTruthy()
    expect(isCurrent({ current: false })).toBeFalsy()
  })
})

describe("getFirstByDate", () => {
  it("returns undefined for no and undated items", () => {
    expect(getFirstByDate([])).toBeUndefined()
    expect(
      getFirstByDate([{ value: 10 }, { value: 15 }, { value: 30 }]),
    ).toBeUndefined()
  })
  it("returns earliest item", () => {
    expect(
      getFirstByDate([
        { value: 10, date: "2020" },
        { value: 20, date: "2010" },
        { value: 30, date: "2015" },
      ]),
    ).toEqual({ value: 20, date: "2010" })
  })
})

describe("getLastByDate", () => {
  it("returns undefined for no and undated items", () => {
    expect(getLastByDate([])).toBeUndefined()
    expect(getLastByDate([{ value: 10 }, { value: 15 }, { value: 30 }])).toBeUndefined()
  })
  it("returns latest item", () => {
    expect(
      getLastByDate([
        { value: 10, date: "2020-05-05" },
        { value: 20, date: "2020-01" },
        { value: 30, date: "2020-05" },
      ]),
    ).toEqual({ value: 10, date: "2020-05-05" })
  })
})

describe("parseDate", () => {
  it("parses strings 'YYYY-MM-DD' and returns full year", () => {
    expect(parseDate("1700")).toEqual(1700)
    expect(parseDate("1950")).toEqual(1950)
    expect(parseDate("2010")).toEqual(2010)
    expect(parseDate("2010-01")).toEqual(2010)
    expect(parseDate("2010-12-31")).toEqual(2010)
  })
})
