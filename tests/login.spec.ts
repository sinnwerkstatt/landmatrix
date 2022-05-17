import { test, expect } from "@playwright/test";

test("basic test", async ({ page }) => {
  await page.goto("/login", { waitUntil: "networkidle" });
  await page.fill('text=Username >> [placeholder="Username"]', "shakespeare");
  await page.fill('text=Password >> [placeholder="Password"]', "hamlet4eva");

  await page.click("text=Username Password Login >> button");
  await page.waitForLoadState("networkidle");

  const wrap = await page.locator(".login-wrapper");
  await expect(wrap).toHaveText("You are logged in.");
});
