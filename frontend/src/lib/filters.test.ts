import { FilterValues } from "$lib/filters"

describe("filters", () => {
  test("isDefault", () => {
    expect(new FilterValues().isDefault()).toBeFalsy()
    expect(new FilterValues().empty().isDefault()).toBeFalsy()
    expect(new FilterValues().default().isDefault()).toBeTruthy()
  })
})
