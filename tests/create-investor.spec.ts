import { expect, test } from "@playwright/test";

test.use({ storageState: "tests/storageState/admin.json" });

test("create new investor", async ({ context, page }) => {
  await page.goto("/");
  await page.pause();
});
