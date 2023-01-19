import { createInvestorName, verifyPDF } from "./utils";
import { test, expect } from "@playwright/test";

test.use({ storageState: "tests/storageState/admin.json" });

test.describe.serial("deal creation tests", () => {
  let dealID;
  let investorID;
  let ParentID;

  let investorChildName = createInvestorName();
  let investorParentName = createInvestorName();

  test("create new deal", async ({ page }) => {
    await page.goto("/deal/add/");

    // LOCATION
    await page.locator('[placeholder="Country"]').fill("Albania");

    // GENERAL
    await page.locator("text=General info").click();
    await expect(
      page.locator('input[name="production_size_current"]').first()
    ).toBeDisabled();

    // DecimalField
    const decimalField = page.locator(`[name=intended_size]`);
    await decimalField.fill("123.203498512903402342347");
    expect(
      decimalField.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.stepMismatch
      )
    ).toBeTruthy();
    await decimalField.fill("-123");
    expect(
      decimalField.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.rangeUnderflow
      )
    ).toBeTruthy();

    await decimalField.fill("123.20");
    expect(
      decimalField.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    // Area
    await page.locator(`[name=production_size]`).nth(1).fill("2000");

    // DateField
    const dateField = page.locator(`[name=production_size]`).first();
    await dateField.fill("01.02.2018");
    expect(
      dateField.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.customError
      )
    ).toBeTruthy();
    await dateField.fill("01/02/2018");
    expect(
      dateField.evaluate(
        (x: HTMLInputElement) => !x.validity.valid && x.validity.customError
      )
    ).toBeTruthy();
    await dateField.fill("2018");
    expect(dateField.evaluate((x: HTMLInputElement) => x.validity.valid)).toBeTruthy();
    await dateField.fill("2018-02-01");
    expect(dateField.evaluate((x: HTMLInputElement) => x.validity.valid)).toBeTruthy();
    await page.locator('input[name="production_size_current"]').first().check();

    // Create 2nd DateAreaField
    await page.locator('button[name="plus_icon"]').nth(1).click();
    await page.locator('input[name="production_size"]').nth(2).fill("2019");
    await page.locator('input[name="production_size"]').nth(3).fill("3000");

    // CharChoiceField
    const charChoiceField = page.locator('select[name="purchase_price_type"]');
    await charChoiceField.selectOption("PER_HA");
    expect(
      charChoiceField.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    // ChoiceField ForeignKey
    const choiceField = page.locator(
      'text=Purchase price Purchase price Purchase price currency Purchase price area type N >> [placeholder="Currency"]'
    );
    // ChoiceField
    await choiceField.fill("USD");
    expect(
      choiceField.evaluate((x: HTMLInputElement) => x.validity.valid)
    ).toBeTruthy();

    // Create 2nd FarmersHouseholdField
    await page.locator('input[name="contract_farming"]').nth(0).check();
    await page.locator('input[name="on_the_lease_state"]').nth(0).check();

    // DateAreaFarmersHouseholds
    const leaseField = page.locator('input[name="on_the_lease"]');
    await leaseField.first().fill("2018-02-01");
    await leaseField.nth(1).fill("2000");
    await leaseField.nth(2).fill("5");
    await leaseField.nth(3).fill("10");
    await page.locator('input[name="on_the_lease_current"]').first().check();

    // ADD CONTRACT
    await page.locator("text=Contracts").click();
    await page.locator("text=Add Contract").click();
    await page.locator('input[name="number"]').fill("1234");
    await page.locator('input[name="date"]').fill("2018-01-02");
    await page.locator('input[name="agreement_duration"]').fill("10");
    await page.locator("text=Add Contract").click();
    await expect(page.locator("text=2. Contract")).toHaveCount(1);

    await page.locator("text=Save").click();

    await expect(page.locator("text=2. Contract")).toHaveCount(0);

    // INVESTOR INFO
    // CharField
    await page.locator("text=Investor info").click();
    const charField = page.locator('input[name="project_name"]');
    await charField.fill(
      "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata123456789"
    );
    await expect(charField).toHaveValue(
      "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata"
    );
    expect(charField.evaluate((x: HTMLInputElement) => x.validity.valid)).toBeTruthy();

    //DATA SOURCES FILE UPLOAD
    await page.locator("text=Data sources").click();
    await page.locator("text=Add Data source").click();
    const [fileChooser] = await Promise.all([
      page.waitForEvent("filechooser"),
      page.locator('input[type="file"]').click(),
    ]);
    await fileChooser.setFiles("tests/testFile.pdf");
    await page.locator('input[type="file"]').setInputFiles("tests/testFile.pdf");
    await page.locator("text=Save").click();
    await expect(page.locator("button:has-text('Remove this file')")).toBeVisible();

    //get DealID
    const headline = page.locator("h1");
    await expect(headline).toContainText("Editing deal #");
    dealID = (await headline.innerText()).replace("Editing deal #", "");
  });

  //CHECKOUT DEAL
  test("checkout new deal", async ({ page }) => {
    await page.goto(`deal/${dealID}`);
    await expect(page.locator("h1")).toHaveText(`Deal #${dealID}`);

    await page.locator("text=General info").click();
    await expect(page.locator('div[data-name="intended_size"]')).toContainText("123,2");

    const currentIntention = page.locator("text=2 000").first();
    await expect(currentIntention).toContainText("[2018-02-01, current] 2 000 ha");
    await expect(currentIntention).toHaveClass("font-bold");

    await expect(page.locator('div[data-name="contract_farming"]')).toContainText(
      "Yes"
    );

    await page.locator("text=Contracts").click();
    await expect(page.locator('div[data-name="number"]')).toContainText("1234");

    await page.locator("text=Data sources").click();
    await expect(page.locator("h3:has-text('1. Data source')")).toBeVisible();
    //await verifyPDF(page);
  });

  //EDIT DEAL
  test("edit deal", async ({ page }) => {
    const saveButton = page.locator("text=Save");

    await page.goto(`deal/${dealID}`);
    await page.locator('a:has-text("Edit")').click();
    await page.locator("text=General info").click();

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
    await page.goto(`deal/${dealID}`);
    await page.locator("text=General info").click();

    const currentIntention = page.locator("text=2 000").first();
    await expect(currentIntention).toHaveText("[2018-02-01] 2 000 ha ");
    await expect(currentIntention).toHaveClass("");

    const newCurrentIntention = page.locator("text=3 000");
    await expect(newCurrentIntention).toHaveText("[2022, current] 3 000 ha ");
    await expect(newCurrentIntention).toHaveClass("font-bold");

    await expect(page.locator('div[data-name="contract_farming"]')).toHaveText("Yes");
    await expect(page.locator('div[data-name="contract_farming_comment"]')).toHaveText(
      "Some comment"
    );

    await page.locator("text=Contracts").click();
    await expect(page.locator('div[data-name="number"]').first()).toContainText("1234");
    await expect(page.locator('div[data-name="number"]').nth(1)).toContainText("5678");
  });

  test("create investor", async ({ page }) => {
    await page.goto(`deal/${dealID}`);

    await page.locator('a:has-text("Edit")').click();

    //create Parent investor
    await page.locator("text=Investor info").click();
    const investorInput = page.locator('input[name="operating_company"]').first();
    await investorInput.click();
    await investorInput.fill(`${investorParentName}`);
    await investorInput.press("Enter");
    await page.click('[placeholder="Country"]');
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
    await page.click('[placeholder="Country"]');
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
    const [fileChooser] = await Promise.all([
      page.waitForEvent("filechooser"),
      page.locator('input[type="file"]').click(),
    ]);
    await fileChooser.setFiles("tests/testFile.pdf");
    await page.locator('input[type="file"]').setInputFiles("tests/testFile.pdf");
    await page.locator("text=Save").click();

    //add tertiary investor
    await page.click("text=Tertiary investors/lenders");
    await page.click("text=Tertiary investors/lenders");
    await page.locator("button").last().click();
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
    await verifyPDF(page);
  });

  //delete investors
  test("delete all deals and investors", async ({ page }) => {
    await page.goto(`/investor/${investorID}`);
    await page.locator('button:has-text("Remove")').click();
    await page
      .locator("text=Please provide a comment explaining your request >> textarea")
      .fill("Delete Child investor");
    await page.click('button:has-text("Remove investor version")');

    //delete Parent Investor
    await page.goto(`/investor/${ParentID}`);
    await page.click('button:has-text("Remove")');
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
