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

declare module "svelte-chartjs?client" {
  import * as svelte_chartjs from "svelte-chartjs";
  export = svelte_chartjs;
}

declare module "chart.js?client" {
  import * as chartjs from "chart.js";
  export = chartjs;
}

declare module "@googlemaps/js-api-loader?client" {
  import * as L from "@googlemaps/js-api-loader";
  export = L;
}

// fallback
declare module "*?client";
declare module "*?server";
