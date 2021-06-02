interface UserRegInfo {
  country: object;
  region: object;
}
interface Group {
  id: number;
  name: string;
}
export interface User {
  full_name: string;
  username: string;
  is_authenticated: boolean;
  is_impersonate: boolean;
  userregionalinfo?: UserRegInfo;
  groups?: Array<Group>;
}
