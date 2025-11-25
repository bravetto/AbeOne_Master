<script lang="ts">
	import { onMount } from 'svelte';
	import Hero from '$lib/components/Hero.svelte';
	import BiasDetector from '$lib/components/BiasDetector.svelte';
	import MissionStatement from '$lib/components/MissionStatement.svelte';
	import PerformanceStats from '$lib/components/PerformanceStats.svelte';
	import { checkCode } from '$lib/utils/simple-validator';

	// Svelte 5 Runes for reactive state
	let heroSection: HTMLElement;
	let isLoaded = $state(false);

	// Mission-critical statistics
	const STATS = {
		legalCrisis: '$26,500',
		courtDate: 'August 25, 2025',
		revenueToJustice: '15%'
	};

	const missionDays = $derived(() => {
		const court = new Date('2025-08-25');
		const now = new Date();
		const diffTime = court.getTime() - now.getTime();
		const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
		return diffDays > 0 ? diffDays : 0;
	});

	// Initialize page
	onMount(() => {
		isLoaded = true;
		
		// BiasGuard validator is now integrated and ready for use
		// Use checkCode(someCode) anywhere to validate code against:
		// - React/Vue contamination
		// - JAHmere Webb story authenticity  
		// - Svelte 5 compliance
		// - Performance best practices
	});
</script>

<svelte:head>
	<title>BiasGuards.AI - Justice-Driven AI Bias Detection</title>
	<meta
		name="description"
		content="Born from JAHmere Webb's $26,500 legal crisis. AI bias detection tool with 15% revenue to criminal justice reform. Court date: August 25, 2025."
	/>
</svelte:head>

<!-- Eye-Popping Hero Section -->
<Hero />

<!-- Mission Statistics -->
<section class="py-12 bg-white dark:bg-gray-900">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
			<div
				class="stat-card reveal-scale-up bg-gradient-to-br from-alert-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 p-6 rounded-xl border border-red-200 dark:border-red-700"
			>
				<div class="text-3xl font-bold text-alert-red-600 dark:text-red-400 mb-2">
					{STATS.legalCrisis}
				</div>
				<div class="text-sm text-red-700 dark:text-red-300 font-medium">Legal Crisis Amount</div>
			</div>

			<div
				class="stat-card reveal-scale-up bg-gradient-to-br from-justice-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 p-6 rounded-xl border border-blue-200 dark:border-blue-700"
			>
				<div class="text-3xl font-bold text-justice-blue-600 dark:text-blue-400 mb-2">
					{missionDays}
				</div>
				<div class="text-sm text-blue-700 dark:text-blue-300 font-medium">Days to Court Date</div>
			</div>

			<div
				class="stat-card reveal-scale-up bg-gradient-to-br from-success-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 p-6 rounded-xl border border-green-200 dark:border-green-700"
			>
				<div class="text-3xl font-bold text-success-green-600 dark:text-green-400 mb-2">
					{STATS.revenueToJustice}
				</div>
				<div class="text-sm text-green-700 dark:text-green-300 font-medium">
					Revenue to Justice Reform
				</div>
			</div>

			<div
				class="stat-card reveal-scale-up bg-gradient-to-br from-indigo-50 to-purple-100 dark:from-indigo-900/20 dark:to-purple-800/20 p-6 rounded-xl border border-indigo-200 dark:border-indigo-700"
			>
				<div class="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">Aug 25</div>
				<div class="text-sm text-indigo-700 dark:text-indigo-300 font-medium">Court Date 2025</div>
			</div>
		</div>
	</div>
</section>

<!-- Main Application Components -->
{#if isLoaded}
	<div id="mission-story" class="reveal-on-scroll">
		<MissionStatement />
	</div>
	<div id="bias-detector" class="reveal-fade-in">
		<BiasDetector />
	</div>
	<div class="performance-section reveal-slide-left">
		<PerformanceStats />
	</div>
{/if}

<style>
	/* Component-specific styles */
	.stat-card {
		transition:
			transform 0.2s ease-out,
			box-shadow 0.2s ease-out;
	}

	.stat-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
	}
</style>
