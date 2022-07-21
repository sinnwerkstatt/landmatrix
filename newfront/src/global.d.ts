// global.d.ts (or any ambient dts file)

// named exports
declare module "leaflet?client" {
  import * as L from "leaflet";
  export = L;
}

declare module "leaflet-gesture-handling?client" {
  import * as LGH from "leaflet-gesture-handling";
  export = LGH;
}

// fallback
declare module "*?client";
declare module "*?server";
