import { chromium, expect, FullConfig } from "@playwright/test";

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  // await page.goto("http://localhost:3000/login", { waitUntil: "networkidle" });
  // await page.fill('text=Username >> [placeholder="Username"]', "shakespeare");
  // await page.fill('text=Password >> [placeholder="Password"]', "hamlet4eva");
  // await page.click("button.btn-primary");
  // await page.waitForLoadState("networkidle");
  //
  // const wrap = page.locator(".test-login");
  //
  // await expect(wrap).toHaveText(/You are logged in./);

  // Save signed-in state to 'playwright-storageState.json'.
  await page.context().storageState({ path: "playwright-storageState.json" });
  await browser.close();
}

export default globalSetup;
