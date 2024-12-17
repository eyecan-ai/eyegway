import { browser } from '$app/environment';
import { writable, type Writable, get } from 'svelte/store';
import { persisted } from 'svelte-persisted-store';
import { find, pipe } from 'remeda';
import { z } from 'zod';

const ConfigurationModelSchema = z.object({
    id: z.number(),
}).default({ id: Date.now() });

export type ConfigurationModel = z.infer<typeof ConfigurationModelSchema>;


export class ConfigurationUtils<ConfigurationModel> {
    protected configurationName: string;
    protected defaultValueSchema: z.ZodType<ConfigurationModel>;
    protected configOptionsURLs?: string[];
    protected defaultOption?: string;
    protected configOptions: Record<string, ConfigurationModel> = {};
    protected store?: Writable<ConfigurationModel>;

    constructor(configurationName: string, defaultValueSchema: z.ZodType<ConfigurationModel>, configOptionsURls?: string[], defaultOption?: string) {
        this.configurationName = configurationName;
        this.defaultValueSchema = defaultValueSchema;
        this.configOptionsURLs = configOptionsURls;
        this.defaultOption = defaultOption;
        this.store = undefined;
    }

    async loadConfigOptions(): Promise<void> {
        if (this.configOptionsURLs) {
            for (const option of this.configOptionsURLs) {
                try {
                    const config = await this.loadConfigurationFromUrl(option);
                    this.configOptions[option] = config;
                } catch (error) {
                    console.error(`Failed to load configuration from ${option}: ${error}`);
                }
            }
        }
    }

    private async loadConfigurationFromUrl(url: string): Promise<ConfigurationModel> {
        return new Promise((resolve, reject) => {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const result = this.defaultValueSchema.safeParse(data);
                    if (result.success) {
                        resolve(result.data);
                    } else {
                        reject(result.error.format());
                    }
                })
                .catch(error => {
                    reject(error);
                });
        });
    }

    private async createPersistedStore(): Promise<Writable<ConfigurationModel>> {
        // Use svelte-persisted-store for persistence
        if (browser) {
            await this.loadConfigOptions();
            const initialValue = this.configOptionsURLs && this.defaultOption && this.configOptions[this.defaultOption] ? this.configOptions[this.defaultOption] : undefined;
            return persisted<ConfigurationModel>(this.configurationName, this.defaultValueSchema.parse(initialValue));
        } else {
            // For SSR, use a regular writable store
            const initialValue = this.configOptionsURLs && this.defaultOption && this.configOptions[this.defaultOption] ? this.configOptions[this.defaultOption] : undefined;
            return writable<ConfigurationModel>(this.defaultValueSchema.parse(initialValue));
        }
    }

    async getStore(): Promise<Writable<ConfigurationModel>> {
        if (!this.store) {
            this.store = await this.createPersistedStore();
        }
        return this.store;
    }

    async resetStore(): Promise<void> {
        const store = await this.getStore();
        const initialValue = this.configOptions && this.defaultOption ? this.configOptions[this.defaultOption] : undefined;
        store.set(this.defaultValueSchema.parse(initialValue));
    }

    async saveConfigurationToFile(): Promise<void> {
        if (browser) {
            const configuration = get(await this.getStore());
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
            if (this.configOptionsURLs) {
                resolve(this.configOptionsURLs);
            } else {
                reject('No configuration options available');
            }
        });
    }

    async getActiveOption(): Promise<string> {
        const store = await this.getStore();
        return new Promise((resolve, reject) => {
            if (this.configOptions) {
                const configuration = get(store);
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
        const store = await this.getStore();
        return new Promise((resolve, reject) => {
            if (this.configOptions) {
                const configuration = this.configOptions[optionName];
                if (configuration) {
                    const result = this.defaultValueSchema.safeParse(configuration);
                    if (result.success) {
                        store.set(result.data);
                        resolve();
                    } else {
                        reject(result.error.format());
                    }
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
        const store = await this.getStore();
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
                                const result = this.defaultValueSchema.safeParse(configuration);
                                if (result.success) {
                                    store.set(result.data);
                                    resolve();
                                } else {
                                    reject(result.error.format());
                                }
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