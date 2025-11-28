// BiasGuards.AI - Global type definitions

/// <reference types="@sveltejs/kit" />
/// <reference types="vite/client" />

// Environment variables
interface ImportMetaEnv {
	readonly VITE_COURT_DATE: string;
	readonly VITE_MISSION: string;
	readonly VITE_REVENUE_TO_JUSTICE: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}

// Build-time constants
declare const __COURT_DATE__: string;
declare const __MISSION__: string;
declare const __REVENUE_TO_JUSTICE__: string;
declare const __BUILD_TIME__: string;

// GSAP types for tree-shaking
declare module 'gsap' {
	export * from 'gsap/all';
}

// Skeleton UI types
declare module '@skeletonlabs/skeleton/themes' {
	export * from '@skeletonlabs/skeleton/themes/index.js';
}

// Asset imports
declare module '*.svg' {
	const content: string;
	export default content;
}

declare module '*.png' {
	const content: string;
	export default content;
}

declare module '*.jpg' {
	const content: string;
	export default content;
}

declare module '*.jpeg' {
	const content: string;
	export default content;
}

declare module '*.webp' {
	const content: string;
	export default content;
}

declare module '*.avif' {
	const content: string;
	export default content;
}

// Svelte component types
declare global {
	namespace App {
		// BiasGuards-specific error types
		interface Error {
			code?: string;
			id?: string;
			context?: Record<string, unknown>;
		}

		// Page data interface
		interface PageData {
			meta?: {
				title?: string;
				description?: string;
				keywords?: string[];
				canonical?: string;
			};
		}

		// Application locals
		interface Locals {
			user?: {
				id: string;
				email: string;
				role: 'admin' | 'user';
			};
			session?: {
				id: string;
				expiresAt: Date;
			};
		}

		// Platform interface for deployment
		interface Platform {
			env?: {
				DATABASE_URL?: string;
				REDIS_URL?: string;
				OPENAI_API_KEY?: string;
			};
		}

		// Page state for navigation
		interface PageState {
			selected?: string;
		}
	}
}

export {};
