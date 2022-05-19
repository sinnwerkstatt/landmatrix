import { test, expect } from "@playwright/test";

test.use({ storageState: "playwright-storageState.json" });

test.describe.serial("group", () => {
  let parentID;
  test("create parent investor", async ({ context, page }) => {
    await page.goto("/investor/add/");

    await page.locator('[placeholder="Name"]').fill("MomCorp");
    await page.locator("text=Select option Afghanistan >> div").nth(1).click();
    await page.locator('[placeholder="Select option"]').fill("united states");
    await page.locator('span:has-text("United States of America")').first().click();
    await page
      .locator('select[name="classification"]')
      .selectOption("PRIVATE_EQUITY_FIRM");
    await page.locator('[placeholder="Investor homepage"]').fill("http://momcorp.com");
    await page
      .locator('[placeholder="Opencorporates link"]')
      .fill("https://opencorporates.com/companies/gb/04366849");
    await page.locator('[aria-label="Comment"]').fill("testing comment");

    const p2saveButton = await page.locator("text=Save");
    await p2saveButton.click();
    await page.waitForLoadState("networkidle");
    await expect(p2saveButton).toBeDisabled();
    const headline = await page.locator(".investor-edit-heading > h1");
    await expect(headline).toContainText("Editing Investor #");
    parentID = (await headline.innerText()).replace("Editing Investor #", "");
    await page.close();
  });

  test("create child investor", async ({ context, page }) => {
    await page.goto("/investor/add/");

    await page.locator('[placeholder="Name"]').fill("Planet Express, Inc.");
    await page.locator("text=Select option Afghanistan >> div").nth(1).click();
    await page.locator('[placeholder="Select option"]').fill("ger");
    await page.locator('span:has-text("Germany")').first().click();
    await page.locator('select[name="classification"]').selectOption("PRIVATE_COMPANY");
    await page
      .locator('[placeholder="Investor homepage"]')
      .fill("http://planetexpress.com");
    await page
      .locator('[placeholder="Opencorporates link"]')
      .fill("https://opencorporates.com/companies/de/F1103R_HRB134255");
    await page
      .locator('[aria-label="Comment"]')
      .fill("Our crew is replaceable, your package isn't!");

    const saveButton = await page.locator("text=Save");
    await saveButton.click();
    await page.waitForLoadState("networkidle");
    await expect(saveButton).toBeDisabled();

    await page.locator("text=Parent companies").click();
    await page.locator("text=Add Parent company").click();
    // await page.locator("text=Investor").first().click();

    await page.locator("text=Investor Choose Investor >> div").nth(1).click();
    await page.locator('[placeholder="Choose Investor"]').fill("Mom");
    await page.locator(`text=MomCorp (#${parentID})`).click();
    await page.locator('[placeholder="\\30  – 100"]').fill("300");
    await page.locator('[placeholder="\\31 00\\.23"]').fill("1000001");

    await page.locator("text=Loan currency Currency >> div").nth(1).click();
    await page.locator('span:has-text("US Dollar (USD)")').first().click();
    await page.locator('[placeholder="YYYY-MM-DD"]').click();
    await page.locator('[placeholder="YYYY-MM-DD"]').fill("1990");
    await page.locator('select[name="parent_relation"]').selectOption("SUBSIDIARY");
    await page.locator(".submodel-body").click();
    await page.locator('[aria-label="Comment"]').fill("alternative names: e-corp");

    await saveButton.click();
    await page.waitForLoadState("networkidle");
    await expect(saveButton).toBeDisabled();
    const headline_child = await page.locator(".investor-edit-heading > h1");
    const childID = (await headline_child.innerText()).replace(
      "Editing Investor #",
      ""
    );

    await page.locator("text=Tertiary investors/lenders").click();
    await page.locator("text=Add Tertiary investor/lender").click();

    await page.locator("text=Investor Choose Investor >> div").nth(1).click();
    await page.locator('[placeholder="Choose Investor"]').fill("Mom");
    await page.locator(`text=MomCorp (#${parentID})`).click();
    await page.locator('[placeholder="\\30  – 100"]').fill("300");
    await page.locator('[placeholder="\\31 00\\.23"]').fill("1000001");

    await page.locator("text=Loan currency Currency >> div").nth(1).click();
    await page.locator('span:has-text("US Dollar (USD)")').first().click();
    await page.locator('[placeholder="YYYY-MM-DD"]').click();
    await page.locator('[placeholder="YYYY-MM-DD"]').fill("1990");
    await page.locator('select[name="parent_relation"]').selectOption("SUBSIDIARY");
    await page.locator(".submodel-body").click();
    await page.locator('[aria-label="Comment"]').fill("alternative names: e-corp");
    await saveButton.click();
    await page.waitForLoadState("networkidle");
    await expect(saveButton).toBeDisabled();

    await page.goto(`/investor/${childID}/`);
    await page.locator("text=Tertiary investor/lender");
    await page.locator("text=Parent company");

    const involvements = await page.locator(".investor-id-display").first().innerText();
    expect(involvements === parentID);
  });
});
