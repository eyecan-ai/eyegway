import { EyegwayImage, EyegwayTensor } from "$lib/Eyegway.js";

export class GenericData {

}

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

export type DataGenericType = DataImage | DataTensor | DataPointCloud | DataMetadata;


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
                console.log('Sub', key, value, value[key]);
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
        }
        else if (value instanceof EyegwayTensor) {
            return new DataTensor(value);
        }
        else if (value instanceof Object) {
            if (value.vertices && value.vertices instanceof EyegwayTensor) {
                return new DataPointCloud(value.vertices, value.colors);
            }
            else {
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
    static pickAndParse(data: any, key: string): DataGenericType | null {
        const pickedData = DataExtractor._(data, key);
        return DataExtractor.parse(pickedData);
    }

}


export class MosaicItem {
    name: string = '';
    x: number = 0;
    y: number = 0;
    w: number = 3;
    h: number = 3;

    constructor(name: string = '', x: number = 0, y: number = 0, w: number = 3, h: number = 3) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
    }
}