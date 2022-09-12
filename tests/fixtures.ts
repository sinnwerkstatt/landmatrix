import {
  test as base,
  Page,
  BrowserContext,
  PlaywrightWorkerArgs,
  TestFixture,
} from "@playwright/test";

type Level = "reporter" | "admin" | "editor";

type LevelContexts = { [key in Level]: LevelContext };

interface LevelContext {
  newPage: () => Promise<Page>;
  createDeal: () => Promise<number>;
  deleteDeal: (id: number) => Promise<void>;
}

const createContext =
  (level: Level): TestFixture<LevelContext, PlaywrightWorkerArgs> =>
  async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: `tests/storageState/${level}.json`,
    });
    await use({
      newPage: () => context.newPage(),
      createDeal: () => createTestDeal(context),
      deleteDeal: (id) => deleteTestDeal(context, id),
    });
    await context.close();
  };

export const test = base.extend<LevelContexts>({
  admin: createContext("admin"),
  editor: createContext("editor"),
  reporter: createContext("reporter"),
});

export const extractDealAndVersionId = (
  url: string
): [dealId: number, versionId: number] => {
  const pathname = new URL(url).pathname;
  return pathname.split("/").slice(-2).map(parseInt) as [number, number];
};

const createTestDeal = async (context: BrowserContext): Promise<number> => {
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

const deleteTestDeal = async (
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
