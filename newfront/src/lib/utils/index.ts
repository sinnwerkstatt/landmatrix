import type { Deal } from "$lib/types/deal";
import type { Investor } from "$lib/types/investor";

type TableObj = Deal | Investor;

function dotresolve(path: string, obj: TableObj) {
  if (!path.includes(".")) return obj[path];
  return path.split(".").reduce(function (prev, curr) {
    return prev ? prev[curr] : null;
  }, obj);
}

export const sortFn =
  (sortley: string) =>
  (a: TableObj, b: TableObj): number => {
    const descending = sortley.startsWith("-");
    let x, y;
    // debugger;

    if (descending) {
      x = dotresolve(sortley.replace("-", ""), a);
      y = dotresolve(sortley.replace("-", ""), b);
    } else {
      y = dotresolve(sortley, a);
      x = dotresolve(sortley, b);
    }

    if (x === null || x === undefined) return 1;
    if (y === null || y === undefined) return 1;
    //
    // console.log(
    //   "comparison",
    //   x.toLocaleLowerCase(),
    //   " || ",
    //   y.toLocaleLowerCase(),
    //   " == ",
    //   x.toLocaleLowerCase().localeCompare(y.toLocaleLowerCase()),
    // );

    return x.toLocaleLowerCase().trim().localeCompare(y.toLocaleLowerCase().trim());
  };
