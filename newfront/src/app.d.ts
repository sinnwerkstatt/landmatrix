/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#the-app-namespace
// for information about these interfaces
declare namespace App {
  interface Locals {
    cookie?: string;
  }
  // interface Platform {}
  interface Session {
    cookie?: string;
  }
  // interface Stuff {}
}

declare module "leaflet?client" {
  import * as L from "leaflet";
  export = L;
}

declare module "leaflet-gesture-handling?client" {
  import * as LGH from "leaflet-gesture-handling";
  export = LGH;
}
