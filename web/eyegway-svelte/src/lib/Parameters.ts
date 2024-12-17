export class Parameters {
	static host: string = import.meta.env.EYEGWAY_HOST || 'http://localhost:55221';
	static hubTriggerKey: string = import.meta.env.EYEGWAY_HUB_TRIGGER_KEY || '';
	static title: string = import.meta.env.EYEGWAY_TITLE || 'eyegway';
	static themes: string = import.meta.env.EYEGWAY_THEMES || 'ayu_light,ayu_mirage,bulma,dracula,monokai_pro,one_dark_pro';
	static defaultTheme: string = import.meta.env.EYEGWAY_DEFAULT_THEME || 'bulma';
	static layouts: string = import.meta.env.EYEGWAY_LAYOUTS || 'empty,2x2'
	static defaultLayout: string = import.meta.env.EYEGWAY_DEFAULT_LAYOUT || 'empty';
}