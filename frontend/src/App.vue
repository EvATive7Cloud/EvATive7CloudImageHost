<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import ImageList, { type UploadItem } from "./components/ImageList.vue";
import ImageUploader from "./components/ImageUploader.vue";
import { fetchConfig, uploadImages, type UploadResult } from "./api";

const items = ref<UploadItem[]>([]);
const allowedTypes = ref(["image/jpeg", "image/png", "image/webp"]);
const maxFileSize = ref(5 * 1024 * 1024);
const copyAllLabel = ref("复制全部");
const uploadLabel = ref("上传");
const loadingConfig = ref(true);

const pendingItems = computed(() => items.value.filter((item) => item.status === "pending"));
const uploadedUrls = computed(() => items.value.flatMap((item) => (item.remoteUrl ? [item.remoteUrl] : [])));
const maxSizeLabel = computed(() => `${(maxFileSize.value / 1024 / 1024).toFixed(1)} MB`);

onMounted(async () => {
  try {
    const config = await fetchConfig();
    allowedTypes.value = config.allowedTypes;
    maxFileSize.value = config.maxFileSize;
  } finally {
    loadingConfig.value = false;
  }
});

onBeforeUnmount(() => {
  items.value.forEach((item) => URL.revokeObjectURL(item.previewUrl));
});

function addFiles(fileList: FileList | File[]) {
  for (const file of Array.from(fileList)) {
    if (!allowedTypes.value.includes(file.type)) {
      window.alert(`不支持的文件类型：${file.name}`);
      continue;
    }

    if (file.size > maxFileSize.value) {
      window.alert(`文件过大：${file.name}`);
      continue;
    }

    const exists = items.value.some(
      (item) => item.file.name === file.name && item.file.size === file.size,
    );
    if (exists) {
      continue;
    }

    items.value.push({
      key: `${file.name}-${file.size}-${crypto.randomUUID()}`,
      file,
      previewUrl: URL.createObjectURL(file),
      status: "pending",
      message: "等待上传",
      remoteUrl: null,
    });
  }
}

async function onUpload() {
  if (!pendingItems.value.length) {
    flashLabel(uploadLabel, "没有待上传文件");
    return;
  }

  pendingItems.value.forEach((item) => {
    item.status = "uploading";
    item.message = "上传中";
  });

  try {
    const response = await uploadImages(pendingItems.value.map((item) => item.file));
    const results: UploadResult[] =
      "uploaded" in response.data ? response.data.uploaded : response.data.results;

    results.forEach((result) => applyUploadResult(result));
  } catch {
    pendingItems.value.forEach((item) => {
      item.status = "error";
      item.message = "网络错误";
    });
  }
}

function applyUploadResult(result: UploadResult) {
  const item = items.value.find((current) => current.file.name === result.filename && current.status === "uploading");
  if (!item) {
    return;
  }

  if (result.status === 201) {
    item.status = "success";
    item.message = "上传成功";
    item.remoteUrl = new URL(result.url, window.location.origin).toString();
    return;
  }

  item.status = "error";
  item.message = result.message;
}

async function copyText(text: string, label?: typeof copyAllLabel) {
  await navigator.clipboard.writeText(text);
  if (label) {
    flashLabel(label, "已复制");
  }
}

function copyAll() {
  if (!uploadedUrls.value.length) {
    flashLabel(copyAllLabel, "没有可复制链接");
    return;
  }

  void copyText(uploadedUrls.value.join("\n"), copyAllLabel);
}

function removeItem(key: string) {
  const item = items.value.find((current) => current.key === key);
  if (!item) {
    return;
  }

  URL.revokeObjectURL(item.previewUrl);
  items.value = items.value.filter((current) => current.key !== key);
}

function clearQueue() {
  items.value.forEach((item) => URL.revokeObjectURL(item.previewUrl));
  items.value = [];
}

function flashLabel(target: typeof copyAllLabel, text: string) {
  const previous = target.value;
  target.value = text;
  window.setTimeout(() => {
    target.value = previous;
  }, 2000);
}
</script>

<template>
  <main class="page-shell">
    <section class="hero">
      <p class="hero-eyebrow">兼容旧接口</p>
      <h1 class="hero-title">图床上传面板</h1>
      <p class="hero-copy">保留旧 API，前端换成 Vue 组件化结构。</p>
    </section>

    <ImageUploader :disabled="loadingConfig" :max-size-label="maxSizeLabel" @add="addFiles" />

    <section class="toolbar">
      <button class="button button-primary" type="button" @click="onUpload">{{ uploadLabel }}</button>
      <button class="button button-secondary" type="button" @click="copyAll">{{ copyAllLabel }}</button>
      <button class="button button-danger" type="button" @click="clearQueue">清空队列</button>
    </section>

    <ImageList :items="items" @remove="removeItem" @copy="copyText" />
  </main>
</template>
