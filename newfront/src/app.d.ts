/// <reference types="@sveltejs/kit" />
import type { User } from "./lib/types/user";

declare namespace App {
  interface Locals {
    cookie?: string;
  }
  // interface Platform {}
  interface Session {
    cookie?: string;
  }
  interface Stuff {
    user?: User;
  }
}

declare module "leaflet?client" {
  import * as L from "leaflet";
  export = L;
}

declare module "leaflet-gesture-handling?client" {
  import * as LGH from "leaflet-gesture-handling";
  export = LGH;
}
