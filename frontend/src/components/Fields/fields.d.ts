export interface FormField {
  name: string;
  label: string;
  class: string;
  required: boolean;
  related_model?: string;
  choices?: { [key: string | number]: string };
}
