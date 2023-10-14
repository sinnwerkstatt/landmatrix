export interface FormField {
  name: string
  label: string
  class: string
  required?: boolean
  related_model?: string
  // choices?: { [key: string | number]: string }
  choices?: { value: string; label: string; group?: string }[]
  unit?: string
  help_text?: string
  max_length?: number
  min_value?: number
  max_value?: number
}
