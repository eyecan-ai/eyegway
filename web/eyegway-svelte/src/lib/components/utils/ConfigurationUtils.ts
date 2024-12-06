import { browser } from '$app/environment';
import { writable, type Writable, get } from 'svelte/store';
import { persisted } from 'svelte-persisted-store';
import { isDeepEqual, clone, find, pipe } from 'remeda';

export interface ConfigurationModel {
    id: number
}

export class ConfigurationUtils<ConfigurationModel> {
    protected configurationName: string;
    protected defaultValueType: new () => ConfigurationModel;
    protected configOptions?: Record<string, ConfigurationModel>;
    protected defaultOption?: string;
    protected store: Writable<ConfigurationModel>;

    constructor(configurationName: string, defaultValue: new () => ConfigurationModel, configOptions?: Record<string, ConfigurationModel>, defaultOption?: string) {
        this.configurationName = configurationName;
        this.defaultValueType = defaultValue;
        this.configOptions = configOptions;
        this.defaultOption = defaultOption;
        this.store = this.createPersistedStore();
    }

    private createPersistedStore(): Writable<ConfigurationModel> {
        // Use svelte-persisted-store for persistence
        if (browser) {
            return persisted<ConfigurationModel>(this.configurationName, new this.defaultValueType());
        } else {
            // For SSR, use a regular writable store
            return writable<ConfigurationModel>(new this.defaultValueType());
        }
    }

    getStore(): Writable<ConfigurationModel> {
        return this.store;
    }

    resetStore(): void {
        if (this.configOptions && this.defaultOption && this.configOptions[this.defaultOption]) {
            const configuration = this.configOptions[this.defaultOption] as ConfigurationModel;
            if (configuration) {
                this.store.set(clone(configuration));
            }
        }
        else {
            this.store.set(new this.defaultValueType());
        }
    }

    async saveConfigurationToFile(): Promise<void> {
        if (browser) {
            const configuration = get(this.store);
            // @ts-ignore
            // Omit the default property from the configuration
            const { default: _, ...configWithoutDefault } = configuration;
            const configurationName = prompt('Please enter configuration name', this.configurationName + '_' + new Date().toISOString());
            if (configurationName == null) {
                return;
            }
            const blob = new Blob([JSON.stringify(configWithoutDefault)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = configurationName + '.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    }

    async getOptions(): Promise<string[]> {
        return new Promise((resolve, reject) => {
            if (this.configOptions) {
                resolve(Object.keys(this.configOptions));
            } else {
                reject('No configuration options available');
            }
        });
    }

    async getActiveOption(): Promise<string> {
        return new Promise((resolve, reject) => {
            if (this.configOptions) {
                const configuration = get(this.store);
                // @ts-ignore
                const activeOption = pipe(Object.entries(this.configOptions), find(([_, value]) => value.id === configuration.id));
                if (activeOption) {
                    resolve(activeOption[0]);
                } else {
                    resolve('');
                }
            } else {
                reject('No configuration options available');
            }
        });
    }

    async loadConfigurationFromOptions(optionName: string): Promise<void> {
        return new Promise((resolve, reject) => {
            if (this.configOptions) {
                const configuration = this.configOptions[optionName] as ConfigurationModel;
                if (configuration) {
                    this.store.set(clone(configuration));
                    resolve();
                } else {
                    reject('Invalid option name');
                }
            } else {
                reject('No configuration options available');
            }
        });
    }

    async loadConfigurationFromFile(): Promise<void> {
        return new Promise((resolve, reject) => {
            if (browser) {
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = '.json';
                input.onchange = () => {
                    const file = input.files?.[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = () => {
                            try {
                                const configuration = JSON.parse(reader.result as string) as ConfigurationModel;
                                this.store.set(clone(configuration));
                                resolve();
                            } catch (error) {
                                reject(error);
                            }
                        };
                        reader.readAsText(file);
                    }
                };
                input.click();
            } else {
                reject('Not running in a browser environment.');
            }
        });
    }
}