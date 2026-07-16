<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { Vector3 } from 'three';
import { PointCloudOctree, PointSizeType, Potree, PotreeRenderer } from "potree-core";
import { createScene } from "./point-cloud/scene.ts";
import { createClipController } from "./point-cloud/clipping.ts";
import { createGui, type ViewerParams } from "./point-cloud/gui.ts";

const props = defineProps<{
    url: string;
}>();

const wrapper = ref<HTMLDivElement | null>(null);
const container = ref<HTMLDivElement | null>(null);
const isLoading = ref(true);
const loadStatus = ref("Initialising");
const loadError = ref<string | null>(null);

const potree = new Potree();

const SIZE_TYPE_MAP: Record<ViewerParams["sizeType"], PointSizeType> = {
    Fixed: PointSizeType.FIXED,
    Attenuated: PointSizeType.ATTENUATED,
    Adaptive: PointSizeType.ADAPTIVE,
};


onMounted( async () => {
    if (!container.value) {
        loadError.value = "Viewer container not mounted";
        isLoading.value = false;
        return;
    }

    const params: ViewerParams = {
        orthographic: false,
        edlEnabled: true,
        edlStrength: 0.4,
        edlRadius: 1.4,
        pointSize: 1.0,
        sizeType: "Fixed",
    };

    const scene = createScene(container.value);
    const clip = createClipController(scene.scene);
    const pointClouds: PointCloudOctree[] = [];

    const potreeRenderer = new PotreeRenderer({
        edl: {
            enabled: true,
            pointCloudLayer: 1,
            strength: params.edlStrength,
            radius: params.edlRadius,
            opacity: 1.0,
        },
    });

    createGui(container.value, params, {
        onSwitchCamera: (toOrthographic) => scene.switchCamera(toOrthographic),
        onEdlChange: (opts) => potreeRenderer.setEDL(opts),
        onPointSizeChange: (size) => {
            for (const pco of pointClouds) pco.material.size = size;
        },
        onSizeTypeChange: (type) => {
            for (const pco of pointClouds) pco.material.pointSizeType = SIZE_TYPE_MAP[type];
        },
        onResetView: () => scene.resetView(),
        onToggleFullscreen: () => {
            if (!wrapper.value) return;
            if (document.fullscreenElement) {
                document.exitFullscreen?.();
            } else {
                wrapper.value.requestFullscreen?.();
            }
        },
        clip,
    });

    scene.renderer.setAnimationLoop(() => {
        const camera = scene.getCamera();
        potree.updatePointClouds(pointClouds, camera, scene.renderer);
        scene.getControls().update();
        scene.renderer.clear();

        if (params.edlEnabled) {
            potreeRenderer.render({ renderer: scene.renderer, scene: scene.scene, camera, pointClouds });
        } else {
            scene.renderer.render(scene.scene, camera);
        }

        const viewHelper = scene.getViewHelper();
        viewHelper.render(scene.renderer);
        if (viewHelper.animating) viewHelper.update(scene.clock.getDelta());
    });

    window.addEventListener("resize", scene.updateSize);
    document.addEventListener("fullscreenchange", scene.updateSize);
    scene.updateSize();

    const baseUrl = props.url.substring(0, props.url.lastIndexOf('/')+1);
    const fileName = props.url.split("/").pop();

    try {
        loadStatus.value = "Resolving file URL";

        loadStatus.value = `Loading ${props.url}`;
        const pco = await potree.loadPointCloud( fileName, baseUrl);

        pco.material.size = params.pointSize;
        pco.material.pointSizeType = SIZE_TYPE_MAP[params.sizeType];
        pco.material.shape = 2;
        pco.material.inputColorEncoding = 1;
        pco.material.outputColorEncoding = 1;

        // Potree clouds are Z-up; three.js is Y-up. Rotate -90° around X
        // so the model stands the right way up.
        pco.rotation.x = -Math.PI / 2;
        pco.showBoundingBox = false;
        pco.updateMatrixWorld(true);

        const worldBBox = pco.pcoGeometry.boundingBox.clone().applyMatrix4(pco.matrixWorld);
        const center = worldBBox.getCenter(new Vector3());
        const worldSize = worldBBox.getSize(new Vector3());

        // Frame the cloud: orbit around its centre and pull the camera
        // back far enough to see the whole bounding sphere.
        const radius = worldSize.length() * 0.5;
        const fov = (scene.perspectiveCamera.fov * Math.PI) / 180;
        const distance = radius / Math.sin(fov / 2);
        const dir = new Vector3(1, 0.6, 1).normalize();
        const cameraPos = center.clone().addScaledVector(dir, distance);
        scene.perspectiveCamera.position.copy(cameraPos);
        scene.perspectiveCamera.near = Math.max(distance / 1000, 0.01);
        scene.perspectiveCamera.far = distance * 10;
        scene.perspectiveCamera.updateProjectionMatrix();
        scene.orthographicCamera.position.copy(cameraPos);
        scene.getControls().target.copy(center);
        scene.getControls().update();
        scene.setInitialFraming(cameraPos, center);

        // Wire clipping to this cloud and size the helpers to cover it.
        clip.setTarget(pco);
        clip.setBounds(center, worldSize.clone().multiplyScalar(0.5));
        clip.sizeHelpersToDiagonal(worldSize.length() * 1.1);
        clip.updateAxis("X");
        clip.updateAxis("Y");
        clip.updateAxis("Z");

        scene.scene.add(pco);
        pointClouds.push(pco);

        isLoading.value = false;
    } catch (err) {
        console.error("Point cloud load failed", err);
        loadError.value = err instanceof Error ? err.message : String(err);
        isLoading.value = false;
    }

});
</script>

<template>
    <div ref="wrapper" class="point-cloud-wrapper">
        <div ref="container" class="point-cloud-canvas-host"></div>
        <div v-if="isLoading || loadError" class="point-cloud-overlay">
            <div v-if="loadError" class="point-cloud-error">
                <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>
                <div>Failed to load point cloud</div>
                <div class="point-cloud-error-detail">{{ loadError }}</div>
            </div>
            <div v-else class="point-cloud-loader">
                <div class="point-cloud-spinner" aria-hidden="true"></div>
                <div class="point-cloud-status">{{ loadStatus }}</div>
            </div>
        </div>
    </div>
</template>

<style>
.point-cloud-mount {
    width: 100%;
    height: 650px;
}

.point-cloud-mount--full {
    height: calc(100vh - 200px);
}

/* lil-gui customisation. Unscoped so the overrides apply to the GUI's
   internal class names; the .point-cloud-gui prefix keeps it isolated to
   this component's GUI instance. */
.point-cloud-gui.lil-gui {
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 10;
    --background-color: rgba(20, 22, 28, 0.92);
    --text-color: #e5e7eb;
    --title-background-color: rgba(96, 165, 250, 0.18);
    --title-text-color: #f5f7fa;
    --widget-color: rgba(255, 255, 255, 0.08);
    --hover-color: rgba(255, 255, 255, 0.14);
    --focus-color: rgba(96, 165, 250, 0.35);
    --number-color: #93c5fd;
    --string-color: #fbbf24;
    --font-size: 12px;
    --input-font-size: 12px;
    --folder-indent: 8px;
    --padding: 6px;
    --spacing: 5px;
    --slider-knob-width: 3px;
    --slider-input-width: 28%;
    --color-input-width: 28%;
    --slider-input-min-width: 40px;
    --color-input-min-width: 40px;
    --folder-closed-arrow: '▸';
    --folder-open-arrow: '▾';
    --widget-border-radius: 4px;
    --scrollbar-width: 6px;
    --title-height: 32px;
    --widget-height: 22px;
    width: 280px;
    /* Cap to viewer height so the panel never overflows the wrapper; the
       internal list scrolls when the folders are taller than this. */
    max-height: calc(100% - 24px);
    border-radius: 8px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(8px);
    overflow-y: auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.point-cloud-gui.lil-gui .title {
    font-weight: 600;
    letter-spacing: 0.02em;
    /* lil-gui sizes titles via --title-height; use horizontal padding only
       and let line-height fill the row so text isn't clipped. */
    padding: 0 10px;
    line-height: var(--title-height);
    --title-height: inherit;
}

.point-cloud-gui.lil-gui .controller {
    padding: 2px 8px;
    align-items: center;
}

.point-cloud-gui.lil-gui .controller .name {
    font-size: 11px;
    opacity: 0.85;
}

.point-cloud-gui.lil-gui button {
    cursor: pointer;
}

/* Vertically centre checkboxes — by default they sit at the top of the
   widget cell, out of line with the controller's label text. */
.point-cloud-gui.lil-gui .controller.boolean .widget {
    display: flex;
    align-items: center;
    height: 100%;
}

.point-cloud-gui.lil-gui .controller.boolean input[type="checkbox"] {
    margin: 0;
    cursor: pointer;
}
</style>

<style scoped>
.point-cloud-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
    background: #0b0d12;
    border-radius: 6px;
    overflow: hidden;
}

.point-cloud-canvas-host {
    width: 100%;
    height: 100%;
}

.point-cloud-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(11, 13, 18, 0.75);
    z-index: 5;
    pointer-events: none;
}

.point-cloud-loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    color: #e5e7eb;
    font-size: 14px;
}

.point-cloud-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.15);
    border-top-color: #60a5fa;
    border-radius: 50%;
    animation: point-cloud-spin 0.8s linear infinite;
}

@keyframes point-cloud-spin {
    to { transform: rotate(360deg); }
}

.point-cloud-status {
    font-weight: 500;
}

.point-cloud-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    color: #fca5a5;
    text-align: center;
    padding: 16px;
}

.point-cloud-error .fa {
    font-size: 32px;
}

.point-cloud-error-detail {
    font-size: 12px;
    opacity: 0.8;
}
</style>