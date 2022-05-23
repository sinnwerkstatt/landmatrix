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
    await Promise.all([
      page.waitForNavigation(/*{ url: 'http://localhost:3000/deal/edit/9335/167851' }*/),
      page.locator('a:has-text("Edit")').click(),
    ]);

    await page.locator("text=General info").click();
    //const landArea = page.locator(".panel-body").first();
    // await page.locator('[placeholder="\\31 00\\.23"] >> nth=0').fill("2000");
    // await page.locator(".form-check").first().click();
    // await page.pause();
    // await page
    //   .locator(
    //     'text=Size under contract (leased or purchased area, in ha) CurrentDateArea (ha) ha >> [placeholder="YYYY-MM-DD"]'
    //   )
    //   .fill("2022");
    //
    // await page
    //   .locator(
    //     'text=Size under contract (leased or purchased area, in ha) CurrentDateArea (ha) ha >> [placeholder="YYYY-MM-DD"] >'
    //   )
    //   .press("Tab");
    // await page
    //   .locator(
    //     'text=Size under contract (leased or purchased area, in ha) CurrentDateArea (ha) ha >> [placeholder="\\31 00\\.23"]'
    //   )
    //   .fill("1500");
    // await page.pause();
    // await page
    //   .locator(
    //     'text=Size in operation (production, in ha) CurrentDateArea (ha) ha >> [placeholder="YYYY-MM-DD"]'
    //   )
    //   .press("Tab");
    // await page
    //   .locator(
    //     'text=Size in operation (production, in ha) CurrentDateArea (ha) ha >> [placeholder="\\31 00\\.23"]'
    //   )
    //   .nth(2)
    //   .fill("1000");
    // await page.locator('input[name="intention_of_investment_current"]').check();
    // await page
    //   .locator(
    //     'text=ha Select option Biofuels Food crops Fodder Livestock Non-food agricultural comm >> [placeholder="YYYY-MM-DD"]'
    //   )
    //   .click();
    // await page.locator('select[name="nature_of_deal"]').click();
    // await page.locator('select[name="nature_of_deal"]').click();
    // await saveButton.click();
    // await expect(saveButton).toBeDisabled();
    // await page.pause();
  });
});
