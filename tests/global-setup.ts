import { chromium, FullConfig } from "@playwright/test";

// https://playwright.dev/docs/test-auth#multiple-signed-in-roles
const USERS = [
  {
    level: "admin",
    username: "shakespeare",
    password: "hamlet4eva",
  },
  {
    level: "editor",
    username: "test_editor",
    password: "love2edit",
  },
  {
    level: "reporter",
    username: "test_reporter",
    password: "love2report",
  },
];

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch();

  for (const user of USERS) {
    const page = await browser.newPage();
    await page.goto("localhost:9000/account/login", {
      waitUntil: "networkidle",
    });

    await page.fill('text=Username >> [placeholder="Username"]', user.username);
    await page.fill('text=Password >> [placeholder="Password"]', user.password);
    await page.click('button:has-text("Login")');
    await page.locator("text=Login successful.").waitFor();
    await page
      .context()
      .storageState({ path: `tests/storageState/${user.level}.json` });
  }

  await browser.close();
}

export default globalSetup;
