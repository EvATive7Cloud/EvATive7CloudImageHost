<script setup lang="ts">
defineProps<{
  disabled?: boolean;
  maxSizeLabel: string;
}>();

const emit = defineEmits<{
  add: [files: FileList | File[]];
}>();

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
    <span class="upload-kicker">EvATive7 Cloud Image Host</span>
    <strong class="upload-title">拖拽图片到这里，或点这里选文件</strong>
    <span class="upload-hint">支持 JPG、PNG、WebP，单文件最大 {{ maxSizeLabel }}</span>
  </label>
</template>
