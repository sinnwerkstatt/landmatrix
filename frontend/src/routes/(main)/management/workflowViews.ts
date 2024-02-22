import {
  Version2Status,
  type DealHull,
  type InvestorHull,
  type WorkflowInfoType,
} from "$lib/types/newtypes"

export type WorkflowInfoView = (DealHull | InvestorHull) & {
  relevantWFI: WorkflowInfoType
  openReq?: boolean
}

export type CreateWorkflowInfoViewFn = (
  context: { page: { data: { user: { id: number } } } },
  objects: (DealHull | InvestorHull)[],
) => WorkflowInfoView[]

export const createTodoFeedbackView: CreateWorkflowInfoViewFn = (context, objects) =>
  objects
    .map(obj => {
      const wfis = obj.workflowinfos
      const relevantWFI = wfis.find(
        wfi =>
          wfi.status_before === wfi.status_after &&
          wfi.to_user_id === context.page.data.user.id,
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
      const wfis = obj.workflowinfos
      const relevantWFI = wfis.find(
        wfi =>
          (wfi.status_before === Version2Status.REVIEW ||
            wfi.status_before === Version2Status.ACTIVATION) &&
          wfi.status_after === Version2Status.DRAFT &&
          wfi.to_user_id === context.page.data.user.id,
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
      const wfis = obj.workflowinfos
      const relevantWFI = wfis.find(
        wfi =>
          (wfi.status_before === Version2Status.REVIEW ||
            wfi.status_before === Version2Status.ACTIVATION) &&
          wfi.status_after === Version2Status.DRAFT &&
          wfi.from_user_id === context.page.data.user.id,
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
      obj.workflowinfos.some(
        wfi => wfi.status_before === wfi.status_after && !wfi.resolved,
      ),
    )
    .map(obj => {
      const wfis = obj.workflowinfos
      const relevantWFI = wfis.find(
        wfi =>
          wfi.status_before === wfi.status_after &&
          wfi.from_user_id === context.page.data.user.id,
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
