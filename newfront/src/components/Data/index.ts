import { writable } from "svelte/store";

export const showFilterBar = writable(true);
export const publicOnly = writable(true);
export const isDefaultFilter = writable(true);
