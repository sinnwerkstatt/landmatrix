import "@testing-library/jest-dom"
import { render, screen } from "@testing-library/svelte"
import { userEvent } from "@testing-library/user-event"

import Table from "./Table.svelte"

test("Column labels are shown", () => {
  const columns = ["col1", "col2"]
  const labels = ["colName1", "colName2"]

  render(Table, { columns, labels })

  columns.forEach((col, index) => {
    const el = screen.getByText(labels[index])
    expect(el).toBeInTheDocument()
  })
})

describe("Sorting", () => {
  const columns = ["col1", "col2"]
  const items = [
    { col1: 2, col2: "second" },
    { col1: 1, col2: "first" },
  ]

  test("Default", () => {
    render(Table, { columns, items })

    expect(screen.getByTestId("0-0")).toHaveTextContent("2")
    expect(screen.getByTestId("0-1")).toHaveTextContent("second")
  })

  test("By column", async () => {
    const user = userEvent.setup()

    render(Table, {
      columns,
      labels: ["colName1", "colName2"],
      items,
      sortBy: "col1",
    })

    expect(screen.getByTestId("0-0")).toHaveTextContent("1")
    expect(screen.getByTestId("1-0")).toHaveTextContent("2")

    await user.click(screen.getByText("colName1"))
    expect(screen.getByTestId("0-0")).toHaveTextContent("2")
    expect(screen.getByTestId("1-0")).toHaveTextContent("1")

    await user.click(screen.getByText("colName2"))
    expect(screen.getByTestId("0-1")).toHaveTextContent("first")
    expect(screen.getByTestId("1-1")).toHaveTextContent("second")

    await user.click(screen.getByText("colName2"))
    expect(screen.getByTestId("0-1")).toHaveTextContent("second")
    expect(screen.getByTestId("1-1")).toHaveTextContent("first")
  })
})

describe("Column spans", () => {
  const columns = ["col1", "col2", "col3"]
  const items = [
    { col1: 1, col2: "first", col3: true },
    { col1: 2, col2: "second", col3: false },
  ]

  test("Default to equal span for all columns", () => {
    render(Table, { columns, items })

    expect(screen.getByTestId("0-0")).toHaveStyle("grid-column: span 1 / span 1")
    expect(screen.getByTestId("0-1")).toHaveStyle("grid-column: span 1 / span 1")
    expect(screen.getByTestId("0-2")).toHaveStyle("grid-column: span 1 / span 1")
  })

  test("Spans are correctly applied when passed as props", () => {
    render(Table, {
      columns,
      items,
      spans: [3, 1, 5],
    })

    expect(screen.getByTestId("0-0")).toHaveStyle("grid-column: span 3 / span 3")
    expect(screen.getByTestId("0-1")).toHaveStyle("grid-column: span 1 / span 1")
    expect(screen.getByTestId("0-2")).toHaveStyle("grid-column: span 5 / span 5")
  })
})
