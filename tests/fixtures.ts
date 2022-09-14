import { extractDealAndVersionId } from "./utils";
import {
  BrowserContext,
  Page,
  PlaywrightWorkerArgs,
  test as base,
  TestFixture,
} from "@playwright/test";

type Role = "reporter" | "admin" | "editor";

type RoleContexts = { [key in Role]: RoleContext };

interface RoleContext {
  newPage: () => Promise<Page>;
  createDeal: () => Promise<number>;
  deleteDeal: (id: number) => Promise<void>;
}

const createContext =
  (role: Role): TestFixture<RoleContext, PlaywrightWorkerArgs> =>
  async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: `tests/storageState/${role}.json`,
    });
    await use({
      newPage: () => context.newPage(),
      createDeal: () => createTestDeal(context),
      deleteDeal: (id) => deleteTestDeal(context, id),
    });
    await context.close();
  };

export const test = base.extend<RoleContexts>({
  admin: createContext("admin"),
  editor: createContext("editor"),
  reporter: createContext("reporter"),
});

export const createTestDeal = async (context: BrowserContext): Promise<number> => {
  const page = await context.newPage();

  await page.goto("/deal/add", { waitUntil: "networkidle" });

  // Need to fill any field in order to save
  await page.click("text=Overall comment");
  await page.fill('textarea[name="overall_comment"]', "Test Deal");

  await page.click('button:has-text("Save")');
  await page.waitForNavigation();

  const url = page.url();
  await page.close();
  return extractDealAndVersionId(url)[0];
};

export const deleteTestDeal = async (
  context: BrowserContext,
  dealId: number
): Promise<void> => {
  const page = await context.newPage();

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

  await page.close();
};
