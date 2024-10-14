export type ImageFileType = "svg" | "png" | "webp"
export type DataFileType = "json" | "csv" | "xlsx"

export type ImageDownloadEvent = CustomEvent<ImageFileType>
export type DataDownloadEvent = CustomEvent<DataFileType>

export const aDownload = (blob: Blob, filename: string): void => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")

  a.href = url
  a.download = filename
  a.click()

  URL.revokeObjectURL(url)
}
