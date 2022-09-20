import { expect } from "@playwright/test";

export const extractDealAndVersionId = (
  url: string
): [dealId: number, versionId: number] => {
  const pathname = new URL(url).pathname;
  return pathname.split("/").slice(-2).map(parseInt) as [number, number];
};

export const createInvestorName = (length = 10): string => {
  return Math.random().toString(16).substr(2, length);
};

export async function verifyPDF(page) {
  const regexFilename = new RegExp("testFile_[A-Za-z0-9]{7}.pdf");
  const pdfLink = await page
    .locator(`text=${regexFilename}`)
    .first()
    .getAttribute("href");
  console.log(pdfLink);
  const response = await page.goto(pdfLink);
  expect(response.ok()).toBeTruthy();
  await page.goBack();
}
