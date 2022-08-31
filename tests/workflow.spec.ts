import { extractDealAndVersionId, test } from "./fixtures";
import { expect } from "@playwright/test";

test.describe.serial("Workflow", async () => {
  let dealId: number;
  let copyDealId: number;
  let _: number;

  test.afterAll(async ({ admin }) => {
    for (const id of [dealId, copyDealId]) {
      await admin.deleteDeal(id);
    }
  });

  test("Reporter creates new deal draft and submits it for review", async ({
    reporter,
  }) => {
    dealId = await reporter.createDeal();

    const page = await reporter.newPage();
    await page.goto(`/deal/${dealId}`);

    await expect(
      page.locator(".status-field.active"),
      "Deal is in draft status."
    ).toHaveText("Draft");

    await page.click('button:has-text("Submit for review")');
    await page.waitForLoadState();

    await page.check(
      'text=I\'ve read and agree to the Data policy >> input[type="checkbox"]'
    );
    await page.click('button:has-text("Submit for review") >> nth=1');

    await expect(
      page.locator(".status-field.active"),
      "Deal is in submitted for review status."
    ).toHaveText("Submitted for review");
  });

  test("Editor requests improvement", async ({ editor }) => {
    const page = await editor.newPage();
    await page.goto(`/deal/${dealId}`);

    await page.click('button:has-text("Request improvement")');
    await page.waitForLoadState();

    await page.fill(
      "text=Please provide a comment explaining your request >> textarea",
      "Location, data source and investor missing."
    );
    await page.click('button:has-text("Request improvement") >> nth=1');

    await expect(
      page.locator(".status-field.active"),
      "Deal is in draft status again."
    ).toHaveText("Draft");
  });

  test("Reporter improves draft and submits again", async ({ reporter }) => {
    const page = await reporter.newPage();
    await page.goto(`/deal/${dealId}`);

    await page.click('a:has-text("Edit")');
    await page.waitForNavigation();

    await page.fill('input[placeholder="Country"]', "Albania");
    await page.keyboard.press("Enter");

    // switch to investor tab
    await page.click("text=Investor info");
    await page.waitForLoadState();

    await page.fill('input[placeholder="Investor"]', "#40260");
    await page.locator("text=Test Company (#40260) >> nth=1").click();

    // switch to data source tab
    await page.click("text=Data sources");
    await page.waitForLoadState();

    await page.click("text=Add Data source");
    await page.selectOption('select[name="type"]', "MEDIA_REPORT");

    // save and close
    await page.click('button:has-text("Save")');
    await page.click('button:has-text("Close")');

    await page.click('button:has-text("Submit for review")');
    await page.waitForLoadState();

    await page.check(
      'text=I\'ve read and agree to the Data policy >> input[type="checkbox"]'
    );
    await page.click('button:has-text("Submit for review") >> nth=1');

    await expect(
      page.locator(".status-field.active"),
      "Deal is in submitted for review status."
    ).toHaveText("Submitted for review");
  });

  test("Editor accepts improvement by submitting for activation", async ({
    editor,
  }) => {
    const page = await editor.newPage();
    await page.goto(`/deal/${dealId}`);

    await page.click('button:has-text("Submit for activation")');
    await page.waitForLoadState();
    await page.click('button:has-text("Submit for activation") >> nth=1');

    await expect(
      page.locator(".status-field.active"),
      "Deal is submitted for activation."
    ).toHaveText("Submitted for activation");
  });

  test("Admin activates deal", async ({ admin }) => {
    const page = await admin.newPage();
    await page.goto(`/deal/${dealId}`);

    await page.click('button:has-text("Activate")');
    await page.waitForLoadState();
    await page.click('button:has-text("Activate") >> nth=1');

    await expect(page.locator("text=Activated"), "Deal is activated.").toBeVisible();
  });

  test("Deal is publicly visible", async ({ page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

    await expect(
      page.locator(`text=Deal #${dealId}`),
      "Deal is publicly visible."
    ).toBeVisible();
  });

  test("Admin deletes deal", async ({ admin }) => {
    const page = await admin.newPage();
    await page.goto(`/deal/${dealId}`);

    await page.click('button:has-text("Delete")');
    await page.waitForLoadState();

    await page.fill(
      "text=Please provide a comment explaining your request >> textarea",
      "Let's delete it..."
    );
    await page.click('button:has-text("Delete deal")');

    await expect(
      page.locator("text=Deleted >> nth=0"),
      "Deal is deleted."
    ).toBeVisible();
  });

  test("Deal is no longer publicly visible", async ({ page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

    await expect(
      page.locator("text=404: Deal not found"),
      "Deal is not publicly visible."
    ).toBeVisible();
  });

  test("Admin undeletes deal", async ({ admin }) => {
    const page = await admin.newPage();
    await page.goto(`/deal/${dealId}`);

    await page.click('button:has-text("Undelete")');
    await page.waitForLoadState();

    await page.fill(
      "text=Please provide a comment explaining your request >> textarea",
      "...It's part of the test."
    );
    await page.click('button:has-text("Reactivate deal")');

    await expect(
      page.locator("text=Activated"),
      "Deal is activated again."
    ).toBeVisible();
  });

  test("Admin copies deal", async ({ admin }) => {
    const page = await admin.newPage();
    await page.goto(`/deal/${dealId}`);

    await page.click('button:has-text("Copy deal")');
    await page.waitForLoadState();

    await page.click('button:has-text("Copy deal") >> nth=1');
    const newPage = await page.waitForEvent("popup");

    [copyDealId, _] = extractDealAndVersionId(newPage.url());

    await expect(
      newPage.locator(`text=Deal #${copyDealId} Albania`),
      "Copied deal Id and country are visible."
    ).toBeVisible();

    await expect(
      newPage.locator(".status-field.active"),
      "Copied deal is in draft status."
    ).toHaveText("Draft");

    await newPage.close();
  });
});
