import { browser } from '$app/environment';
import { writable, type Writable, get } from 'svelte/store';
import { persisted } from 'svelte-persisted-store';
import { isDeepEqual, clone, find, pipe } from 'remeda';

export class ConfigurationUtils<T> {
    protected configurationName: string;
    protected defaultValueType: new () => T;
    protected configOptions?: Record<string, unknown>;
    protected defaultOption?: string;
    protected store: Writable<T>;

    constructor(configurationName: string, defaultValue: new () => T, configOptions?: Record<string, unknown>, defaultOption?: string) {
        this.configurationName = configurationName;
        this.defaultValueType = defaultValue;
        this.configOptions = configOptions;
        this.defaultOption = defaultOption;
        this.store = this.createPersistedStore();
    }

    private createPersistedStore(): Writable<T> {
        // Use svelte-persisted-store for persistence
        if (browser) {
            return persisted<T>(this.configurationName, new this.defaultValueType());
        } else {
            // For SSR, use a regular writable store
            return writable<T>(new this.defaultValueType());
        }
    }

    getStore(): Writable<T> {
        return this.store;
    }

    resetStore(): void {
        if (this.configOptions && this.defaultOption && this.configOptions[this.defaultOption]) {
            const configuration = this.configOptions[this.defaultOption] as T;
            if (configuration) {
                this.store.set(configuration);
            }
        }
        else {
            this.store.set(new this.defaultValueType());
        }
    }

    async saveConfigurationToFile(): Promise<void> {
        if (browser) {
            const configuration = get(this.store);
            const configurationName = prompt('Please enter configuration name', this.configurationName + '_' + new Date().toISOString());
            if (configurationName == null) {
                return;
            }
            const blob = new Blob([JSON.stringify(configuration)], { type: 'application/json' });
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
                console.log("Active Configuration is: ", configuration);
                console.log("Possible configurations are: ", clone(this.configOptions));
                const activeOption = pipe(Object.entries(this.configOptions), find(([_, value]) => isDeepEqual(clone(value), configuration)));
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
                const configuration = this.configOptions[optionName] as T;
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
                                const configuration = JSON.parse(reader.result as string) as T;
                                this.store.set(configuration);
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