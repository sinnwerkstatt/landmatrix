import type { User } from "$lib/types/user"
import type { Country } from "$lib/types/wagtail"

export enum Transition {
  TO_REVIEW,
  TO_ACTIVATION,
  ACTIVATE,
  TO_DRAFT,
}

export enum Status {
  DRAFT = 1,
  LIVE,
  UPDATED,
  DELETED,
  REJECTED, // legacy
  TO_DELETE, // legacy
}

export enum DraftStatus {
  DRAFT = 1,
  REVIEW,
  ACTIVATION,
  REJECTED, // legacy
  TO_DELETE,
}

export interface Obj {
  id: number
  status: Status
  draft_status: DraftStatus | null
  versions: ObjVersion[]
  workflowinfos?: WorkflowInfo[]
  created_at?: Date
  created_by?: User
  modified_at?: Date
  modified_by?: User
  country?: Country
  country_id?: number
  current_draft_id?: number
}

export interface ObjVersion {
  id: number
  created_at: Date
  created_by: User
  modified_at: Date
  modified_by: User
  object_id: number
}

type WFReply = {
  timestamp: string
  user_id: number
  comment: string
}
export interface WorkflowInfo {
  id: number
  from_user: User
  to_user?: User
  draft_status_before: DraftStatus | null
  draft_status_after: DraftStatus | null
  timestamp: string
  comment: string
  resolved: boolean
  replies: WFReply[]
  __typename?: string
}
