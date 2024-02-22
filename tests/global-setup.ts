import { chromium, FullConfig } from "@playwright/test";

// https://playwright.dev/docs/test-auth#multiple-signed-in-roles
const USERS = [
  {
    role: "admin",
    username: "shakespeare",
    password: "hamlet4eva",
  },
  {
    role: "editor",
    username: "test_editor",
    password: "love2edit",
  },
  {
    role: "reporter",
    username: "test_reporter",
    password: "love2report",
  },
];

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch();

  for (const user of USERS) {
    const page = await browser.newPage();

    // TOOD: RD - remove debug
    page.on("console", (message) => {
      console.log(`Log: "${message.text()}"`);
    });
    page.on("pageerror", (exception) => {
      console.log(`ERR: "${exception}"`);
    });

    await page.goto("localhost:9000/account/login", {
      waitUntil: "networkidle",
    });

    // TOOD: RD - remove debug
    // console.log(await page.content());

    await page.fill('text=Username >> [placeholder="Username"]', user.username);
    await page.fill('text=Password >> [placeholder="Password"]', user.password);
    await page.click('button:has-text("Login")');
    await page.locator("text=Login successful.").waitFor();
    await page
      .context()
      .storageState({ path: `tests/storageState/${user.role}.json` });
  }

  await browser.close();
}

export default globalSetup;
