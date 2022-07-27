import "@testing-library/jest-dom";
import { fireEvent, render, screen } from "@testing-library/svelte";
import NewTable from "./NewTable.svelte";

test("columns shown in document", () => {
  const columns = ["hi", "there"];
  render(NewTable, { columns });

  columns.forEach((col) => {
    const el = screen.getByText(col);
    expect(el).toBeInTheDocument();
  });
});
//
// // Note: This is as an async test as we are using `fireEvent`
// test("changes button text on click", async () => {
//   render(NewTable, { name: "World" });
//   const button = screen.getByRole("button");
//
//   // Using await when firing events is unique to the svelte testing library because
//   // we have to wait for the next `tick` so that Svelte flushes all pending state changes.
//   await fireEvent.click(button);
//
//   expect(button).toHaveTextContent("Button Clicked");
// });
