import { browser } from '$app/environment';
import { writable, type Writable, get } from 'svelte/store';
import { persisted } from 'svelte-persisted-store';

export class ConfigurationUtils<T> {
    protected configurationName: string;
    protected defaultValueType: new () => T;
    protected store: Writable<T>;

    constructor(configurationName: string, defaultValue: new () => T) {
        this.configurationName = configurationName;
        this.defaultValueType = defaultValue;
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
        console.log('Resetting configuration to default value');
        this.store.set(new this.defaultValueType());
        console.log(this.defaultValueType);
        console.log(get(this.store));
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