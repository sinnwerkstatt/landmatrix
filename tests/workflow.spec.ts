import { test as base, expect, Page } from "@playwright/test";

interface RoleFixtures {
  adminPage: Page;
  reporterPage: Page;
  editorPage: Page;
}

const test = base.extend<RoleFixtures>({
  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: "tests/storageState/admin.json",
    });
    const page = await context.newPage();
    await use(page);
    await page.close();
  },
  editorPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: "tests/storageState/editor.json",
    });
    const page = await context.newPage();
    await use(page);
    await page.close();
  },
  reporterPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: "tests/storageState/reporter.json",
    });
    const page = await context.newPage();
    await use(page);
    await page.close();
  },
});

const extractDealAndVersionId = (url: string): [dealId: number, versionId: number] => {
  const pathname = new URL(url).pathname;
  return pathname.split("/").slice(-2).map(parseInt) as [number, number];
};

const createTestDeal = async (page: Page) => {
  await page.goto("/deal/add");

  // Need to add location in order to be able to save
  await page.fill('[placeholder="Country"]', "Albania");
  await page.keyboard.press("Enter");

  await page.click('button:has-text("Save")');
  await page.click('button:has-text("Close")');
  const [dealId, versionId] = extractDealAndVersionId(page.url());

  return dealId;
};

const deleteTestDeal = async (page: Page, dealId: number) => {
  await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

  if (await page.locator('button:has-text("Delete")').isVisible()) {
    await page.click('button:has-text("Delete")');
    await page.waitForLoadState();

    await page.fill(
      "text=Please provide a comment explaining your request >> textarea",
      "It was just a test."
    );
    await page.click('button:has-text("Delete deal")');
  }
};

test.describe.parallel("Reporter", () => {
  test("Can create, edit and delete own drafts", async ({ reporterPage }) => {
    const dealId = await createTestDeal(reporterPage);

    await expect(
      reporterPage.locator(".status-field.active"),
      "Deal is in draft status."
    ).toHaveText("Draft");
    await expect(
      reporterPage.locator('a:has-text("Edit")'),
      "Reporter can edit own draft."
    ).toBeVisible();
    await expect(
      reporterPage.locator('button:has-text("Delete")'),
      "Reporter can delete own draft."
    ).toBeVisible();

    await deleteTestDeal(reporterPage, dealId);

    await expect(
      reporterPage.locator("text=500: Deal not found"),
      "Deal is deleted."
    ).toBeVisible();
  });

  test("Can submit deal for review", async ({ reporterPage, adminPage }) => {
    const dealId = await createTestDeal(reporterPage);

    await reporterPage.click('button:has-text("Submit for review")');
    await reporterPage.waitForLoadState();

    await reporterPage.check(
      'text=I\'ve read and agree to the Data policy >> input[type="checkbox"]'
    );
    await reporterPage.click('button:has-text("Submit for review") >> nth=1');

    await expect(
      reporterPage.locator(".status-field.active"),
      "Deal is in submitted for review status."
    ).toHaveText("Submitted for review");
    await expect(
      reporterPage.locator('a:has-text("Edit")'),
      "Reporter cannot edit submitted draft."
    ).not.toBeVisible();
    await expect(
      reporterPage.locator('button:has-text("Delete")'),
      "Reporter cannot delete submitted draft."
    ).not.toBeVisible();

    await deleteTestDeal(adminPage, dealId);
  });
});

test.describe.serial("Workflow", async () => {
  let dealId: number;
  let copyDealId: number;
  let _: number;

  test("Reporter creates new deal draft and submits it for review", async ({
    reporterPage: page,
  }) => {
    await createTestDeal(page);

    [dealId, _] = extractDealAndVersionId(page.url());

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

  test("Editor requests improvement", async ({ editorPage: page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

    await page.click('button:has-text("Request improvement")');
    await page.waitForLoadState();

    await page.fill(
      "text=Please provide a comment explaining your request >> textarea",
      "Data source and investor missing."
    );
    await page.click('button:has-text("Request improvement") >> nth=1');

    await expect(
      page.locator(".status-field.active"),
      "Deal is in draft status again."
    ).toHaveText("Draft");
  });

  test("Reporter improves draft and submits again", async ({ reporterPage: page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

    await page.click('a:has-text("Edit")');
    await page.waitForNavigation();

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
    editorPage: page,
  }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

    await page.click('button:has-text("Submit for activation")');
    await page.waitForLoadState();
    await page.click('button:has-text("Submit for activation") >> nth=1');

    await expect(
      page.locator(".status-field.active"),
      "Deal is submitted for activation."
    ).toHaveText("Submitted for activation");
  });

  test("Admin activates deal", async ({ adminPage: page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

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

  test("Admin deletes deal", async ({ adminPage: page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

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
      page.locator(`text=Deal #${dealId}`),
      "Deal is not publicly visible."
    ).not.toBeVisible();
  });

  test("Admin undeletes deal", async ({ adminPage: page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

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

  test("Admin copies deal", async ({ adminPage: page }) => {
    await page.goto(`/deal/${dealId}`, { waitUntil: "networkidle" });

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

  test.afterAll(async ({ adminPage: page }) => {
    for (const id of [dealId, copyDealId]) {
      await deleteTestDeal(page, id);
    }
  });
});
