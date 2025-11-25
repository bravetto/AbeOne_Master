<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { BiasGuardAnimations } from '$lib/utils/animations';

	const MISSION_CONTEXT = {
		courtDate: 'August 25, 2025',
		mission: 'JAHmere Webb Freedom Mission',
		revenueToJustice: '15%',
		legalCrisis: '$26,500'
	} as const;

	$: pageTitle = $page.data?.meta?.title ?? 'BiasGuards.AI - AI Bias Detection';
	$: pageDescription =
		$page.data?.meta?.description ??
		'AI bias detection tool. 15% revenue to criminal justice reform.';

	let animations: BiasGuardAnimations;

	onMount(() => {
		animations = new BiasGuardAnimations();
		const reveals = document.querySelectorAll('.reveal-on-scroll');
		if (reveals.length) animations.addScrollReveal(reveals, 'fade-up');
		return () => animations?.destroy();
	});
</script>

<svelte:head>
	<title>{pageTitle}</title>
	<meta name="description" content={pageDescription} />
	<meta property="og:title" content={pageTitle} />
	<meta property="og:description" content={pageDescription} />
	<meta property="twitter:title" content={pageTitle} />
	<meta property="twitter:description" content={pageDescription} />
</svelte:head>

<div
	class="min-h-screen bg-gradient-to-br from-white via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-blue-900/20 dark:to-indigo-900/30"
>
	<div class="bg-justice-blue-600 text-white py-2 px-4 text-center text-sm font-medium">
		<span class="hidden sm:inline">{MISSION_CONTEXT.mission} • {MISSION_CONTEXT.courtDate} • </span>
		<span class="font-semibold">{MISSION_CONTEXT.revenueToJustice} to justice reform</span>
	</div>

	<main class="flex-1">
		<slot />
	</main>

	<footer
		class="bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-6 px-4"
	>
		<div class="max-w-7xl mx-auto text-center">
			<div
				class="flex flex-col sm:flex-row items-center justify-center gap-4 text-sm text-gray-600 dark:text-gray-400"
			>
				<span>Justice-Driven Technology</span>
				<span class="hidden sm:block">•</span>
				<span>{MISSION_CONTEXT.legalCrisis} Crisis</span>
				<span class="hidden sm:block">•</span>
				<span>{MISSION_CONTEXT.courtDate}</span>
			</div>
		</div>
	</footer>
</div>

<style>
	:global(body) {
		font-family: 'Inter', system-ui, sans-serif;
	}

	:global(code) {
		font-family: 'Source Code Pro', monospace;
	}
</style>
