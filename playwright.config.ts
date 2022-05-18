import { PlaywrightTestConfig, devices } from "@playwright/test";

const config: PlaywrightTestConfig = {
  globalSetup: require.resolve("./tests/global-setup"),
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  use: {
    headless: true,
    viewport: { width: 1920, height: 1080 },
    baseURL: "http://localhost:3000/",
    ignoreHTTPSErrors: true,
    trace: "on-first-retry",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    // { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    // { name: "webkit", use: { ...devices["Desktop Safari"] } },
  ],
};
export default config;
