import { expect, test } from "@playwright/test";

test.use({ storageState: "playwright-storageState.json" });

test("basic cms", async ({ context, page }) => {
  await page.goto("/cms");

  //delete after fixing global setup:
  await page.locator('[placeholder="Enter your username"]').click();
  await page.locator('[placeholder="Enter your username"]').fill("shakespeare");
  await page.locator('[placeholder="Enter password"]').fill("hamlet4eva");
  await page.locator('button:has-text("Sign in")').click();

  // create observatory index page
  await page.locator("text=Pages").first().click();
  await page.locator("text=Land MatrixEnglish").click();
  await page.locator("[aria-label=\"Add a child page to \\'Land Matrix\\' \"]").click();

  //check if observatory index page already exists:
  const indexPage = await page.$("text='Observatory index page'");
  if (!indexPage) {
    console.log("obs index page already exists");
    await page.locator("text=Pages").first().click();
    await page.locator('h3:has-text("Land Matrix")').click();
    await page.locator("text=observatory").first().click();
    await page.locator("div.dropdown-toggle").last().click();
    await Promise.all([page.waitForNavigation(), page.locator("text=Delete").click()]);
    await Promise.all([
      page.waitForNavigation(),
      await page.locator("text=Yes, delete it").click(),
    ]);
    await Promise.all([
      page.waitForNavigation(),
      await page
        .locator("[aria-label=\"Add a child page to \\'Land Matrix\\' \"]")
        .click(),
    ]);
    await page.reload();
  }
  await page.locator("text=Pages").first().click();
  await page.locator("text=Land MatrixEnglish").click();
  await Promise.all([
    page.waitForNavigation(),
    await page
      .locator("[aria-label=\"Add a child page to \\'Land Matrix\\' \"]")
      .click(),
  ]);

  await page.locator("text=Observatory index page").first().click();
  await page.locator('input[name="title_en"]').fill("observatory");
  await page.locator('input[name="title_en"]').press("Enter");

  //create observatory child page
  await page.locator("text=Pages").first().click();
  await page.locator("a:has-text(\"View child pages of 'Land Matrix'\")").click();
  await page.locator('h3:has-text("observatory")').click();
  await page.locator("text=Add child page").click();
  await page.locator('input[name="title_en"]').fill("global");
  await page.locator("text=Paragraph").first().click();
  await page.locator('div[role="textbox"] div').nth(2).click();
  await page.keyboard.type("test global child page");
  await page.locator("div.dropdown-toggle").first().click();

  //ToDo: needs Fixing to delete timeout
  await page.evaluate(() => {
    return new Promise((resolve) => setTimeout(resolve, 500));
  });
  await Promise.all([
    page.waitForNavigation(),
    page.locator('button:has-text("Publish")').click(),
  ]);

  await page.locator("text=View live").first().click(),
    await expect(page.locator("h3 >> nth=0")).toContainText(
      "We currently have information about:"
    );
  await page.locator("text=Observatories").click();
  await page.locator("text=Observatories global >> a").click();
});
