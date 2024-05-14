export class Parameters {
	static host: string = import.meta.env.VITE_EYEGWAY_HOST || 'http://localhost:55221';
	static hubTriggerKey: string = import.meta.env.VITE_HUB_TRIGGER_KEY || '';
}
