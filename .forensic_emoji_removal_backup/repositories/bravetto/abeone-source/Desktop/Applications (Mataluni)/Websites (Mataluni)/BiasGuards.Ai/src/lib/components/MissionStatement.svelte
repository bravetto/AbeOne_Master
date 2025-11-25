<script lang="ts">
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';

	// Mission-critical data
	const MISSION_DATA = {
		legalCrisis: '$26,500',
		courtDate: 'August 25, 2025',
		revenueToJustice: '15%',
		missionTitle: 'JAHmere Webb Freedom Mission',
		tonnyDungyConnection: 'Tony Dungy Legacy'
	} as const;

	// Component refs
	let missionSection: HTMLElement;
	let timelineItems: HTMLElement[] = [];

	// Mission timeline
	const timeline = [
		{
			date: 'Crisis Point',
			title: 'JAHmere Webb Legal Crisis',
			description: `${MISSION_DATA.legalCrisis} legal crisis exposes systemic bias in criminal justice`,
			icon: '⚖️',
			color: 'alert-red'
		},
		{
			date: 'Inspiration',
			title: 'Tony Dungy Connection',
			description: "Drawing strength from Tony Dungy's legacy of justice and transformation",
			icon: '🏆',
			color: 'justice-blue'
		},
		{
			date: 'Mission Born',
			title: 'BiasGuards.AI Created',
			description: 'AI bias detection tool born from personal crisis to help others',
			icon: '🛡️',
			color: 'success-green'
		},
		{
			date: MISSION_DATA.courtDate,
			title: 'Court Date Target',
			description: 'Working toward justice and systemic reform',
			icon: '📅',
			color: 'justice-blue'
		}
	];

	// Performance-focused animations
	onMount(() => {
		const tl = gsap.timeline();

		tl.fromTo(
			missionSection,
			{ opacity: 0, y: 40 },
			{ opacity: 1, y: 0, duration: 0.8, ease: 'power2.out' }
		).fromTo(
			'.timeline-item',
			{ opacity: 0, x: -30 },
			{ opacity: 1, x: 0, duration: 0.5, stagger: 0.2, ease: 'power2.out' },
			'-=0.4'
		);
	});
</script>

<section bind:this={missionSection} class="py-16 bg-white dark:bg-gray-900">
	<div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Mission Header -->
		<div class="text-center mb-16">
			<div
				class="reveal-scale-up inline-flex items-center px-4 py-2 bg-justice-blue-100 dark:bg-blue-900/30 text-justice-blue-700 dark:text-blue-300 rounded-full text-sm font-semibold mb-6"
			>
				🏛️ {MISSION_DATA.missionTitle}
			</div>

			<h2
				class="reveal-on-scroll text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-6"
			>
				Born from Crisis,<br />
				<span class="text-justice-blue-600 dark:text-blue-400">Built for Justice</span>
			</h2>

			<p
				class="reveal-fade-in text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed"
			>
				BiasGuards.AI emerged from JAHmere Webb's <strong class="text-alert-red-600"
					>${MISSION_DATA.legalCrisis} legal crisis</strong
				>, transforming personal struggle into a mission to reform the criminal justice system
				through AI bias detection.
			</p>
		</div>

		<!-- Revenue Commitment -->
		<div
			class="reveal-slide-left bg-gradient-to-r from-success-green-50 via-green-50 to-success-green-100 dark:from-green-900/20 dark:via-green-800/20 dark:to-green-900/30 rounded-2xl p-8 mb-16 border border-success-green-200 dark:border-green-700"
		>
			<div class="text-center">
				<div class="text-5xl font-bold text-success-green-600 dark:text-green-400 mb-4">
					{MISSION_DATA.revenueToJustice}
				</div>
				<div class="text-xl font-semibold text-success-green-700 dark:text-green-300 mb-2">
					of Revenue Goes to Criminal Justice Reform
				</div>
				<p class="text-green-700 dark:text-green-400">
					Your support directly funds legal aid, policy reform, and systemic change initiatives
				</p>
			</div>
		</div>

		<!-- Mission Timeline -->
		<div class="relative">
			<div
				class="absolute left-4 md:left-1/2 md:transform md:-translate-x-px top-0 bottom-0 w-0.5 bg-gradient-to-b from-justice-blue-400 via-purple-400 to-success-green-400"
			></div>

			<div class="space-y-12">
				{#each timeline as item, index}
					<div class="story-milestone timeline-item reveal-on-scroll relative flex items-center">
						<div
							class="flex-shrink-0 w-8 h-8 bg-{item.color}-500 rounded-full flex items-center justify-center text-white text-lg font-bold z-10 md:absolute md:left-1/2 md:transform md:-translate-x-1/2"
						>
							{item.icon}
						</div>

						<div class="ml-6 md:ml-0 md:w-1/2 {index % 2 === 0 ? 'md:pr-8' : 'md:pl-8 md:ml-auto'}">
							<div class="biasguards-card">
								<div
									class="text-sm font-semibold text-{item.color}-600 dark:text-{item.color}-400 mb-2"
								>
									{item.date}
								</div>
								<h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">
									{item.title}
								</h3>
								<p class="text-gray-600 dark:text-gray-300">
									{item.description}
								</p>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<!-- Call to Action -->
		<div class="mt-16 text-center">
			<div class="bg-gradient-to-r from-justice-blue-600 to-indigo-700 text-white rounded-2xl p-8">
				<h3 class="text-2xl font-bold mb-4">Join the Justice Mission</h3>
				<p class="text-blue-100 mb-6 max-w-2xl mx-auto">
					Bias detection analysis contributes to criminal justice reform. Together, we can build a
					more equitable future.
				</p>
				<div class="flex flex-col sm:flex-row gap-4 justify-center">
					<button
						class="bg-white text-justice-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
					>
						Start Detecting Bias
					</button>
					<button
						class="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/10 transition-colors"
					>
						Learn More About Our Mission
					</button>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	/* Timeline responsive adjustments */
	@media (max-width: 768px) {
		.timeline-item {
			padding-left: 2rem;
		}
	}
</style>
