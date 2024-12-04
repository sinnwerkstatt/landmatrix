import { error } from "@sveltejs/kit"

import { getCsrfToken } from "$lib/utils"

export async function updateDealVariable(deal: number, variable: number, body: object) {
  if (!deal || !variable)
    throw error(400, { message: "Deal ID and Variable must be defined" })
  try {
    const res = await fetch(`/api/accountability/deal/${deal}/${variable}/`, {
      method: "PATCH",
      credentials: "include",
      body: JSON.stringify(body),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (!res.ok) throw error(res.status, { message: res.statusText })
    return res
  } catch (error) {
    return error
  }
}

export async function bulkUpdateDealVariable(body: {
  toUpdate: { deal: number; variable: number }[]
  assignee: number | null
}) {
  try {
    const res = await fetch(`/api/accountability/deal/bulk/`, {
      method: "PATCH",
      credentials: "include",
      body: JSON.stringify({ to_update: body.toUpdate, assignee: body.assignee }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (!res.ok) throw error(res.status, { message: res.statusText })
    return res
  } catch (error) {
    return error
  }
}
