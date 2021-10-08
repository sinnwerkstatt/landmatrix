import { User } from "$types/user";

interface Obj {
  id: number;
  status: number;
  draft_status: number;
  versions: ObjVersion[];
  workflowinfos: WorkflowInfo[];
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
}
