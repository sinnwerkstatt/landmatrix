export type Deal = {
  id: number;
  status: number;
  draft_status: number;
  versions: DealVersion[];
  current_intention_of_investment: string[];
  current_implementation_status: string;
};

export type DealVersion = {
  id: number;
  deal: Deal;
  created_at: Date;
  created_by: User;
  object_id: Int;
};
