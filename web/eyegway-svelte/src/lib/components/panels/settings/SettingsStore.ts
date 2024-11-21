import { StyleSettingsUtils } from './SettingsUtils.js';

const styleUtils = new StyleSettingsUtils();

export const styleSettings = styleUtils.getStore();

export const styleSettingsReset = () => {
    styleUtils.resetStore();
};

export const saveStyleSettingsToFile = () => {
    styleUtils.saveConfigurationToFile();
};

export const loadStyleSettingsFromFile = async () => {
    await styleUtils.loadConfigurationFromFile();
};