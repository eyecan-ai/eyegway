import { persisted } from 'svelte-persisted-store';
import { Parameters } from './Parameters.js';
import type { Writable } from 'svelte/store';

export const ServerPreferences = persisted('ServerPreferences', {
	host: Parameters.host
});

export interface HubsPreferences {
	activeHub: string | null;
}

export const HubsPreferences: Writable<HubsPreferences> = persisted('HubsPreferences', {
	activeHub: null
});
