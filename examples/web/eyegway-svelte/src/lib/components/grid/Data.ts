import { EyegwayImage, EyegwayTensor } from "$lib/Eyegway.js";
import type { E } from "vitest/dist/reporters-1evA5lom.js";

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
    tensor: EyegwayTensor | null = null;

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

export class EyegwayDataPurger {

    static purge(data: any) {
        let newData: any = {};
        for (let key in data) {
            const value = data[key];

            // Images
            if (value instanceof EyegwayImage) {
                newData[key] = new DataImage(value.imageUrl());
            }
            // Generic Tensor
            else if (value instanceof EyegwayTensor) {
                newData[key] = new DataTensor(value);
            }
            // Generico Object
            else if (value instanceof Object) {

                // If object has vertices and optionally colors, it's a point cloud
                if (value.vertices && value.vertices instanceof EyegwayTensor) {
                    newData[key] = new DataPointCloud(value.vertices, value.colors);
                }
                // Otherwise, it's a generic object
                else {
                    newData[key] = new DataMetadata(value);
                }
            }
        }
        return newData;
    }
}


export class ProtoypeItem {
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