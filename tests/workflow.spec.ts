import { extractDealAndVersionId, test } from "./fixtures";
import { expect } from "@playwright/test";

test.describe("Roles", () => {
  let adminDealId: number;
  let editorDealId: number;
  let reporterDealId: number;

  test.beforeAll(async ({ reporter, admin, editor }) => {
    adminDealId = await admin.createDeal();
    editorDealId = await editor.createDeal();
    reporterDealId = await reporter.createDeal();
  });

  test.afterAll(async ({ admin }) => {
    await admin.deleteDeal(adminDealId);
    await admin.deleteDeal(editorDealId);
    await admin.deleteDeal(reporterDealId);
  });

  test("Reporter access", async ({ reporter }) => {
    const reporterPage = await reporter.newPage();

    await reporterPage.goto(`/deal/${reporterDealId}`);
    await expect(
      reporterPage.locator(`text=Deal #${reporterDealId}`),
      "Reporter can see reporter draft."
    ).toBeVisible();

    await reporterPage.goto(`/deal/${editorDealId}`);
    await expect(
      reporterPage.locator("text=404: Deal not found"),
      "Reporter cannot see editor draft."
    ).toBeVisible();

    await reporterPage.goto(`/deal/${adminDealId}`);
    await expect(
      reporterPage.locator("text=404: Deal not found"),
      "Reporter cannot see admin draft."
    ).toBeVisible();
  });

  test("Reporter actions", async ({ reporter }) => {
    const reporterPage = await reporter.newPage();
    await reporterPage.goto(`/deal/${reporterDealId}`);

    await expect(
      reporterPage.locator('a:has-text("Edit")'),
      "Reporter can edit own draft."
    ).toBeVisible();
    await expect(
      reporterPage.locator('button:has-text("Delete")'),
      "Reporter can delete own draft."
    ).toBeVisible();
    await expect(
      reporterPage.locator('button:has-text("Submit for review")'),
      "Reporter can submit own draft for review."
    ).toBeVisible();

    await reporterPage.click('button:has-text("Submit for review")');
    await reporterPage.waitForLoadState();

    await reporterPage.check(
      'text=I\'ve read and agree to the Data policy >> input[type="checkbox"]'
    );
    await reporterPage.click('button:has-text("Submit for review") >> nth=1');

    await expect(
      reporterPage.locator('a:has-text("Edit")'),
      "Reporter cannot edit draft (submitted for review)."
    ).not.toBeVisible();
    await expect(
      reporterPage.locator('button:has-text("Delete")'),
      "Reporter cannot delete draft (submitted for review)."
    ).not.toBeVisible();
    await expect(
      reporterPage.locator('button:has-text("Request Improvement")'),
      "Editor cannot request improvement on draft (submitted for review)."
    ).not.toBeVisible();
    await expect(
      reporterPage.locator('button:has-text("Submit for activation")'),
      "Editor cannot submit draft (submitted for review) for activation."
    ).not.toBeVisible();
  });

  test("Editor access", async ({ editor }) => {
    const editorPage = await editor.newPage();

    await editorPage.goto(`/deal/${reporterDealId}`);
    await expect(
      editorPage.locator(`text=Deal #${reporterDealId}`),
      "Editor can see reporter draft."
    ).toBeVisible();

    await editorPage.goto(`/deal/${editorDealId}`);
    await expect(
      editorPage.locator(`text=Deal #${editorDealId}`),
      "Editor can see editor draft."
    ).toBeVisible();

    await editorPage.goto(`/deal/${adminDealId}`);
    await expect(
      editorPage.locator(`text=Deal #${adminDealId}`),
      "Editor can see admin draft."
    ).toBeVisible();
  });

  test("Editor actions", async ({ editor }) => {
    const editorPage = await editor.newPage();
    await editorPage.goto(`/deal/${editorDealId}`);

    await expect(
      editorPage.locator('a:has-text("Edit")'),
      "Editor can edit own draft."
    ).toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Delete")'),
      "Editor can delete own draft."
    ).toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Submit for review")'),
      "Editor can submit own draft for review."
    ).toBeVisible();

    await editorPage.click('button:has-text("Submit for review")');
    await editorPage.waitForLoadState();

    await editorPage.check(
      'text=I\'ve read and agree to the Data policy >> input[type="checkbox"]'
    );
    await editorPage.click('button:has-text("Submit for review") >> nth=1');

    await expect(
      editorPage.locator('a:has-text("Edit")'),
      "Editor can create new version of draft (submitted for review)."
    ).toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Delete")'),
      "Editor can delete draft (submitted for review)."
    ).toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Request Improvement")'),
      "Editor can request improvement on draft (submitted for review)."
    ).toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Submit for activation")'),
      "Editor can submit draft (submitted for review) for activation."
    ).toBeVisible();

    await editorPage.click('button:has-text("Submit for activation")');
    await editorPage.waitForLoadState();
    await editorPage.click('button:has-text("Submit for activation") >> nth=1');

    await expect(
      editorPage.locator('a:has-text("Edit")'),
      "Editor cannot create new version of draft (submitted for activation)."
    ).not.toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Delete")'),
      "Editor cannot delete draft (submitted for activation)."
    ).not.toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Request Improvement")'),
      "Editor cannot request improvement of draft (submitted for activation)."
    ).not.toBeVisible();
    await expect(
      editorPage.locator('button:has-text("Activate")'),
      "Editor cannot activate draft (submitted for activation)."
    ).not.toBeVisible();
  });

  test("Admin access", async ({ admin }) => {
    const adminPage = await admin.newPage();

    await adminPage.goto(`/deal/${reporterDealId}`);
    await expect(
      adminPage.locator(`text=Deal #${reporterDealId}`),
      "Admin can see reporter draft."
    ).toBeVisible();

    await adminPage.goto(`/deal/${editorDealId}`);
    await expect(
      adminPage.locator(`text=Deal #${editorDealId}`),
      "Admin can see editor draft."
    ).toBeVisible();

    await adminPage.goto(`/deal/${adminDealId}`);
    await expect(
      adminPage.locator(`text=Deal #${adminDealId}`),
      "Admin can see admin draft."
    ).toBeVisible();
  });

  test("Admin actions", async ({ admin }) => {
    const adminPage = await admin.newPage();
    await adminPage.goto(`/deal/${adminDealId}`);

    await expect(
      adminPage.locator('a:has-text("Edit")'),
      "Admin can edit own draft."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Delete")'),
      "Admin can delete own draft."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Submit for review")'),
      "Admin can submit own draft for review."
    ).toBeVisible();

    await adminPage.click('button:has-text("Submit for review")');
    await adminPage.waitForLoadState();

    await adminPage.check(
      'text=I\'ve read and agree to the Data policy >> input[type="checkbox"]'
    );
    await adminPage.click('button:has-text("Submit for review") >> nth=1');

    await expect(
      adminPage.locator('a:has-text("Edit")'),
      "Admin can create new version of draft (submitted for review)."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Delete")'),
      "Admin can delete draft (submitted for review)."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Request Improvement")'),
      "Admin can request improvement on draft (submitted for review)."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Submit for activation")'),
      "Admin can submit draft (submitted for review) for activation."
    ).toBeVisible();

    await adminPage.click('button:has-text("Submit for activation")');
    await adminPage.waitForLoadState();
    await adminPage.click('button:has-text("Submit for activation") >> nth=1');

    await adminPage.pause();
    await expect(
      adminPage.locator('a:has-text("Edit")'),
      "Admin can create new version of draft (submitted for activation)."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Delete")'),
      "Admin can delete draft (submitted for activation)."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Request Improvement")'),
      "Admin can request improvement of draft (submitted for activation)."
    ).toBeVisible();
    await expect(
      adminPage.locator('button:has-text("Activate")'),
      "Admin can activate draft (submitted for activation)."
    ).toBeVisible();
  });
});

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
