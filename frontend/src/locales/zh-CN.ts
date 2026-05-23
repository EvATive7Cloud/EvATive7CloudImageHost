export default {
  app: {
    eyebrow: "兼容旧接口",
    title: "图床上传面板",
    description: "保留旧 API，前端换成 Vue 组件化结构。",
    upload: "上传",
    copyAll: "复制全部",
    clearQueue: "清空队列",
  },
  language: {
    label: "语言",
    zhCN: "中文",
    en: "English",
    ja: "日本語",
  },
  uploader: {
    title: "拖拽图片到这里，或点这里选文件",
    hint: "支持 JPG、PNG、WebP，单文件最大 {size}",
  },
  image: {
    copy: "复制",
    remove: "删除",
  },
  status: {
    pending: "等待上传",
    uploading: "上传中",
    success: "上传成功",
    networkError: "网络错误",
  },
  feedback: {
    copied: "已复制",
    noPendingFiles: "没有待上传文件",
    noLinksToCopy: "没有可复制链接",
    unsupportedType: "不支持的文件类型：{name}",
    fileTooLarge: "文件过大：{name}",
  },
} as const;
