export const extractDealAndVersionId = (
  url: string
): [dealId: number, versionId: number] => {
  const pathname = new URL(url).pathname;
  return pathname.split("/").slice(-2).map(parseInt) as [number, number];
};
