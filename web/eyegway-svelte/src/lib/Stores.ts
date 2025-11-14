import { persisted } from 'svelte-persisted-store';
import { Parameters } from './Parameters.js';
import type { Writable } from 'svelte/store';

const defaultServerPreferences = {
	host: Parameters.host,
};

export const ServerPreferences = persisted('ServerPreferences', defaultServerPreferences);

export const serverPreferencesReset = () => {
	ServerPreferences.set(defaultServerPreferences);
};

export interface HubsPreferences {
	activeHub: string | null;
}

const defaultHubsPreferences: HubsPreferences = {
	activeHub: Parameters.defaultHubName
};

export const HubsPreferences: Writable<HubsPreferences> = persisted('HubsPreferences', defaultHubsPreferences);
