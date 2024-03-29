import { negotiation_status_choices } from "$utils/choices";
import type { Deal } from "$types/deal";

export function sum(items: Deal[], prop: string): number {
  return items.reduce(function (a, b) {
    return a + b[prop];
  }, 0);
}

export function custom_is_null(field: unknown): boolean {
  return (
    field === undefined ||
    field === null ||
    field === "" ||
    (Array.isArray(field) && field.length === 0)
  );
}

export function prepareNegotianStatusData(deals: Deal[]): Array<unknown> {
  const stati = ["Intended", "Concluded", "Failed"];
  const colors = ["rgba(252,148,31,0.4)", "rgba(252,148,31,1)", "#7D4A0F"];
  const data = [];

  if (deals.length) {
    for (const [i, status] of stati.entries()) {
      const filteredDeals = deals.filter((d) => {
        return Object.keys(negotiation_status_choices[status]).includes(
          d.current_negotiation_status
        );
      });
      data.push({
        label: status,
        count: filteredDeals.length,
        size: sum(filteredDeals, "deal_size"),
        color: colors[i],
      });
    }
  }
  return data;
}
