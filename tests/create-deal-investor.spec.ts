import { test, expect } from "@playwright/test";
import { TIMEOUT } from "dns";
import { log } from "util";

test.use({ storageState: "playwright-storageState.json" });

test.describe.serial("deal creation tests", () => {
  let dealID;
  let saveButton;
  let investorID;
  let ParentID;
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
    const buttonCurrent = await page
      .locator('input[name="production_size_current"]')
      .first();
    await expect(buttonCurrent).toBeDisabled();

    //DecimalField
    let decimalField = await page.locator(`[name=intended_size]`);
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
    await page.locator(`[name=production_size]`).nth(1).fill("2000");
    //Datefield
    let datefield = await page.locator(`[name=production_size]`).first();

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

    await page.locator('input[name="production_size_current"]').first().check();
    // ToDo: Testing "+"button
    //Create 2nd DateAreaField

    await page.locator('button[name="plus_icon"]').nth(1).click();
    await page.locator('input[name="production_size"]').nth(2).fill("2019");
    await page.locator('input[name="production_size"]').nth(3).fill("3000");
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

    //Create 2nd DateAreaFarmersHouseholdField

    // Check input[name="contract_farming"] >> nth=1
    let radiobutton = await page.locator('input[name="contract_farming"]').nth(1);
    await radiobutton.check();
    await page.locator('input[name="on_the_lease_state"]').first().check();

    //DateAreaFarmersHouseholds
    let leaseField = await page.locator('input[name="on_the_lease"]');
    await leaseField.first().fill("2018-02-01");
    await leaseField.nth(1).fill("2000");
    await leaseField.nth(2).fill("5");
    await leaseField.nth(3).fill("10");
    await page.locator('input[name="on_the_lease_current"]').first().check();

    //INVESTOR INFO
    //Charfield
    await page.locator("text=Investor info").click();
    let charfield = await page.locator('input[name="project_name"]');
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

    //ADD CONTRACT
    await page.locator("text=Contracts").click();
    await page.locator("text=Add Contract").click();
    await page.locator('input[name="number"]').fill("1234");
    await page.locator('input[name="date"]').fill("2018-01-02");
    await page.locator('input[name="agreement_duration"]').fill("10");
    await page.locator("text=Add Contract").click();
    await expect((await page.locator("text=2. Contract").count()) === 1).toBeTruthy();
    await Promise.all([page.waitForNavigation(), saveButton.click()]);
    await expect((await page.locator("text=2. Contract").count()) === 0).toBeTruthy();

    //await page.locator("text=/1. Contract/ >> svg").first().click();
    //ToDo: Expect alert, but not showing in chromium-browser, playwright-docu: https://playwright.dev/docs/dialogs

    //ToDo: ADD FILE
    // https://playwright.dev/docs/input#upload-files
    //...

    //await Promise.all([page.waitForNavigation(), saveButton.click()]);

    // await expect(saveButton).toBeDisabled();

    //ToDo: needs fixing: wait for navigation line 156 not working, l175 returns innertext from before and after clicking the save-button
    await page.evaluate(() => {
      return new Promise((resolve) => setTimeout(resolve, 500));
    });

    let headline = await page.locator("h1");
    await expect(headline).toContainText("Editing deal #");
    dealID = (await headline.innerText()).replace("Editing deal #", "");
  });

  //CHECKOUT DEAL
  test("checkout new deal", async ({ context, page }) => {
    await page.goto(`deal/${dealID}`);
    await expect(await page.locator("h1")).toHaveText(`Deal #${dealID}`);

    await Promise.all([
      page.waitForNavigation(),
      await page.goto(`deal/${dealID}/#general`),
    ]);
    await expect(await page.locator('div[data-name="intended_size"]')).toContainText(
      "123,2"
    );
    const currentIntention = await page.locator("text=2 000").first();
    await expect(currentIntention).toContainText("[2018-02-01, current] 2 000 ha");
    await expect(currentIntention).toHaveClass("font-bold");
    // console.log(await currentIntention.count());

    await expect(page.locator('div[data-name="contract_farming"]')).toContainText("No");
    await page.goto(`deal/${dealID}/#contracts`);
    await expect(page.locator('div[data-name="number"]')).toContainText("1234");
  });

  //EDIT DEAL
  test("edit deal", async ({ context, page }) => {
    saveButton = page.locator("text=Save");

    await page.goto(`deal/${dealID}`);
    await Promise.all([
      page.waitForNavigation(),
      await page.locator('a:has-text("Edit")').click(),
    ]);
    await Promise.all([
      page.waitForNavigation(),
      await page.locator("text=General info").click(),
    ]);

    await page.locator('input[name="production_size_current"]').nth(1).check();
    await page.locator('input[name="production_size"]').nth(2).fill("2022");
    await page
      .locator('textarea[name="contract_farming_comment"]')
      .fill("Some comment");
    await page.locator('input[name="contract_farming"]').first().check();
    //await page.locator('input[name="on_the_lease_state"]').nth(1).check();

    //Add second contract:
    await page.locator("text=Contracts").click();
    await page.locator("text=Add Contract").click();
    await page.locator("text=2. Contract").click();

    await page.locator('input[name="number"]').fill("5678");
    await page.locator('input[name="date"]').fill("2022-01-02");
    await page.locator('input[name="agreement_duration"]').fill("20");

    await saveButton.click();

    //CHECKOUT DEAL CHANGES AFTER EDIT
    await Promise.all([
      page.waitForNavigation(),
      await page.goto(`deal/${dealID}/#general`),
    ]);
    const currentIntention = await page.locator("text=2 000").first();
    await expect(currentIntention).toHaveText("[2018-02-01] 2 000 ha ");
    await expect(currentIntention).toHaveClass("");

    const newCurrentIntention = await page.locator("text=3 000");
    await expect(newCurrentIntention).toHaveText("[2022, current] 3 000 ha ");
    await expect(newCurrentIntention).toHaveClass("font-bold");

    await expect(page.locator('div[data-name="contract_farming"]')).toHaveText("Yes");
    await expect(page.locator('div[data-name="contract_farming_comment"]')).toHaveText(
      "Some comment"
    );
    await page.goto(`deal/${dealID}/#contracts`);
    await expect(page.locator('div[data-name="number"]').first()).toContainText("1234");

    await expect(page.locator('div[data-name="number"]').nth(1)).toContainText("5678");
  });

  test("create investor", async ({ context, page }) => {
    await page.goto(`deal/${dealID}`);
    await Promise.all([
      page.waitForNavigation(),
      await page.locator('a:has-text("Edit")').click(),
    ]);

    //create Parent investor
    await page.locator("text=Investor info").click();
    const investorInput = page.locator('input[name="operating_company"]').first();
    await investorInput.click();
    await investorInput.fill("Parent Investor Test");
    await investorInput.press("Enter");
    //ToDo: select country
    //...
    await page.locator('select[name="classification"]').selectOption("GOVERNMENT");
    await page.locator('[placeholder="Investor homepage"]').click();
    await page
      .locator('[placeholder="Investor homepage"]')
      .fill("https://www.testing-parent-investor.de");
    await page.locator("#investor_info >> text=Save").click();
    ParentID = await page.locator("a[class=investor-link]").innerText();
    ParentID = ParentID.replace("Show details for investor #", "");
    ParentID = ParentID.replace(" Parent Investor Test", "");

    //create Child investor
    await investorInput.click();
    await investorInput.fill("Child Investor Test");
    await investorInput.press("Enter");
    //ToDo: select country
    //...

    await page.locator('select[name="classification"]').selectOption("GOVERNMENT");
    await page.locator('[placeholder="Investor homepage"]').click();
    await page
      .locator('[placeholder="Investor homepage"]')
      .fill("https://www.testing-child-investor.de");
    await page.locator("#investor_info >> text=Save").click();
    await page.locator("text=Save").first().click();
    investorID = await page.locator("a[class=investor-link]").innerText();
    investorID = investorID.replace("Show details for investor #", "");
    investorID = investorID.replace(" Child Investor Test", "");

    //checkout new Investor detail page
    // await page.locator("a[class=investor-link]").click();
    await page.goto(`/investor/${investorID}`);
    await expect(page.locator("h1")).toHaveText(`Child Investor Test #${investorID}`);
    await expect(page.locator("text=Government")).toBeVisible();
    await expect(
      page.locator('a:has-text("www.testing-child-investor.de")')
    ).toBeVisible();

    //add Parent Investor to Child Investor
    await page.locator('button:has-text("Edit")').click();
    await page.locator('button:has-text("Create a new draft")').click();
    await page.locator("text=Parent companies").click();
    await page.reload();
    await page.locator("text=Add Parent company").click();
    await page.locator('[placeholder="Investor"]').click();
    //await page.locator(`text=Parent Investor Test #${ParentID}`).click();
    await page.keyboard.press("ArrowDown");
    await page.keyboard.press("Enter");

    //add data source to Child Investor
    await page.locator("text=Data sources").click();
    await page.locator("text=Add Data source").click();
    await page.locator('select[name="type"]').selectOption("MEDIA_REPORT");
    await page.locator('[placeholder="Publication title"]').click();
    await page.locator('[placeholder="Publication title"]').fill("Publication Test");
    await page.locator('[placeholder="YYYY-MM-DD"]').click();
    await page.locator('[placeholder="YYYY-MM-DD"]').fill("2022-02-02");
    await page.locator('[placeholder="Name"]').click();
    await page.locator('[placeholder="Name"]').fill("William Shakespeare");
    await page.locator("text=Save").click();

    //checkout Investor Changes (WIP)
    await page.goto(`/investor/${investorID}`);
    await page.click('a:has-text("Involvements")');
    // await expect(page.locator("data-name=name").first()).toHaveText(
    //   "Parent Investor Test"
    // );
    await page.locator("text=Data sources").click();
    // await expect(page.locator("h3")).toContainText("1. Data source");
    // await expect(page.locator("text=2022-02-02")).toBeVisible();
  });

  test("delete investors", async ({ context, page }) => {
    await page.goto(`/investor/${investorID}`);
    await page.locator('button:has-text("Delete")').click();

    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .click();
    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .fill("delete Child Investor Test");
    await Promise.all([
      page.waitForNavigation(),
      page.locator('button:has-text("Delete investor version")').click(),
    ]);
    //delete Parent Investor
    await page.goto(`/investor/${ParentID}`);
    await page.locator('button:has-text("Delete")').click();

    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .click();
    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .fill("delete Parent Investor Test");
    await Promise.all([
      page.waitForNavigation(),
      page.locator('button:has-text("Delete investor version")').click(),
    ]);
  });

  //ToDo: needs fixing:
  // test("delete new deal", async ({ context, page }) => {
  //    await page.goto(`deal/${dealID}`);
  //   await page.pause();
  // });
});
