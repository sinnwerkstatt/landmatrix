import type { Country, Region } from "$lib/types/wagtail"

interface Group {
  id: number
  name: string
}

export enum UserRole {
  ANYBODY,
  REPORTER,
  EDITOR,
  ADMINISTRATOR,
}

export interface User {
  id: number
  username: string
  first_name: string
  last_name: string
  full_name: string
  email: string
  is_active: boolean
  is_authenticated: boolean
  is_impersonate: boolean
  is_superuser: boolean
  date_joined: Date
  country: Country
  region: Region
  groups?: Group[]
  role: UserRole
}
