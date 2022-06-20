import { test, expect } from "@playwright/test";
import { TIMEOUT } from "dns";
import { log } from "util";

test.use({ storageState: "playwright-storageState.json" });

test.describe.serial("deal creation tests", () => {
  let dealID;
  let saveButton;
  test("create new deal", async ({ context, page }) => {
    await page.goto("/deal/add/");
    saveButton = page.locator("text=Save");

    //Location
    // await page.locator(".chevron").click();
    // await page.locator("text=Albania").nth(1).click();
    // await page.locator("text=Add Location").click();
    // await page.locator('[placeholder="Location"]').click();
    // await page.locator('[placeholder="Location"]').fill("Belsh");
    // await page.locator("text=Save").click();

    //GENERAL
    await page.locator("text=General info").click();

    //DecimalField
    let decimalField = await page.locator(
      'text=Intended size (in ha) ha >> [placeholder="\\31 23\\.45"]'
    );
    await decimalField.fill("123.203498512903402342347");
    await expect(
      await decimalField.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.stepMismatch
      )
    ).toBeTruthy();
    await decimalField.fill("-123");
    await expect(
      await decimalField.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.rangeUnderflow
      )
    ).toBeTruthy();

    await decimalField.fill("123.20");
    await expect(
      await decimalField.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    //Datefield
    let datefield = await page.locator(
      'text=Size under contract (leased or purchased area, in ha) Current Date Area (ha) ha >> [placeholder="YYYY-MM-DD"]'
    );
    await datefield.fill("01.02.2018");

    await expect(
      await datefield.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.customError
      )
    ).toBeTruthy();
    await datefield.fill("01/02/2018");
    await expect(
      await datefield.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.customError
      )
    ).toBeTruthy();

    await datefield.fill("2018");
    await expect(
      await datefield.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    await datefield.fill("2018-02-01");
    await expect(
      await datefield.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    //ChoiceField
    // let choiceField = await page.locator(
    //   'text=Purchase price Purchase price Purchase price currency Purchase price area type N >> [placeholder="Currency"]'
    // );
    //
    // await choiceField.fill("USD");
    // await page.locator("text=US Dollar (USD)").nth(1).click();
    //
    // await expect(
    //   await choiceField.evaluate((x: HTMLInputElement) => x.validity.valid)
    // ).toBeTruthy();
    //

    //DecimalField Farmers
    let farmers = await page
      .locator(
        'text=On leased area/farmers/households Current Date Area (ha) Farmers Households ha >> input[type="number"]'
      )
      .nth(1);
    await farmers.fill("-4");
    await expect(
      await farmers.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeFalsy();
    await farmers.fill("5.45");
    await expect(
      await farmers.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeFalsy();
    await farmers.fill("5");
    await expect(
      await farmers.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    //Contracts

    await page.pause();
  });
});
