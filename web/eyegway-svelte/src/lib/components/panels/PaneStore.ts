import { PaneConfigurationUtils } from './PaneUtils.js';

const paneUtils = new PaneConfigurationUtils();

export const paneConfiguration = paneUtils.getStore();

export const paneConfigurationReset = () => {
    paneUtils.resetStore();
};

export const savePaneConfigurationToFile = () => {
    paneUtils.saveConfigurationToFile();
};

export const loadPaneConfigurationFromFile = async () => {
    await paneUtils.loadConfigurationFromFile();
};