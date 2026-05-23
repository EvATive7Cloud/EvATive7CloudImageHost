export default {
  app: {
    eyebrow: "旧 API 互換",
    title: "EvATive7 Cloud Image Host",
    description: "旧 API を維持しつつ、フロントエンドを Vue コンポーネント構成に置き換えます。",
    upload: "アップロード",
    copyAll: "すべてコピー",
    clearQueue: "キューをクリア",
  },
  language: {
    label: "言語",
    zhCN: "中文",
    en: "English",
    ja: "日本語",
  },
  uploader: {
    title: "ここに画像をドラッグするか、クリックしてファイルを選択",
    hint: "JPG、PNG、WebP に対応。1 ファイルの上限は {size}",
  },
  image: {
    copy: "コピー",
    remove: "削除",
  },
  status: {
    pending: "アップロード待ち",
    uploading: "アップロード中",
    success: "アップロード成功",
    networkError: "ネットワークエラー",
  },
  feedback: {
    copied: "コピーしました",
    noPendingFiles: "アップロード待ちのファイルがありません",
    noLinksToCopy: "コピーできるリンクがありません",
    unsupportedType: "未対応のファイル形式: {name}",
    fileTooLarge: "ファイルサイズが大きすぎます: {name}",
    uploadFailed: "以下のファイルのアップロードに失敗しました：\n{errors}",
  },
} as const;
