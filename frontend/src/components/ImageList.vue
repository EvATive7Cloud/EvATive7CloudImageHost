<script setup lang="ts">
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
          @click="emit('copy', item.remoteUrl)"
        >
          复制
        </button>
        <button class="button button-danger" type="button" @click="emit('remove', item.key)">
          删除
        </button>
      </div>
    </article>
  </section>
</template>
