interface ImportMeta {
  readonly env: {
    readonly VITE_MEDIA_URL: string;
    readonly VITE_BASE_URL: string;
    readonly VITE_SENTRY_DSN: string;
    readonly VITE_GAPI_KEY: string;
    readonly SSR: boolean;
  };
}
