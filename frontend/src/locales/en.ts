export default {
  app: {
    title: "EvATive7 Cloud Image Host",
    upload: "Upload",
    copyAll: "Copy All",
    clearQueue: "Clear Queue",
  },
  language: {
    label: "Language",
    zhCN: "中文",
    en: "English",
    ja: "日本語",
  },
  uploader: {
    title: "Drag images here, or click to choose files",
    hint: "Supports JPG, PNG, and WebP. Max size per file: {size}",
  },
  image: {
    copy: "Copy",
    remove: "Delete",
  },
  status: {
    pending: "Waiting to upload",
    uploading: "Uploading",
    success: "Upload succeeded",
    networkError: "Network error",
  },
  feedback: {
    copied: "Copied",
    noPendingFiles: "No files waiting to upload",
    noLinksToCopy: "No links available to copy",
    unsupportedType: "Unsupported file type: {name}",
    fileTooLarge: "File too large: {name}",
    uploadFailed: "The following files failed to upload:\n{errors}",
  },
} as const;
