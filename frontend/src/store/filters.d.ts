interface GQLFilter {
  field: string;
  operation?: string;
  value: any;
  exclusion?: boolean;
  allow_null?: boolean;
}
