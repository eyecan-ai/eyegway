import { persisted } from 'svelte-persisted-store'
import { Parameters } from './Parameters.js'

export const ServerPreferences = persisted('ServerPreferences', {
    host: Parameters.host,
})

export const HubsPreferences = persisted('HubsPreferences', {
    activeHub: null,
})