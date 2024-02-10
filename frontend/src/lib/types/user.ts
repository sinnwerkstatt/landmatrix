export enum UserRole {
  ANYBODY = 0,
  REPORTER = 1,
  EDITOR = 2,
  ADMINISTRATOR = 3,
}

export interface User {
  id: number
  username: string
  first_name: string
  last_name: string
  full_name: string
  email: string
  phone: string
  information: string
  is_authenticated: boolean
  is_impersonate: boolean
  is_superuser: boolean
  is_staff: boolean
  is_active: boolean
  last_login: Date
  date_joined: Date
  country_id: number | null
  region_id: number | null
  role: UserRole
}
