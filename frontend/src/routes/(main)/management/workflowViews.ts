import type { Deal, DealWorkflowInfo } from "$lib/types/deal"
import type { WorkflowInfo } from "$lib/types/generics"
import { DraftStatus } from "$lib/types/generics"
import type { Investor } from "$lib/types/investor"

export type WorkflowInfoView = (Deal | Investor) & {
  relevantWFI: WorkflowInfo
  openReq?: boolean
}

export type CreateWorkflowInfoViewFn = (
  context: { page: { data: { user: { id: number } } } },
  objects: (Deal | Investor)[],
) => WorkflowInfoView[]

export const createTodoFeedbackView: CreateWorkflowInfoViewFn = (context, objects) =>
  objects
    .map(obj => {
      const wfis = obj.workflowinfos as WorkflowInfo[]
      const relevantWFI = wfis.find(
        wfi =>
          wfi.draft_status_before === wfi.draft_status_after &&
          wfi.to_user?.id === context.page.data.user.id,
      )

      const lastReply = relevantWFI?.replies.at(-1)
      const openReq = !lastReply || lastReply.user_id !== context.page.data.user.id

      return { ...obj, relevantWFI, openReq } as WorkflowInfoView
    })
    .sort((a, b) => {
      if (a.openReq && !b.openReq) return -1
      else if (b.openReq && !a.openReq) return 1
      if (!b.relevantWFI?.timestamp || !a.relevantWFI?.timestamp) return 0
      return (
        new Date(b.relevantWFI.timestamp).valueOf() -
        new Date(a.relevantWFI.timestamp).valueOf()
      )
    })

export const createTodoImprovementView: CreateWorkflowInfoViewFn = (context, objects) =>
  objects
    .map(obj => {
      const wfis = obj.workflowinfos as WorkflowInfo[]
      const relevantWFI = wfis.find(
        wfi =>
          (wfi.draft_status_before === DraftStatus.REVIEW ||
            wfi.draft_status_before === DraftStatus.ACTIVATION) &&
          wfi.draft_status_after === DraftStatus.DRAFT &&
          wfi.to_user?.id === context.page.data.user.id,
      )

      return { ...obj, relevantWFI } as WorkflowInfoView
    })
    .sort((a, b) => {
      if (!b.relevantWFI?.timestamp || !a.relevantWFI?.timestamp) return 0
      return (
        new Date(b.relevantWFI.timestamp).valueOf() -
        new Date(a.relevantWFI.timestamp).valueOf()
      )
    })

export const createRequestImprovementView: CreateWorkflowInfoViewFn = (
  context,
  objects,
) =>
  objects
    .map(obj => {
      const wfis = obj.workflowinfos as DealWorkflowInfo[]
      const relevantWFI = wfis.find(
        wfi =>
          (wfi.draft_status_before === DraftStatus.REVIEW ||
            wfi.draft_status_before === DraftStatus.ACTIVATION) &&
          wfi.draft_status_after === DraftStatus.DRAFT &&
          wfi.from_user?.id === context.page.data.user.id,
      )

      return { ...obj, relevantWFI } as WorkflowInfoView
    })
    .sort((a, b) => {
      if (!b.relevantWFI?.timestamp || !a.relevantWFI?.timestamp) return 0
      return (
        new Date(b.relevantWFI.timestamp).valueOf() -
        new Date(a.relevantWFI.timestamp).valueOf()
      )
    })

export const createRequestFeedbackView: CreateWorkflowInfoViewFn = (context, objects) =>
  objects
    .filter(obj =>
      (obj.workflowinfos as DealWorkflowInfo[]).some(
        wfi => wfi.draft_status_before === wfi.draft_status_after && !wfi.resolved,
      ),
    )
    .map(obj => {
      const wfis = obj.workflowinfos as DealWorkflowInfo[]
      const relevantWFI = wfis.find(
        wfi =>
          wfi.draft_status_before === wfi.draft_status_after &&
          wfi.from_user?.id === context.page.data.user.id,
      )

      const lastReply = relevantWFI?.replies.at(-1)
      const openReq = lastReply && lastReply.user_id !== context.page.data.user.id

      return { ...obj, relevantWFI, openReq } as WorkflowInfoView
    })
    .sort((a, b) => {
      if (a.openReq && !b.openReq) return -1
      else if (b.openReq && !a.openReq) return 1
      if (!b.relevantWFI?.timestamp || !a.relevantWFI?.timestamp) return 0
      return (
        new Date(b.relevantWFI.timestamp).valueOf() -
        new Date(a.relevantWFI.timestamp).valueOf()
      )
    })
