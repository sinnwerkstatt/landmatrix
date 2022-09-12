import type { Country, Region } from "$lib/types/wagtail"

interface Group {
  id: number
  name: string
}

export enum UserLevel {
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
  initials: string
  email: string
  is_active: boolean
  is_authenticated: boolean
  is_staff: boolean
  is_impersonate: boolean
  date_joined: Date
  country: Country
  region: Region
  groups?: Group[]
  level: UserLevel
}
