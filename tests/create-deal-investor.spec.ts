import { createInvestorName } from "./utils";
import { test, expect } from "@playwright/test";

test.use({ storageState: "tests/storageState/admin.json" });

test.describe.serial("deal creation tests", () => {
  let dealID;
  let saveButton;
  let investorID;
  let ParentID;

  let investorChildName = createInvestorName();
  let investorParentName = createInvestorName();

  test("create new deal", async ({ context, page }) => {
    await page.goto("/deal/add/");
    saveButton = page.locator("text=Save").nth(0);

    //LOCATION
    await page.locator('[placeholder="Country"]').fill("Albania");

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

    //Create 2nd DateAreaField
    await page.locator('button[name="plus_icon"]').nth(1).click();
    await page.locator('input[name="production_size"]').nth(2).fill("2019");
    await page.locator('input[name="production_size"]').nth(3).fill("3000");
    //ToDo: Purchase price
    //await page.locator('input["name=purchase_price"]').fill("2345.60");
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
    //ChoiceField
    await choiceField.fill("USD");
    await expect(
      await choiceField.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    //Create 2nd FarmersHouseholdField
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

    //INVESTOR INFO
    //Charfield
    await page.locator("text=Investor info").click();
    let charfield = await page.locator('input[name="project_name"]');
    await charfield.fill(
      "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata123456789"
    );
    await charfield.evaluate((x: HTMLInputElement) => console.log(x.validity));
    //check max-length
    await expect(charfield).toHaveValue(
      "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata"
    );
    await expect(
      await charfield.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    //DATA SOURCES FILE UPLOAD
    await page.locator("text=Data sources").click();
    await page.locator("text=Add Data source").click();
    const upload = await page.locator('input[type="file"]');
    let [fileChooser1] = await Promise.all([
      page.waitForEvent("filechooser"),
      upload.click(),
    ]);
    await fileChooser1.setFiles("tests/testFile.pdf");
    await page.locator('input[type="file"]').setInputFiles("tests/testFile.pdf");
    await saveButton.click();
    await expect(page.locator("button:has-text('Remove this file')")).toBeVisible();

    //get DealID
    await page.waitForSelector("h1");
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
    await expect(page.locator('div[data-name="contract_farming"]')).toContainText("No");
    await page.goto(`deal/${dealID}/#contracts`);
    await expect(page.locator('div[data-name="number"]')).toContainText("1234");

    await page.locator("text=Data sources").click();
    await expect(page.locator("h3:has-text('1. Data source')")).toBeVisible();
    const [newPage] = await Promise.all([
      context.waitForEvent("page"),
      await page.locator("svg").nth(-3).click(),
    ]);
    const response = await page.goto(newPage.url());
    expect(response.ok()).toBeTruthy();
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
    await investorInput.fill(`${investorParentName}`);
    await investorInput.press("Enter");
    await page.click("[placeholder" + '="Country"]');
    await page.click("text=Albania");

    await page.locator('select[name="classification"]').selectOption("GOVERNMENT");
    await page.locator('[placeholder="Investor homepage"]').click();
    await page
      .locator('[placeholder="Investor homepage"]')
      .fill("https://www.testing-parent-investor.de");
    await page.locator("#investor_info >> text=Save").click();
    ParentID = await page.locator("a[class=investor-link]").innerText();
    ParentID = ParentID.replace("Show details for investor #", "");
    ParentID = ParentID.replace(` ${investorParentName}`, "");

    //create Child investor
    await investorInput.click();
    await investorInput.fill(`${investorChildName}`);
    await investorInput.press("Enter");
    await page.click("[placeholder" + '="Country"]');
    await page.click("text=Albania");
    await page.locator('select[name="classification"]').selectOption("GOVERNMENT");
    await page.locator('[placeholder="Investor homepage"]').click();
    await page
      .locator('[placeholder="Investor homepage"]')
      .fill("https://www.testing-child-investor.de");
    await page.locator("#investor_info >> text=Save").click();
    await page.locator("text=Save").first().click();
    investorID = await page.locator("a[class=investor-link]").innerText();
    investorID = investorID.replace("Show details for investor #", "");
    investorID = investorID.replace(` ${investorChildName}`, "");

    //checkout new Investor detail page
    // await page.locator("a[class=investor-link]").click();
    await page.goto(`/investor/${investorID}`);
    await expect(page.locator("h1")).toHaveText(`${investorChildName} #${investorID}`);
    await expect(page.locator("text=Government")).toBeVisible();
    await expect(
      page.locator('a:has-text("www.testing-child-investor.de")')
    ).toBeVisible();
    await expect(page.locator("text=Albania")).toBeVisible();
    //add Parent Investor to Child Investor
    await page.locator('button:has-text("Edit")').click();
    await page.locator('button:has-text("Create a new draft")').click();
    await page.locator("text=Parent companies").click();
    await page.reload();
    await page.locator("text=Add Parent company").click();
    await page.locator('[placeholder="Investor"]').click();
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
    const upload = await page.locator('input[type="file"]');
    let [fileChooser1] = await Promise.all([
      page.waitForEvent("filechooser"),
      upload.click(),
    ]);
    await fileChooser1.setFiles("tests/testFile.pdf");
    await page.locator('input[type="file"]').setInputFiles("tests/testFile.pdf");
    await page.locator("text=Save").click();
    //add tertiary investor
    await page.click("text=Tertiary investors/lenders");
    await page.click("text=Tertiary investors/lenders");
    await page.click("text=Add Tertiary investor/lender");
    await page.click("text=1. Tertiary investor/lender");
    await page.click('[placeholder="Investor"]');
    await page.keyboard.press("ArrowDown");
    await page.keyboard.press("Enter");
    await page.locator("text=Save").click();
    //checkout Investor Changes (WIP)
    await page.goto(`/investor/${investorID}`);
    await page.locator("text=Data sources").click();
    await expect(page.locator("text=Media report")).toBeVisible;
    await expect(page.locator("text=Publication Test")).toBeVisible;
    await page.click('a:has-text("Involvements")');
    await expect(page.locator('td:has-text("Parent company")')).toBeVisible();
    await expect(page.locator('td:has-text("Tertiary investor/lender")')).toBeVisible();
    await page.locator("text=Data sources").click();
    //await page.locator("text=testFile_[A-Za-z0-9]{7}\\.pdf").first().click();
    const [newPage] = await Promise.all([
      context.waitForEvent("page"),
      await page.locator("svg").nth(-3).click(),
    ]);
    const response = await page.goto(newPage.url());
    expect(response.ok()).toBeTruthy();
  });

  //delete investors
  test("delete all deals and investors", async ({ context, page }) => {
    await page.goto(`/investor/${investorID}`);
    await page.locator('button:has-text("Remove")').click();
    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .fill("Delete Child investor");
    await page.click('button:has-text("Remove investor version")');
    //delete Parent Investor
    await page.goto(`/investor/${ParentID}`);
    await page.locator('button:has-text("Remove")').click();
    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .fill("delete Parent investor");
    await page.click('button:has-text("Remove investor version")');
    await page.goto(`/deal/${dealID}`);
    await page.locator('button:has-text("Remove")').click();
    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .fill("Remove deal version");
    await page.click('button:has-text("Remove deal version")');
    await expect(page.locator("h1")).toContainText("Deal not found");
  });
});
