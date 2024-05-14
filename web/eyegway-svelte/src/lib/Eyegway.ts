import { encode, decode, ExtensionCodec } from '@msgpack/msgpack';
import { Parameters } from './Parameters.js';

/**
 * Map of EyegwayDataTypes to their respective numbers in the Eyegway protocol.
 */
export class EyegwayDataTypes {
	static readonly TENSOR = 66;
	static readonly IMAGE = 67;
}

/**
 * EyegwayTensor is a class that represents a tensor aka a numpy array like object
 * with a shape and a data type.
 */
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

/**
 * EyegwayImage is a class that represents an image with a data type and a shape. The
 * image is encoded as Blob ObjectURL when coming from the server. When pushing an image
 * to the server, it needs to be a Uint8Array EyeGwayImage.
 */
export class EyegwayImage {
	type: string;
	data: string | Uint8Array;
	shape: Array<number>;

	constructor(data: string | Uint8Array, type: string, shape: Array<number>) {
		this.type = type;
		this.data = data;
		this.shape = shape;
	}

	/**
	 * Create a new EyegwayImage with data encoded as Uint8Array
	 * @returns <Promise<EyegwayImage>> A new EyegwayImage with data encoded as Uint8Array
	 */
	async convertToEyegwayImageUint8(): Promise<EyegwayImage> {
		if (this.data instanceof Uint8Array) return this;
		const response = await fetch(new URL(this.data));
		const blob = await response.blob();
		const buffer = await blob.arrayBuffer();
		return new EyegwayImage(new Uint8Array(buffer), this.type, this.shape);
	}

	/**
	 * Create a new EyegwayImage with data encoded as Blob
	 * @returns <Promise<EyegwayImage>> A new EyegwayImage with data encoded as Blob
	 */
	async convertoToEyegwayImageBlob(): Promise<EyegwayImage> {
		if (this.data instanceof Uint8Array) {
			const blob = new Blob([this.data], { type: this.type });
			const urlCreator = window.URL || window.webkitURL;
			const imageUrl = urlCreator.createObjectURL(blob);
			return new EyegwayImage(imageUrl, this.type, this.shape);
		}
		return this;
	}

	/**
	 * Check if the data is a Uint8Array
	 * @returns <boolean> True if the data is a Uint8Array
	 */
	isUint8Array() {
		return this.data instanceof Uint8Array;
	}

	imageUrl(): string {
		if (this.data instanceof Uint8Array) {
			const blob = new Blob([this.data], { type: this.type });
			const urlCreator = window.URL || window.webkitURL;
			return urlCreator.createObjectURL(blob);
		}
		return this.data;
	}
}

/**
 * EyegwayPacker is a class that is used to encode and decode data to and from the Eyegway
 * protocol. It uses the msgpack library to encode and decode data. It also registers
 * custom encoders and decoders for custom data like e.g.: EyegwayTensor and EyegwayImage.
 */
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
			uint64: BigUint64Array,
			uint8: Uint8Array
		};

		this.extensionCodec = new ExtensionCodec();
		let extensionCodec = this.extensionCodec;

		/**
		 * Register TENSOR type encoder and decoder
		 */
		this.extensionCodec.register({
			type: EyegwayDataTypes.TENSOR,

			/**
			 * When a EyegwayTensor is provided as object to encode, it will
			 */
			encode: (object: unknown): Uint8Array | null => {
				if (object instanceof EyegwayTensor) {
					const { data, type, shape } = object;
					const arr = new typeMap[type](data);
					return encode({ data: arr, type, shape }, { extensionCodec });
				}

				return null;
			},

			/**
			 * When a ExtType is provided as data to decode, it will create a new EyegwayTensor
			 */
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

		/**
		 * Register IMAGE type encoder and decoder
		 */
		this.extensionCodec.register({
			type: EyegwayDataTypes.IMAGE,

			/**
			 * When a EyegwayImage is provided as object to encode, it will
			 */
			encode: (object: unknown): Uint8Array | null => {
				if (object instanceof EyegwayImage) {
					if (!object.isUint8Array()) {
						throw new Error('EyegwayImage data must be Uint8Array');
					}
					const { data, type, shape } = object;
					return encode({ type, data, shape }, { extensionCodec });
				}
				return null;
			},

			/**
			 * When a ExtType is provided as data to decode, it will create a new EyegwayImage
			 */
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

	/**
	 * Decode a buffer to a JavaScript object (msgpack)
	 * @param buffer the buffer to decode
	 * @returns decoded object
	 */
	decode(buffer: ArrayLike<number> | BufferSource): unknown {
		return decode(buffer, { extensionCodec: this.extensionCodec });
	}

	/**
	 * Encode a JavaScript object to a buffer (msgpack)
	 * @param object the object to encode
	 * @returns the encoded buffer
	 */
	encode(object: unknown): Uint8Array {
		return encode(object, { extensionCodec: this.extensionCodec });
	}

	static instance: EyegwayPacker;
	static getInstance(): EyegwayPacker {
		if (!EyegwayPacker.instance) {
			EyegwayPacker.instance = new EyegwayPacker();
		}

		return EyegwayPacker.instance;
	}
}

// ====================================================================================
// ====================================================================================
// ====================================================================================

/**
 * EyegwayHubClient is a class that is used to connect to an EyegwayHub server. It provides
 * methods to push and pop data from the server. The data is encoded and decoded using the
 * EyegwayPacker (msgpack with custom encoders and decoders).
 */
export class EyegwayHubClient {
	hubName: string;
	packer: EyegwayPacker;
	baseUrl: string;

	public constructor(hubName: string, baseUrl: string = Parameters.host) {
		this.hubName = hubName;
		this.baseUrl = baseUrl;
		if (this.baseUrl.endsWith('/')) {
			this.baseUrl = this.baseUrl.slice(0, -1);
		}
		this.packer = EyegwayPacker.getInstance();
	}

	public buildUrl(path: string): string {
		if (!path.startsWith('/')) path = '/' + path;
		return this.baseUrl + path;
	}

	/**
	 * Decode the packed data into plain JavaScript objects
	 * @param data the packed data
	 * @returns <any> The decoded data
	 */
	public decodeData(data: ArrayBuffer): any {
		return this.packer.decode(data);
	}

	/**
	 * Encode plain JavaScript objects into packed data
	 * @param data the plain JavaScript objects
	 * @returns  <Uint8Array> The packed data
	 */
	public encodeData(data: any): Uint8Array {
		return this.packer.encode(data);
	}

	/**
	 * Get the size of the hub history
	 * @returns <Promise<number>> The size of the history buffer
	 */
	async historySize(): Promise<number> {
		const response = await fetch(this.buildUrl(`/hubs/${this.hubName}/history_size`));
		return response.json();
	}

	/**
	 * Clear the history of the hub
	 */
	async clearHistory() {
		await fetch(this.buildUrl(`/hubs/${this.hubName}/clear_history`), { method: 'POST' });
	}

	/**
	 * Get the size of the hub buffer
	 * @returns <Promise<number>> The size of the buffer
	 */
	async bufferSize(): Promise<number> {
		const response = await fetch(this.buildUrl(`/hubs/${this.hubName}/buffer_size`));
		return response.json();
	}

	/**
	 * Clear the buffer of the hub
	 */
	async clearBuffer() {
		await fetch(this.buildUrl(`/hubs/${this.hubName}/clear_buffer`), { method: 'POST' });
	}

	/**
	 * Clear the history and buffer of the hub
	 * @returns <Promise<any>>
	 */
	async clear(): Promise<any> {
		await this.clearHistory();
		await this.clearBuffer();
	}

	/**
	 * Get the last data from the hub
	 * @param offset the offset of the data in the history. offset=0 means the last data,
	 * offset=1 means the second last data, etc.
	 *
	 * @returns <Promise<any | null>> The last data from the hub or null if no data is available
	 */
	async last(offset: number = 0): Promise<any | null> {
		const response = await fetch(this.buildUrl(`/hubs/${this.hubName}/last?offset=${offset}`));
		if (response.status === 200) {
			return this.decodeData(await response.arrayBuffer());
		} else {
			return null;
		}
	}

	/**
	 * Get and remove the buffered data from the hub
	 *
	 * @param timeout the timeout in seconds to wait for data to be available
	 * @returns <Promise<any | null>> The buffered data from the hub or null if no data is available
	 */
	async pop(timeout: number = 1): Promise<any | null> {
		const response = await fetch(this.buildUrl(`/hubs/${this.hubName}/pop?timeout=${timeout}`));
		if (response.status === 200) {
			return this.decodeData(await response.arrayBuffer());
		} else {
			return null;
		}
	}

	/**
	 * Push data to the hub
	 *
	 * @param data the data to push to the hub
	 */
	async push(data: any): Promise<any> {
		await fetch(this.buildUrl(`/hubs/${this.hubName}/push`), {
			method: 'POST',
			body: this.encodeData(data)
		});
	}

	/**
	 * Return a list of all available hubs
	 * @returns <Promise<Array<string>>>
	 */
	async listHubs(hubTriggerKey: string = Parameters.hubTriggerKey): Promise<Array<string>> {
		const response = await fetch(this.buildUrl('/hubs'));
		let hubs: Array<string> = await response.json();
		if (hubTriggerKey) {
			hubs = hubs.filter((hub) => hub.includes(hubTriggerKey));
		}

		return hubs;
	}

	async freezeHistory() {
		await fetch(this.buildUrl(`/hubs/${this.hubName}/freeze_history`), {
			method: 'POST'
		});
	}

	async unfreezeHistory() {
		await fetch(this.buildUrl(`/hubs/${this.hubName}/unfreeze_history`), {
			method: 'POST'
		});
	}

	async isHistoryFrozen(): Promise<boolean> {
		const response = await fetch(this.buildUrl(`/hubs/${this.hubName}/history_frozen`));
		return response.json();
	}

	/**
	 * Return a list of all available variables in the hub
	 * @returns <Promise<Array<string>>>
	 */
	async listVariables(): Promise<Array<string>> {
		const response = await fetch(this.buildUrl(`/hubs/${this.hubName}/variables`));
		return response.json();
	}

	/**
	 * Gets the value of a variable in the hub
	 * @param variableName the name of the variable
	 * @returns the value of the variable
	 */
	async getVariableValue(variableName: string): Promise<any> {
		const response = await fetch(this.buildUrl(`/hubs/${this.hubName}/variables/${variableName}`));
		return await response.json();
	}

	/**
	 * Sets the value of a variable in the hub
	 * @param variableName the name of the variable
	 * @param value the new value of the variable
	 */
	async setVariableValue(variableName: string, value: any): Promise<any> {
		await fetch(this.buildUrl(`/hubs/${this.hubName}/variables/${variableName}`), {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ value: value })
		});
	}

	/**
	 * Deletes a variable in the hub
	 * @param variableName the name of the variable
	 */
	async deleteVariable(variableName: string): Promise<any> {
		await fetch(this.buildUrl(`/hubs/${this.hubName}/variables/${variableName}`), {
			method: 'DELETE'
		});
	}
}

// ====================================================================================
// ====================================================================================
// ====================================================================================
