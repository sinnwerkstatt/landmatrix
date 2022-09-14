import { expect, test } from "@playwright/test";

test.use({ storageState: "tests/storageState/admin.json" });

test.describe.serial("basic cms tests", () => {
  async function publishNewPage(page) {
    await page.locator("div.dropdown-toggle").first().click();
    await Promise.all([
      page.waitForNavigation(),
      page.locator('button:has-text("Publish")').click(),
    ]);
  }

  test("basic cms", async ({ context, page }) => {
    await page.goto("/map");
    await Promise.all([
      page.waitForNavigation(),
      page.locator('a:has-text("Map")').nth(1).click(),
    ]);
    await expect(page.locator('h3:has-text("Filter")')).toBeVisible();
    await page.locator("text=Table").click();
    await Promise.all([
      page.waitForNavigation(),
      page.locator("text=Deals").nth(2).click(),
    ]);
    await expect(await page.locator("text=Target country")).toBeVisible();
  });

  test("create observatory page", async ({ context, page }) => {
    await page.goto("/cms");

    // create observatory index page
    await page.locator("text=Pages").first().click();
    await page.locator("text=Land MatrixEnglish").click();
    await page
      .locator("[aria-label=\"Add a child page to \\'Land Matrix\\' \"]")
      .click();

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
    await page.locator("text=Section divider").first().click();
    await publishNewPage(page);
    await page.locator("text=View live").first().click();
    await expect(page.locator("h3 >> nth=0")).toContainText(
      "We currently have information about:"
    );
    await page.locator("text=Observatories").click();
    await page.locator("text=Observatories global >> a").click();
  });

  test("create wagtail page", async ({ context, page }) => {
    await page.goto("/cms");

    await page.locator("text=Pages").first().click();
    await page.locator('h3:has-text("Land Matrix")').click();
    await page
      .locator("[aria-label=\"Add a child page to \\'Land Matrix\\' \"]")
      .click();
    await page.locator("text=Wagtail page").first().click();
    await page.locator('input[name="title_en"]').fill("Contribute");
    await page.locator(".c-sf-button").first().click();
    await page.locator('input[name="body_en-0-value"]').click();
    await page.locator('input[name="body_en-0-value"]').fill("Test Title");
    await publishNewPage(page);
    await page.locator("text=View live").first().click();
    await Promise.all([
      page.waitForNavigation(),
      page.locator('a:has-text("Contribute")').click(),
    ]);

    await expect(page.locator("text=Test Title")).toBeVisible();
  });

  test("create blog page", async ({ context, page }) => {
    await page.goto("/cms");
    //create blog category
    await page.locator("text=Snippets").click();
    await page.locator("text=Blog Categories").click();
    await page.locator("text=Add Blog Category").click();
    await page.locator('input[name="name"]').click();
    await page.locator('input[name="name"]').fill("News");
    await page.locator('input[name="name"]').press("Enter");
    //create blog index page
    await page.locator("text=Pages").first().click();
    await page.locator('h3:has-text("Land Matrix")').click();
    await Promise.all([
      page.waitForNavigation(),
      await page.locator("text=Add child page").first().click(),
    ]);
    await page.locator("text=Blog index").first().click();
    await page.locator('input[name="title_en"]').fill("Resources");
    await publishNewPage(page);
    //create blog Article page
    await page.locator("a[title=\"Add a child page to 'Resources'\"]").click();
    await page.locator('input[name="title_en"]').fill("Blog Article");
    await page.locator('text="News"').click();
    await page.locator("text=Section divider").click();
    await publishNewPage(page);
    //checkout frontend
    await page.goto("/");
    await page.locator("text=Resources").click();
    await Promise.all([
      page.waitForNavigation(),
      page.locator("text=Resources News >> a").click(),
    ]);
    await Promise.all([
      page.waitForNavigation(),
      page.locator('a:has-text("Blog Article")').click(),
    ]);
  });

  test.afterAll(async ({ context, page }) => {
    await page.goto("/cms");
    //delete pages
    await page.locator("text=Pages").first().click();
    await page.locator('h3:has-text("Land Matrix")').click();
    await page.locator('input[type="checkbox"]').first().check();
    await Promise.all([
      page.waitForNavigation(),
      await page.locator("text=Delete").last().click(),
    ]);
    await page.locator("text=Yes, delete").click();
    //Delete category "News"
    await page.locator("text=Snippets").click();
    await page.locator("text=Blog Categories").click();
    await page
      .locator('text=Select all Blog Categories Title >> input[type="checkbox"]')
      .check();
    await page.locator("text=Delete Blog Categories").click();
    await page.locator("text=Yes, delete").click();
  });
});
