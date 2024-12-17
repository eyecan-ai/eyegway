import { env } from '$env/dynamic/public'

export class Parameters {
	static host: string = env.PUBLIC_EYEGWAY_HOST || 'http://localhost:55221';
	static hubTriggerKey: string = env.PUBLIC_EYEGWAY_HUB_TRIGGER_KEY || '';
	static title: string = env.PUBLIC_EYEGWAY_TITLE || 'eyegway';
	static themes: string = env.PUBLIC_EYEGWAY_THEMES || 'ayu_light:ayu_mirage:bulma:dracula:monokai_pro:one_dark_pro';
	static defaultTheme: string = env.PUBLIC_EYEGWAY_DEFAULT_THEME || 'bulma';
	static layouts: string = env.PUBLIC_EYEGWAY_LAYOUTS || 'empty,2x2'
	static defaultLayout: string = env.PUBLIC_EYEGWAY_DEFAULT_LAYOUT || 'empty';
}