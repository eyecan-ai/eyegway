import axios from "axios";
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import { encode, decode, ExtensionCodec } from '@msgpack/msgpack';

enum StatusCode {
    Unauthorized = 401,
    Forbidden = 403,
    TooManyRequests = 429,
    InternalServerError = 500,
}

function apiBaseUrl(): string {
    return import.meta.env.VITE_EYEGWAY_SERVER || 'http://localhost:55221'
}

const headers: Readonly<Record<string, string | boolean>> = {
    Accept: "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "X-Requested-With": "XMLHttpRequest",
};

const injectToken = (config: AxiosRequestConfig): AxiosRequestConfig => {
    try {
        const token = localStorage.getItem("accessToken");

        if (token != null) {
            if (config.headers) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    } catch (error: any) {
        throw new Error(error);
    }
};

class Http {
    private instance: AxiosInstance | null = null;

    private get http(): AxiosInstance {
        return this.instance != null ? this.instance : this.initHttp();
    }

    initHttp() {
        const http = axios.create({
            baseURL: apiBaseUrl(),
            headers,
            withCredentials: false,
        });

        //@ts-ignore
        http.interceptors.request.use(injectToken, (error) => Promise.reject(error));

        http.interceptors.response.use(
            (response) => response,
            (error) => {
                const { message } = error;
                return this.handleError(message);
            }
        );

        this.instance = http;
        return http;
    }

    buildGenericUrl(url: string): string {
        if (!url.startsWith("/")) {
            url = "/" + url;
        }
        url = apiBaseUrl() + url;
        url = url.replace(/([^:]\/)\/+/g, "$1");
        return url;
    }

    request<T = any, R = AxiosResponse<T>>(config: AxiosRequestConfig): Promise<R> {
        return this.http.request(config);
    }

    get<T = any, R = AxiosResponse<T>>(url: string, config?: AxiosRequestConfig): Promise<R> {
        return this.http.get<T, R>(url, config);
    }

    getBlob<T = any, R = AxiosResponse<T>>(url: string, config?: AxiosRequestConfig): Promise<R> {
        return this.http.get<T, R>(url, { ...config, responseType: "blob" });
    }

    post<D = any, T = any, R = AxiosResponse<T>>(
        url: string,
        data?: D,
        config?: AxiosRequestConfig
    ): Promise<R> {
        return this.http.post<T, R>(url, data, config);
    }

    put<D = any, T = any, R = AxiosResponse<T>>(
        url: string,
        data?: D,
        config?: AxiosRequestConfig
    ): Promise<R> {
        return this.http.put<T, R>(url, data, config);
    }

    delete<T = any, R = AxiosResponse<T>>(url: string, config?: AxiosRequestConfig): Promise<R> {
        return this.http.delete<T, R>(url, config);
    }

    private handleError(error: any) {
        const { status, data } = error;

        switch (status) {
            case StatusCode.InternalServerError: {
                break;
            }
            case StatusCode.Forbidden: {
                break;
            }
            case StatusCode.Unauthorized: {
                break;
            }
            case StatusCode.TooManyRequests: {
                break;
            }
        }

        return Promise.reject(error);
    }
}

export const http = new Http();

export class EyegwayConnector {
    hub2world(data: any): any {
        return data;
    }
    world2hub(data: any): any {
        return data;
    }
}

export class EyegwayClient {
    packer: EyegwayPacker;
    connector: EyegwayConnector | null;
    private static instance: EyegwayClient | null = null;

    private constructor() {
        this.packer = EyegwayPacker.getInstance();
        this.connector = null;
    }

    public setConnector(connector: EyegwayConnector) {
        this.connector = connector;
    }

    public decodeData(data: any): any {
        data = this.packer.decode(data);
        if (this.connector) {
            data = this.connector.hub2world(data);
        }
        return data;
    }

    public static getInstance(): EyegwayClient {
        if (EyegwayClient.instance == null) {
            EyegwayClient.instance = new EyegwayClient();
        }
        return EyegwayClient.instance;
    }

    async history_size(hub_name: string): Promise<number> {
        const { data } = await http.get<number>(`/hubs/${hub_name}/history_size`);
        return data;
    }

    async buffer_size(hub_name: string): Promise<number> {
        const { data } = await http.get<number>(`/hubs/${hub_name}/buffer_size`);
        return data;
    }

    async last(hub_name: string, offset: number = 0): Promise<any> {
        const response = await http.getBlob<Blob>(`/hubs/${hub_name}/last?offset=${offset}`);
        return this.decodeData(await response.data.arrayBuffer());
    }

}

// ====================================================================================
// ====================================================================================
// ====================================================================================


export class EyegwayTensor {
    data: Array<number>;
    type: string;
    shape: Array<number>;

    constructor(data: Array<number>, type: string, shape: Array<number>) {
        this.data = data;
        this.type = type;
        this.shape = shape;
    }
}

export class EyegwayImage {
    type: string;
    data: string;
    shape: Array<number>;

    constructor(data: string, type: string, shape: Array<number>) {
        this.type = type;
        this.data = data;
        this.shape = shape;
    }
}

export class EyegwayConstants {
    static readonly TENSOR = 66;
    static readonly IMAGE = 67;
}

export class EyegwayPacker {
    extensionCodec: ExtensionCodec;

    constructor() {

        const typeMap: any = {
            float32: Float32Array,
            float64: Float64Array,
            int16: Int16Array,
            uint16: Uint16Array,
            int32: Int32Array,
            uint32: Uint32Array,
            int64: BigInt64Array,
            uint64: BigUint64Array
        };

        this.extensionCodec = new ExtensionCodec();
        let extensionCodec = this.extensionCodec;

        // Register TENSOR type
        this.extensionCodec.register({
            type: EyegwayConstants.TENSOR,
            encode: (object: unknown): Uint8Array | null => {
                throw new Error(`Encoding for ${EyegwayConstants.TENSOR} is not supported yet`);
                // if (object instanceof Set) {
                //     return encode([...object], { extensionCodec });
                // } else {
                //     return null;
                // }
            },
            decode: (buff: Uint8Array) => {
                const decoded = decode(buff, { extensionCodec }) as any;
                const { data, type, shape } = decoded;

                const offset = data.byteOffset;
                const length = data.byteLength;
                const buffer = data.buffer.slice(offset, offset + length);

                if (!typeMap[type]) throw new Error('Unknown dtype: ' + type);

                const arr = new typeMap[type](buffer);

                return new EyegwayTensor(arr, type, shape);
            }
        });

        // Register IMAGE type
        this.extensionCodec.register({
            type: EyegwayConstants.IMAGE,
            encode: (object: unknown): Uint8Array | null => {
                throw new Error(`Encoding for ${EyegwayConstants.IMAGE} is not supported yet`);
                // if (object instanceof Set) {
                //     return encode([...object], { extensionCodec });
                // } else {
                //     return null;
                // }
            },
            decode: (d: Uint8Array) => {

                const { type, data, shape } = decode(d, { extensionCodec }) as any;


                var blob = new Blob([data], { type });
                var urlCreator = window.URL || window.webkitURL;
                var imageUrl = urlCreator.createObjectURL(blob);
                var img = new Image();
                img.src = imageUrl;

                return new EyegwayImage(imageUrl, type, shape);
            }
        });
    }

    decode(buffer: ArrayLike<number> | BufferSource): unknown {
        return decode(buffer, { extensionCodec: this.extensionCodec });
    }

    encode(object: unknown): Uint8Array {
        return encode(object, { extensionCodec: this.extensionCodec });
    }


    // make this class singleton

    static instance: EyegwayPacker;
    static getInstance(): EyegwayPacker {
        if (!EyegwayPacker.instance) {
            EyegwayPacker.instance = new EyegwayPacker();
        }

        return EyegwayPacker.instance;
    }
}
