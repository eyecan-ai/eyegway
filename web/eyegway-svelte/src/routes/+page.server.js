
import { Parameters } from '$lib/Parameters.ts';

/** @type {import('./$types').PageServerLoad} */
export function load({ params }) {
    return {
        config: {
            host: process.env.EYEGWAY_HOST || Parameters.host,
            title: process.env.EYEGWAY_WEBUI_TITLE || 'Debug Viewer',
            hubTriggerKey: process.env.EYEGWAY_HUB_TRIGGER_KEY || Parameters.hubTriggerKey,
        }
    };
}