export type Deal = {
  id: number;
  status: number;
  draft_status: number;
  versions: DealVersion[];
};

export type DealVersion = {
  id: number;
  deal: Deal;
  created_at: Date;
  created_by: User;
  object_id: Int;
};
