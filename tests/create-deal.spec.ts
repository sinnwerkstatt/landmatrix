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

    //LOCATION
    await page.locator('[placeholder="Country"]').fill("Albania");
    // await page.locator("text=Add Location").click();
    // await page.locator('[placeholder="Location"]').click();
    // await page.locator('[placeholder="Location"]').fill("Belsh");

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

    //DateAreaField
    //Radiobutton

    //Area
    await page
      .locator(
        'text=Size under contract (leased or purchased area, in ha) Current Date Area (ha) ha >> [placeholder="\\31 23\\.45"]'
      )
      .click();
    await page
      .locator(
        'text=Size under contract (leased or purchased area, in ha) Current Date Area (ha) ha >> [placeholder="\\31 23\\.45"]'
      )
      .fill("2000");

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

    await page.locator('input[name="contract_size_current"]').first().check();

    //Create 2nd DateAreaField
    await page
      .locator(
        "text=Size under contract (leased or purchased area, in ha) Current Date Area (ha) ha >> button"
      )
      .first()
      .click();
    await page.locator('text=ha ha >> [placeholder="YYYY-MM-DD"]').nth(1).click();
    await page.locator('text=ha ha >> [placeholder="YYYY-MM-DD"]').nth(1).fill("2019");
    await page.locator('text=ha ha >> [placeholder="YYYY-MM-DD"]').nth(1).press("Tab");
    await page
      .locator('text=ha ha >> [placeholder="\\31 23\\.45"]')
      .nth(1)
      .fill("3000");

    //Purchase price
    // await page.locator('input [placeholder="\\31 23\\.45"]').nth(4).click();
    //ChoiceField Charfield
    let choiceField_Charfield = await page.locator(
      'select[name="purchase_price_type"]'
    );
    choiceField_Charfield.selectOption("PER_HA");
    // Click div:has-text("Adding new deal Save Cancel Locations General info Contracts Employment Investor") >> nth=1
    await expect(
      await choiceField_Charfield.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    //ChoiceField ForeignKey
    let choiceField = await page.locator(
      'text=Purchase price Purchase price Purchase price currency Purchase price area type N >> [placeholder="Currency"]'
    );

    await choiceField.fill("USD");
    await page.locator("text=US Dollar (USD)").nth(1).click();

    //DateAreaFarmersHouseholds
    await page
      .locator(
        'text=On leased area/farmers/households Current Date Area (ha) Farmers Households ha >> [placeholder="YYYY-MM-DD"]'
      )
      .click();
    await page
      .locator(
        'text=On leased area/farmers/households Current Date Area (ha) Farmers Households ha >> [placeholder="YYYY-MM-DD"]'
      )
      .fill("2018-02-01");
    await page
      .locator(
        'text=On leased area/farmers/households Current Date Area (ha) Farmers Households ha >> [placeholder="YYYY-MM-DD"]'
      )
      .press("Tab");
    await page
      .locator(
        'text=On leased area/farmers/households Current Date Area (ha) Farmers Households ha >> [placeholder="\\31 23\\.45"]'
      )
      .fill("2000");
    await page
      .locator(
        "text=On leased area/farmers/households Current Date Area (ha) Farmers Households ha >> button"
      )
      .first()
      .click();
    await page
      .locator(
        'text=On leased area/farmers/households Current Date Area (ha) Farmers Households ha >> input[type="number"]'
      )
      .nth(2)
      .fill("10");

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

    // Check input[name="contract_farming"] >> nth=1
    let radiobutton = await page.locator('input[name="contract_farming"]').nth(1);
    await radiobutton.check();
    await page.locator('input[name="on_the_lease_state"]').first().check();
    await page.locator('input[name="on_the_lease_current"]').first().check();

    //Create 2nd DateAreaFarmersHouseholdField
    await page
      .locator(
        'text=Current Date Area (ha) Farmers Households ha ha >> [placeholder="YYYY-MM-DD"]'
      )
      .nth(1)
      .click();
    await page
      .locator(
        'text=Current Date Area (ha) Farmers Households ha ha >> [placeholder="YYYY-MM-DD"]'
      )
      .nth(1)
      .fill("2019");
    await page
      .locator(
        'text=Current Date Area (ha) Farmers Households ha ha >> [placeholder="YYYY-MM-DD"]'
      )
      .nth(1)
      .press("Tab");
    await page
      .locator(
        'text=Current Date Area (ha) Farmers Households ha ha >> [placeholder="\\31 23\\.45"]'
      )
      .nth(1)
      .fill("1000");
    await page
      .locator(
        'text=Current Date Area (ha) Farmers Households ha ha >> [placeholder="\\31 23\\.45"]'
      )
      .nth(1)
      .press("Tab");

    //INVESTOR INFO
    //Charfield
    await page.locator("text=Investor info").click();
    let charfield = await page.locator('[placeholder="Name of investment project"]');
    await charfield.fill(
      "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata123456789"
    );
    await charfield.evaluate((x: HTMLInputElement) => console.log(x.validity));
    await expect(charfield).toHaveValue(
      "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata"
    );
    await expect(
      await charfield.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    await Promise.all([page.waitForNavigation(), saveButton.click()]);

    // await expect(saveButton).toBeDisabled();
    // await page.waitForNavigation();

    let headline = await page.locator("h1");

    dealID = (await headline.innerText()).replace("Editing Deal #", "");

    await page.goto(`deal/${dealID}`);

    //CHECKOUT DEAL
    await expect(await page.locator("h1")).toHaveText(`Deal #${dealID}`);

    await Promise.all([
      page.waitForNavigation(),
      await page.goto(`deal/${dealID}/#general`),
    ]);

    const currentIntention = await page.locator("text=2 000");
    await expect(currentIntention).toHaveText("[2018-02-01, current] 2 000 ha ");
    await expect(currentIntention).toHaveClass("font-bold");
    // console.log(await currentIntention.count());

    let contractFarming = page.locator(".test", {
      has: page.locator("text=Contract farming"),
    });
    await expect(contractFarming).toHaveText(/No/);

    //EDIT DEAL
    await Promise.all([
      page.waitForNavigation(),
      await page.locator('a:has-text("Edit")').click(),
    ]);
    await Promise.all([
      page.waitForNavigation(),
      await page.locator("text=General info").click(),
    ]);

    await page.locator('input[name="contract_size_current"]').nth(1).check();
    await page
      .locator('text=Current Date Area (ha) ha ha >> [placeholder="YYYY-MM-DD"]')
      .nth(1)
      .fill("2022");
    await page
      .locator('textarea[name="contract_farming_comment"]')
      .fill("Some comment");
    await page.locator('input[name="contract_farming"]').first().check();
    //await page.locator('input[name="on_the_lease_state"]').nth(1).check();
    await saveButton.click();

    //CHECKOUT DEAL CHANGES AFTER EDIT
    await Promise.all([
      page.waitForNavigation(),
      await page.goto(`deal/${dealID}/#general`),
    ]);

    await expect(currentIntention).toHaveText("[2018-02-01] 2 000 ha ");
    await expect(currentIntention).toHaveClass("");

    const newCurrentIntention = await page.locator("text=3 000");
    await expect(newCurrentIntention).toHaveText("[2022, current] 3 000 ha ");
    await expect(newCurrentIntention).toHaveClass("font-bold");

    await expect(contractFarming.first()).toHaveText(/Yes/);
    await expect(contractFarming.nth(1)).toHaveText(/Some comment/);

    await page.pause();
  });
});
