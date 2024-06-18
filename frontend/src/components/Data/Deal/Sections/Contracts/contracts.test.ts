import { createContract, isEmptyContract } from "./contracts"

test("New contract is empty", () => {
  expect(isEmptyContract(createContract("nid-123"))).toBeTruthy()
})
