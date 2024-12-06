import { EyegwayImage, EyegwayTensor } from '$lib/Eyegway.js';
import {
    ImageSettings,
    MetadataSettings,
    PointCloudSettings,
    MatrixSettings,
    PlotSettings,
    type GenericSettings
} from './settings/SettingsModel.js';
import { type ConfigurationModel } from '../utils/ConfigurationUtils.js';
export class GenericData { }


export class DataImage extends GenericData {
    url: string = '';
    constructor(url: string) {
        super();
        this.url = url;
    }
}

export class DataTensor extends GenericData {
    tensor: EyegwayTensor;

    constructor(tensor: EyegwayTensor) {
        super();
        this.tensor = tensor;
    }
}

export class DataPointCloud extends GenericData {
    vertices: EyegwayTensor;
    colors: EyegwayTensor | null = null;

    constructor(vertices: EyegwayTensor, colors: EyegwayTensor | null = null) {
        super();
        this.vertices = vertices;
        this.colors = colors;
    }
}

export class DataMetadata extends GenericData {
    data: any = {};
    constructor(data: any) {
        super();
        this.data = data;
    }
}

export class DataPlot extends GenericData {
    data: any = {};
    layout: any = {};
    config: any = {};

    constructor(data: any, layout: any, config: any) {
        super();
        this.data = data;
        this.layout = layout;
        this.config = config;
    }
}

export type DataGenericType =
    | DataImage
    | DataTensor
    | DataPointCloud
    | DataMetadata
    | DataPlot;

/**
 * Extract data from a source object
 */
export class DataExtractor {
    /**
     * Lodash get like
     * @param obj The source object
     * @param dotNotation The dot notation path
     * @returns The value of the path if exists, undefined otherwise
     */
    static _(obj: any, dotNotation: string) {
        const keys = dotNotation.split('.');
        let value = obj;

        for (const key of keys) {
            if (key in value) {
                value = value[key];
            } else {
                return undefined;
            }
        }

        return value;
    }

    /**
     * Parse a value to a DataGenericType if possible
     * @param value The value to parse
     * @returns The parsed value or null if it's not possible
     */
    static parse(value: any): DataGenericType | null {
        if (value instanceof EyegwayImage) {
            return new DataImage(value.imageUrl());
        } else if (value instanceof EyegwayTensor) {
            return new DataTensor(value);
        } else if (value instanceof Object) {
            if (value.vertices && value.vertices instanceof EyegwayTensor) {
                return new DataPointCloud(value.vertices, value.colors);
            } else if (value.data && value.layout && value.config) {
                return new DataPlot(value.data, value.layout, value.config);
            } else {
                return new DataMetadata(value);
            }
        } else {
            if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
                return new DataMetadata(value);
            }
        }
        return null;
    }

    /**
     * Pick a value from a data object and parse it to a DataGenericType
     * @param data the source data
     * @param key the key to pick
     * @returns the parsed value or null if it's not possible
     */
    static pickAndParse(data: any | null, key: string): DataGenericType | null {
        if (data === null) {
            return null;
        }
        const pickedData = DataExtractor._(data, key);
        return DataExtractor.parse(pickedData);
    }

    static getSettingsType(data: DataGenericType, settings: GenericSettings): GenericSettings {
        if (data instanceof DataImage) {
            return new ImageSettings(settings);
        } else if (data instanceof DataTensor) {
            return new MatrixSettings(settings);
        } else if (data instanceof DataPointCloud) {
            return new PointCloudSettings(settings);
        } else if (data instanceof DataMetadata) {
            return new MetadataSettings(settings);
        } else if (data instanceof DataPlot) {
            return new PlotSettings(settings);
        }
        return settings;
    }
}

export class PaneConfiguration implements ConfigurationModel {
    id: number = Date.now();
    split: '' | 'horizontal' | 'vertical' = '';
    size: number = 100;
    children: PaneConfiguration[] = [];
    item: TileItem = { name: '', settings: {} }
}

export class TileItem {
    name: string = '';
    settings: GenericSettings = {};

    constructor(name: string = '', settings: GenericSettings = {}) {
        this.name = name;
        this.settings = settings;
    }
}

export function splitPane(pane: PaneConfiguration, direction: 'horizontal' | 'vertical') {
    pane.split = direction;
    pane.children = [
        {
            id: Date.now(),
            split: '',
            size: 100,
            children: [],
            item: { name: pane.item.name, settings: pane.item.settings }, // Clone the item
        },
        {
            id: Date.now() + 1,
            split: '',
            size: 100,
            children: [],
            item: { name: '', settings: {} },
        }
    ];
}

// Recursive function to remove a pane from the tree
export function removePane(parentPane: PaneConfiguration, paneToDelete: PaneConfiguration) {
    if (!parentPane.children) return false;

    const index = parentPane.children.findIndex((child) => child.id === paneToDelete.id);
    if (index !== -1) {
        parentPane.children.splice(index, 1);
        if (parentPane.children.length === 1) {
            // Collapse parent pane if only one child remains
            const remainingChild = parentPane.children[0];
            parentPane.split = remainingChild.split;
            parentPane.children = remainingChild.children;
            parentPane.item = remainingChild.item;
        } else if (parentPane.children.length === 0) {
            parentPane.split = '';
            parentPane.item = { name: '', settings: {} };
        }
        return true;
    }

    // Recursively search in child panes
    for (let child of parentPane.children) {
        if (removePane(child, paneToDelete)) {
            return true;
        }
    }

    return false;
}