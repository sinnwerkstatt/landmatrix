import { test } from "./fixtures";
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
      reporterPage.locator("text=401: Unauthorized"),
      "Reporter cannot see editor draft."
    ).toBeVisible();

    await reporterPage.goto(`/deal/${adminDealId}`);
    await expect(
      reporterPage.locator("text=401: Unauthorized"),
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
      reporterPage.locator('button:has-text("Remove")'),
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
      editorPage.locator('button:has-text("Remove")'),
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
      editorPage.locator('button:has-text("Remove")'),
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
      adminPage.locator('button:has-text("Remove")'),
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
      adminPage.locator('button:has-text("Remove")'),
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
      adminPage.locator('button:has-text("Remove")'),
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
