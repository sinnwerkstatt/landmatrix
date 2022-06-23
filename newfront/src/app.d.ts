/// <reference types="@sveltejs/kit" />

declare namespace App {
  interface Locals {
    cookie?: string;
  }
  // interface Platform {}
  interface Session {
    cookie?: string;
  }
  interface Stuff {
    user: import("$lib/types/user").User;
    secureApolloClient: import("$lib/types/custom").SecureApolloClient;
  }
}
