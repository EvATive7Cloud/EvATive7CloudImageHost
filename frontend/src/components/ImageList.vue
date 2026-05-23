<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";

export type UploadItem = {
  key: string;
  file: File;
  previewUrl: string;
  status: "pending" | "uploading" | "success" | "error";
  message: string;
  remoteUrl: string | null;
};

defineProps<{
  items: UploadItem[];
}>();

const emit = defineEmits<{
  remove: [key: string];
  copy: [text: string];
}>();

const { t } = useI18n();

const copiedKey = ref<string | null>(null);

function handleCopy(item: UploadItem) {
  if (!item.remoteUrl) return;
  emit("copy", item.remoteUrl);
  copiedKey.value = item.key;
  window.setTimeout(() => {
    if (copiedKey.value === item.key) {
      copiedKey.value = null;
    }
  }, 2000);
}
</script>

<template>
  <section class="image-list">
    <article v-for="item in items" :key="item.key" class="image-card">
      <img class="image-thumb" :src="item.previewUrl" :alt="item.file.name" />
      <div class="image-body">
        <div class="image-name">{{ item.file.name }}</div>
        <div class="image-meta">{{ item.message }}</div>
        <a
          v-if="item.remoteUrl"
          class="image-link"
          :href="item.remoteUrl"
          target="_blank"
          rel="noreferrer"
        >
          {{ item.remoteUrl }}
        </a>
      </div>
      <div class="image-actions">
        <button
          v-if="item.remoteUrl"
          class="button button-secondary"
          type="button"
          @click="handleCopy(item)"
        >
          {{ copiedKey === item.key ? t("feedback.copied") : t("image.copy") }}
        </button>
        <button class="button button-danger" type="button" @click="emit('remove', item.key)">
          {{ t("image.remove") }}
        </button>
      </div>
    </article>
  </section>
</template>
