import { aDownload } from "./download"

describe("aDownload", () => {
  beforeEach(() => {
    // Create mocks for browser dependent functions
    global.URL.createObjectURL = vi.fn(() => "blob:test-url")
    global.URL.revokeObjectURL = vi.fn()
  })

  afterEach(() => {
    // Clean up mocks
    vi.resetAllMocks()
  })

  it("should create a download link and trigger a download", () => {
    const blob = new Blob(["name,age\nAlice,30\nBob,25"], { type: "text/csv" })
    const fileName = "test.csv"

    // Create a real anchor element and spy on its click method.
    const anchor = document.createElement("a")
    const clickSpy = vi.spyOn(anchor, "click").mockImplementation(vi.fn())

    // Mock document.createElement to return our real anchor.
    vi.spyOn(document, "createElement").mockReturnValue(anchor)

    // Act: Call the aDownload function with a blob
    aDownload(blob, fileName)

    // Assert: Check that createObjectURL was called with the provided blob
    expect(global.URL.createObjectURL).toHaveBeenCalledTimes(1)
    expect(global.URL.createObjectURL).toHaveBeenCalledWith(blob)

    // Assert: Check that the link's download attribute is set correctly
    expect(anchor.download).toBe(fileName)
    expect(anchor.href).toBe("blob:test-url")

    // Assert: Check that the anchor's click method was called
    expect(clickSpy).toHaveBeenCalledTimes(1)

    // Assert: Check that revokeObjectURL was called with the correct URL
    expect(global.URL.revokeObjectURL).toHaveBeenCalledTimes(1)
    expect(global.URL.revokeObjectURL).toHaveBeenCalledWith("blob:test-url")
  })
})
