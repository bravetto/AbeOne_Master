<script lang="ts">
	import { onMount } from 'svelte';
	import { BiasGuardAnimations } from '$lib/utils/animations';

	const CRISIS_DATA = {
		legalCost: 26500,
		courtDate: new Date('2025-08-25'),
		revenueToJustice: 15
	} as const;

	const daysUntilCourt = $derived(() => {
		const diffTime = CRISIS_DATA.courtDate.getTime() - Date.now();
		const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
		return Math.max(diffDays, 0);
	});

	let heroSection: HTMLElement;
	let animations: BiasGuardAnimations;

	function handleCTAClick(type: 'demo' | 'story') {
		const target = type === 'demo' ? '#bias-detector' : '#mission-story';
		document.querySelector(target)?.scrollIntoView({ behavior: 'smooth' });
	}

	onMount(() => {
		if (!heroSection) return;

		animations = new BiasGuardAnimations();
		animations.animateHeroEntrance(heroSection);

		const buttons = heroSection.querySelectorAll('.cta-button');
		buttons.forEach(btn => animations.addMouseMagnetism(btn as HTMLElement));

		const counter = heroSection.querySelector('.revenue-number') as HTMLElement;
		if (counter) animations.animateNumber(counter, CRISIS_DATA.revenueToJustice, 2000, '', '%');

		return () => animations?.destroy();
	});
</script>

<section
	bind:this={heroSection}
	class="hero-section min-h-screen flex items-center justify-center bg-gradient-to-br from-justice-blue-900 via-indigo-900 to-purple-900 relative overflow-hidden"
	role="banner"
>
	<div
		class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"
		aria-hidden="true"
	></div>
	<div
		class="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"
		aria-hidden="true"
	></div>

	<div class="relative z-10 max-w-4xl mx-auto px-4 text-center">
		<div
			class="hero-alert reveal-scale-up inline-flex items-center px-4 py-2 bg-alert-red-600 text-white rounded-full text-sm font-bold mb-8"
		>
			<span class="mr-2">🚨</span>
			LEGAL CRISIS: ${CRISIS_DATA.legalCost.toLocaleString()} • {daysUntilCourt} Days to Court
		</div>

		<h1 class="hero-title reveal-on-scroll text-4xl sm:text-6xl font-bold text-white mb-8">
			AI Bias Detection Tool
		</h1>

		<div class="hero-subtitle reveal-fade-in mb-12">
			<p class="text-xl text-blue-100 mb-4">
				<strong class="text-white">JAHmere Webb</strong> •
				<strong class="text-alert-red-300">${CRISIS_DATA.legalCost.toLocaleString()} case</strong>
				drives this bias detection project.
			</p>
			<p class="text-lg text-blue-200">
				Court: <strong class="text-white">August 25, 2025</strong> •
				<strong class="text-success-green-300">{CRISIS_DATA.revenueToJustice}%</strong> revenue target
			</p>
		</div>

		<!-- Call to Action Buttons -->
		<div
			class="hero-cta cta-buttons reveal-slide-left flex flex-col sm:flex-row gap-6 justify-center items-center mb-16"
		>
			<button
				class="cta-button bg-white text-justice-blue-600 px-6 py-3 rounded-lg font-bold text-lg shadow-xl hover:shadow-2xl transition-transform duration-300"
				onclick={() => handleCTAClick('demo')}
				aria-label="Try demo"
			>
				Demo
			</button>

			<button
				class="cta-button border-2 border-white text-white px-6 py-3 rounded-lg font-bold text-lg hover:bg-white/10 transition-transform duration-300"
				onclick={() => handleCTAClick('story')}
				aria-label="My story"
			>
				Story
			</button>
		</div>

		<!-- Hero Statistics -->
		<div
			class="hero-stats reveal-slide-right grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-3xl mx-auto"
		>
			<div class="stat-item text-center">
				<div class="text-4xl font-bold text-white mb-2">
					<span class="revenue-number">0</span>%
				</div>
				<div class="text-sm text-blue-200 font-medium">Revenue Goal</div>
			</div>

			<div class="stat-item text-center">
				<div class="text-4xl font-bold text-success-green-400 mb-2">Beta</div>
				<div class="text-sm text-blue-200 font-medium">Current Status</div>
			</div>

			<div class="stat-item text-center">
				<div class="text-4xl font-bold text-yellow-400 mb-2">Active</div>
				<div class="text-sm text-blue-200 font-medium">Development</div>
			</div>
		</div>
	</div>

	<!-- Court Date Countdown -->
	<div
		class="court-countdown absolute bottom-8 left-1/2 transform -translate-x-1/2 bg-black/30 backdrop-blur-sm text-white px-6 py-3 rounded-full"
	>
		<div class="flex items-center gap-2 text-sm font-medium">
			<span>⚖️</span>
			<span>Court Date: August 25, 2025</span>
			<span class="text-alert-red-300 font-bold">({daysUntilCourt} days remaining)</span>
		</div>
	</div>

	<!-- Scroll Indicator -->
	<div
		class="absolute bottom-4 left-1/2 transform -translate-x-1/2 animate-bounce"
		aria-hidden="true"
	>
		<svg class="w-6 h-6 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M19 14l-7 7m0 0l-7-7m7 7V3"
			></path>
		</svg>
	</div>
</section>

<style>
	.cta-button {
		will-change: transform, box-shadow;
		transform: translateZ(0);
	}

	@media (prefers-reduced-motion: reduce) {
		.animate-bounce {
			animation: none;
		}
	}

	@media (max-width: 640px) {
		.cta-buttons {
			flex-direction: column;
			gap: 1rem;
		}

		.cta-button {
			width: 100%;
			max-width: 320px;
		}
	}

	@media (prefers-contrast: high) {
		.cta-button {
			border: 2px solid currentColor;
		}
	}

	.cta-button:focus {
		outline: 3px solid #fbbf24;
		outline-offset: 2px;
	}
</style>
