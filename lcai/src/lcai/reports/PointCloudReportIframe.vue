<script setup lang="ts">

const props = defineProps<{
    url: string;
}>();

const iframeUrl = `https://legiongis.github.io/potree-viewer-standalone/?url=${props.url}`;

</script>

<template>
    <iframe id="potree-viewer-iframe" :src=iframeUrl></iframe>
</template>

<style>
    iframe {
        height: calc(100vh - 200px);
        width: 100%;
    }
</style>