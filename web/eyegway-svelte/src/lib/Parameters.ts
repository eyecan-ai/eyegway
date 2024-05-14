import { env } from '$env/dynamic/public';

export class Parameters {
	static host: string = env.PUBLIC_EYEGWAY_HOST || 'http://localhost:55221';
	static hubTriggerKey: string = env.PUBLIC_HUB_TRIGGER_KEY || '';
	static title: string = env.PUBLIC_TITLE || '⛭ Eyegway WEBUI ⛭';
}
