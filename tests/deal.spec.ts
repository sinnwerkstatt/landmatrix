import { test, expect } from "@playwright/test";

test.use({ storageState: "playwright-storageState.json" });

test.describe.serial("deal creation tests", () => {
  let dealID;
  let saveButton;
  test("create new deal", async ({ context, page }) => {
    await page.goto("/deal/add/");
    await page
      .locator(
        "text=Select option Afghanistan Åland Islands Albania Algeria American Samoa Angola An >> div"
      )
      .nth(1)
      .click();
    await page.locator('[placeholder="Select option"]').fill("Mex");
    await page.locator('span:has-text("Mexico")').first().click();
    await page.locator("text=Add location").click();
    await page.locator('select[name="level_of_accuracy"]').selectOption("COUNTRY");
    await page.locator('[placeholder="Location"]').click();
    await page.locator('[placeholder="Location"]').fill("");
    await page.locator(".leaflet-buttons-control-button").first().click();
    await page
      .locator(
        "text=Click to place marker+−CancelFinishFinishFinishFinishLeaflet | Maps © Thunderfor"
      )
      .click();
    await page.locator(".leaflet-marker-icon").click();
    await page.locator(".leaflet-buttons-control-button").first().click();
    await page.locator(".leaflet-marker-icon").click();
    await page.locator('[placeholder="Location"]').click();
    await page.locator('[placeholder="Location"]').fill("Chiapas");
    await page.locator('[placeholder="Description"]').click();
    await page.locator('[placeholder="Description"]').fill("coffee plantation");
    await page.locator('[placeholder="Description"]').press("Tab");
    await page.locator('[placeholder="Facility name"]').fill("Mexican Coffee Comp");
    await Promise.all([
      page.waitForNavigation(/*{ url: 'http://localhost:3000/deal/edit/9324/167840' }*/),
      page.locator("text=Save").click(),
    ]);

    saveButton = page.locator("text=Save");
    await expect(saveButton).toBeDisabled();

    const headline = await page.locator("h1");
    dealID = (await headline.innerText()).replace("Editing Deal #", "");
    dealID = dealID.replace(" in Mexico", "");
  });

  test("edit new deal", async ({ context, page }) => {
    await page.goto(`deal/${dealID}`);
    await page.locator("text=Mexican Coffee Comp");
    await page.locator('a:has-text("Edit")').click();
    // await Promise.all([
    await page.waitForNavigation();
    // ]);

    await page.locator("text=General info").click();
    const landArea = page.locator(".panel-body").first();
    await page.locator("input[name='intended_size']").fill("2000");
    await page.pause();
  });
});
