export class Parameters {
	static host: string = import.meta.env.VITE_EYEGWAY_HOST || 'http://localhost:55221';
	static title: string = import.meta.env.VITE_WEBUI_TITLE || 'Debug Viewer';
	static hubTriggerKey: string = import.meta.env.VITE_HUB_TRIGGER_KEY || '';
}
