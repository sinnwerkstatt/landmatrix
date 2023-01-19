import { devices, PlaywrightTestConfig } from "@playwright/test";

const config: PlaywrightTestConfig = {
  globalSetup: require.resolve("./tests/global-setup"),
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  use: {
    headless: true,
    // viewport: { width: 1920, height: 1080 },
    baseURL: "http://localhost:9000/",
    ignoreHTTPSErrors: true,
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1920, height: 1080 } },
    },
    // { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    // { name: "webkit", use: { ...devices["Desktop Safari"] } },
  ],
  reporter: process.env.CI
    ? [["dot"], ["junit", { outputFile: "results.xml" }]]
    : "list",
};
export default config;
