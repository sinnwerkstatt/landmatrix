import { User } from "$types/user";
import { Country } from "$types/wagtail";

export enum Transition {
  TO_REVIEW,
  TO_ACTIVATION,
  ACTIVATE,
  TO_DRAFT,
}

interface Obj {
  id: number;
  status: number;
  draft_status: number | null;
  versions: ObjVersion[];
  workflowinfos: WorkflowInfo[];
  created_at: Date;
  created_by: User;
  modified_at: Date;
  modified_by: User;
  country?: Country;
  country_id?: number;
}

interface ObjVersion {
  id: number;
  created_at: Date;
  created_by: User;
  object_id: Int;
}

interface WorkflowInfo {
  id: number;
  from_user: User;
  to_user?: User;
  draft_status_before: number;
  draft_status_after: number;
  timestamp: Date;
  comment: string;
  processed_by_receiver: boolean;
  __typename?: string;
}
