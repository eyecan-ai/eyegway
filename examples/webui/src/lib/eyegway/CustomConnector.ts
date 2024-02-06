import { EyegwayConnector, EyegwayImage, EyegwayTensor } from "./EyegwayClient";


export class EImage {
    url: string;
    constructor(url: string) {
        this.url = url;
    }
}

export class ETensor {
    data: any;
    type: string;
    shape: Array<number>;

    constructor(data: any, type: string, shape: Array<number>) {
        this.data = data;
        this.type = type;
        this.shape = shape;
    }
}

export class EPointCloud extends ETensor {
    vertices: Float32Array | null = null;
    colors: Float32Array | null = null;
    //
    constructor(data: any, type: string, shape: Array<number>) {
        super(data, type, shape);

        if (shape.length != 2) {
            throw new Error('PointCloud Data shape must be 2');
        }
        const [rows, cols] = shape;

        const N = data.length / cols;
        if (cols >= 3) {
            this.vertices = new Float32Array(N * 3);
            for (let i = 0; i < N; i++) {
                this.vertices[i * 3] = data[i * cols];
                this.vertices[i * 3 + 1] = data[i * cols + 1];
                this.vertices[i * 3 + 2] = data[i * cols + 2];
            }
        }
        if (cols >= 6) {
            this.colors = new Float32Array(N * 3);
            for (let i = 0; i < N; i++) {
                this.colors[i * 3] = data[i * cols + 3] / 255;
                this.colors[i * 3 + 1] = data[i * cols + 4] / 255;
                this.colors[i * 3 + 2] = data[i * cols + 5] / 255;
            }
        }
    }
}


export class CustomConnector extends EyegwayConnector {
    hub2world(data: any): any {
        let output_data: { [key: string]: any } = {};

        for (const [key, value] of Object.entries(data)) {
            //
            if (value instanceof EyegwayImage) {
                output_data[key] = new EImage(value.data);
            }
            //
            else if (value instanceof EyegwayTensor) {
                if (value.shape.length == 2) {
                    const [rows, cols] = value.shape;
                    if (cols == 3 || cols == 6 || cols == 7) {
                        output_data[key] = new EPointCloud(value.data, value.type, value.shape);
                        continue;
                    }
                }
                output_data[key] = new ETensor(value.data, value.type, value.shape);
            }
            //
            else {
                output_data[key] = value;
            }
        }
        return output_data;
    }
}
