import { createInvolvement, isEmptyInvolvement } from "./involvements"

test("New involvement is empty", () => {
  expect(isEmptyInvolvement(createInvolvement(true, 1)("nid-123"))).toBeTruthy()
  expect(isEmptyInvolvement(createInvolvement(false, 1)("nid-123"))).toBeTruthy()
})
