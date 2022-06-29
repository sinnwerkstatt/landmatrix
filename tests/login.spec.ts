import { expect, test } from "@playwright/test";

test("happy path", async ({ page }) => {
  await page.goto("/login", { waitUntil: "networkidle" });
  await page.fill('text=Username >> [placeholder="Username"]', "shakespeare");
  await page.fill('text=Password >> [placeholder="Password"]', "hamlet4eva");

  await page.click("button.btn-primary");
  await page.waitForLoadState("networkidle");

  const wrap = page.locator(".test-login");

  await expect(wrap).toHaveText(/You are logged in./);
});

test("unhappy path", async ({ page }) => {
  await page.goto("/login", { waitUntil: "networkidle" });
  await page.fill('text=Username >> [placeholder="Username"]', "shakespeare");
  await page.fill('text=Password >> [placeholder="Password"]', "wrong-password");

  await page.click("button.btn-primary");
  await page.waitForLoadState("networkidle");

  const wrap = page.locator(".test-login");

  await expect(wrap).toHaveText(/Invalid username or password/);
});
