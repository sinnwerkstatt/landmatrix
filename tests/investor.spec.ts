import { test, expect } from "@playwright/test";

test.use({ storageState: "playwright-storageState.json" });

test("basic test", async ({ page }) => {
  await page.goto("/investor/add/");

  await page.locator('[placeholder="Name"]').fill("sinnwerkstatt medienagentur GmbH");
  // Click text=Select option Afghanistan Åland Islands Albania Algeria American Samoa Andorra A >> div >> nth=1
  await page
    .locator(
      "text=Select option Afghanistan Åland Islands Albania Algeria American Samoa Andorra A >> div"
    )
    .nth(1)
    .click();
  // Fill [placeholder="Select option"]
  await page.locator('[placeholder="Select option"]').fill("ger");
  // Click span:has-text("Germany") >> nth=0
  await page.locator('span:has-text("Germany")').first().click();
  // Select PRIVATE_COMPANY
  await page.locator('select[name="classification"]').selectOption("PRIVATE_COMPANY");

  await page.locator('[placeholder="Investor homepage"]').fill("sinnwerkstatt.com");
  await page
    .locator('[placeholder="Opencorporates link"]')
    .fill("https://opencorporates.com/companies/de/F1103R_HRB134255");
  await page.locator('[aria-label="Comment"]').fill("testing comment");

  await page.locator("text=Save").click();
  await page.pause();
});
