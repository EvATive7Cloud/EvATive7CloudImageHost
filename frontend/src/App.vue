<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import ImageList, { type UploadItem } from "./components/ImageList.vue";
import ImageUploader from "./components/ImageUploader.vue";
import { fetchConfig, uploadImages, type UploadResult } from "./api";
import { setLocale, supportedLocales, type SupportedLocale } from "./i18n";

const items = ref<UploadItem[]>([]);
const allowedTypes = ref(["image/jpeg", "image/png", "image/webp"]);
const maxFileSize = ref(5 * 1024 * 1024);
const loadingConfig = ref(true);
const copyAllFeedback = ref<string | null>(null);
const uploadFeedback = ref<string | null>(null);
const { locale, t } = useI18n();

const pendingItems = computed(() => items.value.filter((item) => item.status === "pending"));
const uploadedUrls = computed(() => items.value.flatMap((item) => (item.remoteUrl ? [item.remoteUrl] : [])));
const maxSizeLabel = computed(() => `${(maxFileSize.value / 1024 / 1024).toFixed(1)} MB`);
const uploadLabel = computed(() => uploadFeedback.value ?? t("app.upload"));
const copyAllLabel = computed(() => copyAllFeedback.value ?? t("app.copyAll"));
const localeOptions: { value: SupportedLocale; labelKey: string }[] = [
  { value: "zh-CN", labelKey: "language.zhCN" },
  { value: "en", labelKey: "language.en" },
  { value: "ja", labelKey: "language.ja" },
];

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
      window.alert(t("feedback.unsupportedType", { name: file.name }));
      continue;
    }

    if (file.size > maxFileSize.value) {
      window.alert(t("feedback.fileTooLarge", { name: file.name }));
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
      message: t("status.pending"),
      remoteUrl: null,
    });
  }
}

async function onUpload() {
  if (!pendingItems.value.length) {
    flashLabel(uploadFeedback, t("feedback.noPendingFiles"));
    return;
  }

  pendingItems.value.forEach((item) => {
    item.status = "uploading";
    item.message = t("status.uploading");
  });

  try {
    const response = await uploadImages(pendingItems.value.map((item) => item.file));
    const results: UploadResult[] =
      "uploaded" in response.data ? response.data.uploaded : response.data.results;

    const failedList: string[] = [];
    results.forEach((result) => {
      applyUploadResult(result);
      if (result.status !== 201) {
        failedList.push(`${result.filename}: ${result.message}`);
      }
    });

    if (failedList.length > 0) {
      window.alert(t("feedback.uploadFailed", { errors: failedList.join("\n") }));
    }
  } catch {
    pendingItems.value.forEach((item) => {
      item.status = "error";
      item.message = t("status.networkError");
    });
    window.alert(t("status.networkError"));
  }
}

function applyUploadResult(result: UploadResult) {
  const item = items.value.find((current) => current.file.name === result.filename && current.status === "uploading");
  if (!item) {
    return;
  }

  if (result.status === 201) {
    item.status = "success";
    item.message = t("status.success");
    item.remoteUrl = new URL(result.url, window.location.origin).toString();
    return;
  }

  item.status = "error";
  item.message = result.message;
}

async function copyText(text: string, showFeedback = false) {
  await navigator.clipboard.writeText(text);
  if (showFeedback) {
    flashLabel(copyAllFeedback, t("feedback.copied"));
  }
}

function copyAll() {
  if (!uploadedUrls.value.length) {
    flashLabel(copyAllFeedback, t("feedback.noLinksToCopy"));
    return;
  }

  void copyText(uploadedUrls.value.join("\n"), true);
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

function flashLabel(target: typeof copyAllFeedback, text: string) {
  target.value = text;
  window.setTimeout(() => {
    target.value = null;
  }, 2000);
}

function onLocaleChange(event: Event) {
  const nextLocale = (event.target as HTMLSelectElement).value;
  if (supportedLocales.includes(nextLocale as SupportedLocale)) {
    setLocale(nextLocale as SupportedLocale);
  }
}
</script>

<template>
  <main class="page-shell">
    <section class="topbar">
      <label class="locale-switcher">
        <span class="locale-label">{{ t("language.label") }}</span>
        <select class="locale-select" :value="locale" @change="onLocaleChange">
          <option v-for="option in localeOptions" :key="option.value" :value="option.value">
            {{ t(option.labelKey) }}
          </option>
        </select>
      </label>
    </section>

    <section class="hero">
      <p class="hero-eyebrow">{{ t("app.eyebrow") }}</p>
      <h1 class="hero-title">{{ t("app.title") }}</h1>
      <p class="hero-copy">{{ t("app.description") }}</p>
    </section>

    <ImageUploader :disabled="loadingConfig" :max-size-label="maxSizeLabel" @add="addFiles" />

    <section class="toolbar">
      <button class="button button-primary" type="button" @click="onUpload">{{ uploadLabel }}</button>
      <button class="button button-secondary" type="button" @click="copyAll">{{ copyAllLabel }}</button>
      <button class="button button-danger" type="button" @click="clearQueue">{{ t("app.clearQueue") }}</button>
    </section>

    <ImageList :items="items" @remove="removeItem" @copy="copyText" />
  </main>
</template>
