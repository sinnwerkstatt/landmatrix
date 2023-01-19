import { expect, test } from "@playwright/test";

test("happy path", async ({ page }) => {
  await page.goto("/account/login", { waitUntil: "networkidle" });
  await page.fill('text=Username >> [placeholder="Username"]', "shakespeare");
  await page.fill('text=Password >> [placeholder="Password"]', "hamlet4eva");

  await page.click('button:has-text("Login")');
  await page.waitForLoadState("networkidle");

  const wrap = page.locator(".text-green-500");

  await expect(wrap).toHaveText(/Login successful./);
});

test("unhappy path", async ({ page }) => {
  await page.goto("/account/login", { waitUntil: "networkidle" });
  await page.fill('text=Username >> [placeholder="Username"]', "shakespeare");
  await page.fill('text=Password >> [placeholder="Password"]', "wrong-password");

  await page.click('button:has-text("Login")');
  await page.waitForLoadState("networkidle");

  const wrap = page.locator(".text-red-500");

  await expect(wrap).toHaveText(/Invalid username or password/);
});
