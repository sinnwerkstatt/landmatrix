import { createDataSource, isEmptyDataSource } from "./dataSources"

test("New data source is empty", () => {
  expect(isEmptyDataSource(createDataSource("nid-123"))).toBeTruthy()
})
