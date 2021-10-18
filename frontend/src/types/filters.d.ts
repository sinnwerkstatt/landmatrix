interface GQLFilter {
  field: string;
  operation?: string;
  value: unknown;
  exclusion?: boolean;
  allow_null?: boolean;
}
