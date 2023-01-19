import type { Country, Region } from "$types/wagtail";

interface Group {
  id: number;
  name: string;
}

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  is_active: boolean;
  is_authenticated: boolean;
  is_staff: boolean;
  is_impersonate: boolean;
  date_joined: Date;
  country: Country;
  region: Region;
  groups?: Group[];
  role: number;
}
