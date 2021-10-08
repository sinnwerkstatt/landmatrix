interface UserRegInfo {
  country: unknown;
  region: unknown;
}
interface Group {
  id: number;
  name: string;
}

export type User = {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  initials: string;
  email: string;
  is_active: boolean;
  is_authenticated: boolean;
  is_staff: boolean;
  is_impersonate: boolean;
  date_joined: Date;
  userregionalinfo?: UserRegInfo;
  groups?: Group[];
  // role: UserRole
};
