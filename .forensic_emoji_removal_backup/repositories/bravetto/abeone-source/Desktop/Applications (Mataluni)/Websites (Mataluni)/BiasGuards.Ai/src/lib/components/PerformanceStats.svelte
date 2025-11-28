<script lang="ts">
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';

	// Metrics state
	let performanceData = $state({
		lighthouse: 0,
		fcp: 0,
		lcp: 0,
		cls: 0,
		fid: 0,
		bundleSize: 0,
		isLoaded: false
	});

	// Reference values
	const REFERENCE = {
		lighthouse: 85,
		fcp: 2.0,
		lcp: 3.0,
		cls: 0.15,
		fid: 150,
		bundleSize: 250
	} as const;

	// Component refs
	let statsSection: HTMLElement;

	// Basic setup
	onMount(() => {
		// Simple animation
		gsap.fromTo(statsSection, { opacity: 0 }, { opacity: 1, duration: 0.5 });

		// Show sample data
		setTimeout(() => {
			performanceData = {
				lighthouse: 87,
				fcp: 1.8,
				lcp: 2.4,
				cls: 0.12,
				fid: 95,
				bundleSize: 210,
				isLoaded: true
			};
		}, 500);
	});

	// Simple status
	const getColor = (current: number, ref: number, reverse = false) => {
		const ratio = reverse ? ref / current : current / ref;
		if (ratio >= 0.8) return 'green';
		if (ratio >= 0.6) return 'yellow';
		return 'red';
	};
</script>

<section
	bind:this={statsSection}
	class="performance-section py-16 bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-800 dark:via-gray-900 dark:to-indigo-900/20"
>
	<div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Section Header -->
		<div class="text-center mb-12">
			<h2
				class="stat-number reveal-on-scroll text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4"
			>
				App Stats
			</h2>
			<p class="reveal-fade-in text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
				Current performance data
			</p>
		</div>

		<!-- Performance Metrics Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
			<!-- Lighthouse Score -->
			<div class="stat-card reveal-scale-up biasguards-card text-center">
				<div class="text-4xl mb-2">🏆</div>
				<div class="stat-number text-3xl font-bold text-blue-600 mb-2" data-suffix="">
					{performanceData.lighthouse.toFixed(0)}
				</div>
				<div class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
					Lighthouse Score
				</div>
			</div>

			<!-- First Contentful Paint -->
			<div class="stat-card reveal-scale-up biasguards-card text-center">
				<div class="text-4xl mb-2">⚡</div>
				<div class="stat-number text-3xl font-bold text-blue-600 mb-2" data-suffix="s">
					{performanceData.fcp.toFixed(2)}
				</div>
				<div class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
					First Contentful Paint
				</div>
			</div>

			<!-- Largest Contentful Paint -->
			<div class="stat-card reveal-scale-up biasguards-card text-center">
				<div class="text-4xl mb-2">🎯</div>
				<div class="text-3xl font-bold text-blue-600 mb-2">
					{performanceData.lcp.toFixed(2)}s
				</div>
				<div class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
					Largest Contentful Paint
				</div>
			</div>

			<!-- Cumulative Layout Shift -->
			<div class="stat-card reveal-scale-up biasguards-card text-center">
				<div class="text-4xl mb-2">📐</div>
				<div class="text-3xl font-bold text-blue-600 mb-2">
					{performanceData.cls.toFixed(3)}
				</div>
				<div class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
					Cumulative Layout Shift
				</div>
			</div>

			<!-- First Input Delay -->
			<div class="stat-card reveal-scale-up biasguards-card text-center">
				<div class="text-4xl mb-2">👆</div>
				<div class="text-3xl font-bold text-blue-600 mb-2">
					{performanceData.fid.toFixed(0)}ms
				</div>
				<div class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
					First Input Delay
				</div>
			</div>

			<!-- Bundle Size -->
			<div class="stat-card reveal-scale-up biasguards-card text-center">
				<div class="text-4xl mb-2">📦</div>
				<div class="text-3xl font-bold text-blue-600 mb-2">
					{performanceData.bundleSize.toFixed(0)}KB
				</div>
				<div class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Bundle Size</div>
			</div>
		</div>

		<!-- Tech Stack -->
		<div class="biasguards-card">
			<h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4 text-center">
				Built With
			</h3>

			<div class="grid grid-cols-4 gap-4 text-center">
				<div class="flex flex-col items-center">
					<div class="text-2xl mb-2">🔥</div>
					<div class="text-sm font-medium text-gray-900 dark:text-white">Svelte</div>
				</div>

				<div class="flex flex-col items-center">
					<div class="text-2xl mb-2">💎</div>
					<div class="text-sm font-medium text-gray-900 dark:text-white">Tailwind</div>
				</div>

				<div class="flex flex-col items-center">
					<div class="text-2xl mb-2">⚡</div>
					<div class="text-sm font-medium text-gray-900 dark:text-white">GSAP</div>
				</div>

				<div class="flex flex-col items-center">
					<div class="text-2xl mb-2">🚀</div>
					<div class="text-sm font-medium text-gray-900 dark:text-white">Vite</div>
				</div>
			</div>
		</div>
	</div>
</section>
