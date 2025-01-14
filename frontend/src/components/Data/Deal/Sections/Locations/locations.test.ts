import { createLocation, isEmptyLocation } from "./locations"

test("New location is empty", () => {
  expect(isEmptyLocation(createLocation("nid-123"))).toBeTruthy()
})
