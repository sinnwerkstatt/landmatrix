export const extractDealAndVersionId = (
  url: string
): [dealId: number, versionId: number] => {
  const pathname = new URL(url).pathname;
  return pathname.split("/").slice(-2).map(parseInt) as [number, number];
};

export const createInvestorName = (length = 10): string => {
  return Math.random().toString(16).substr(2, length);
};
