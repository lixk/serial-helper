<script setup>
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { onMounted } from 'vue'
import bus from './eventBus'

const D2R = Math.PI / 180 // 角度转弧度

onMounted(() => {
	const rotation = { x: 0, y: 0, z: 0 }
	initScene(rotation)
	bus.on('flyControlData', function (dataItem) {
		rotation.x = (dataItem['x'] || 0) * D2R
		rotation.y = (dataItem['y'] || 0) * D2R
		rotation.z = (dataItem['z'] || 0) * D2R
	})
})

function initScene(rotation) {
	const container = document.getElementById("flyControlContainer")
	container.parentElement.style.overflow = 'hidden'
	var width = container.parentElement.clientWidth
	var height = container.parentElement.clientHeight
	const scene = new THREE.Scene()
	// 创建相机
	const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)

	// 设置相机位置
	camera.position.z = 35
	// 添加环境光
	const skyColor = 0xB1E1FF;  // light blue
	const groundColor = 0xffffff;  // brownish orange
	const intensity = 1;
	const light = new THREE.HemisphereLight(skyColor, groundColor, intensity);
	scene.add(light);
	// 创建渲染器
	const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
	renderer.setSize(width, height)
	container.appendChild(renderer.domElement)
	// 加载背景图
	const loader = new THREE.TextureLoader();
	// const bgTexture = loader.load('src/assets/sky.jpg')
	// const bgTexture = loader.load('/static/space.jpg')
	// scene.background = bgTexture
	scene.add(new THREE.AxesHelper(120))
	scene.add(new THREE.GridHelper(100))
	const controls = new OrbitControls(camera, renderer.domElement)
	// 加载飞机模型
	const planeLoader = new GLTFLoader();
	planeLoader.load("/static/plane.glb", (gltf) => {
		const root = gltf.scene
		scene.add(root)
		//显示动画
		function animation(time) {
			root.rotation.x = rotation.x
			root.rotation.y = rotation.y
			root.rotation.z = rotation.z
			controls.update();
			renderer.render(scene, camera);
		}
		renderer.setAnimationLoop(animation);
	});
	// 修正缩放
	setInterval(() => {
		var newWidth = container.parentElement.clientWidth
		var newHeight = container.parentElement.clientHeight
		if (width != newWidth || height != newHeight) {
			width = newWidth
			height = newHeight
			console.log("width", newWidth, "height: ", newHeight)
			renderer.setSize(width, height)
		}
	}, 100)

	return rotation
}


</script>

<template>
	<div id="flyControlContainer"></div>
</template>