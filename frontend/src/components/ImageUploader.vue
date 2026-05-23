<script setup lang="ts">
import { useI18n } from "vue-i18n";

defineProps<{
  disabled?: boolean;
  maxSizeLabel: string;
}>();

const emit = defineEmits<{
  add: [files: FileList | File[]];
}>();

const { t } = useI18n();

function onChange(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files) {
    return;
  }

  emit("add", input.files);
  input.value = "";
}

function onDrop(event: DragEvent) {
  event.preventDefault();
  if (!event.dataTransfer?.files?.length) {
    return;
  }

  emit("add", event.dataTransfer.files);
}
</script>

<template>
  <label
    class="upload-panel"
    :class="{ 'is-disabled': disabled }"
    @dragover.prevent
    @drop="onDrop"
  >
    <input
      class="upload-input"
      type="file"
      multiple
      accept="image/jpeg,image/png,image/webp"
      :disabled="disabled"
      @change="onChange"
    />
    <strong class="upload-title">{{ t("uploader.title") }}</strong>
    <span class="upload-hint">{{ t("uploader.hint", { size: maxSizeLabel }) }}</span>
  </label>
</template>
