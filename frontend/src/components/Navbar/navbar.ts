export type MenuEntry = NavLink | SubMenu

export interface SubMenu {
  title: string
  subEntries: NavLink[]
  href?: never
}

export interface NavLink {
  title: string
  subEntries?: never
  href: string
}

export const isSubMenu = (entry: MenuEntry): entry is SubMenu => !!entry.subEntries
// export const isNavLink = (entry: MenuEntry): entry is NavLink => !!entry.href
