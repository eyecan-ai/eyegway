import { z } from "zod";

export class GenericSettings { }


export class ImageSettings extends GenericSettings {
    fit: "contain" | "cover";

    constructor(settings: Partial<ImageSettings> = { fit: 'contain' }) {
        super();
        this.fit = settings.fit ?? 'contain';
    }
}

export class MatrixSettings extends GenericSettings {
    numFractionDigits: number;
    maxElements: number;

    constructor(settings: Partial<MatrixSettings> = { numFractionDigits: 3, maxElements: 64 }) {
        super();
        this.numFractionDigits = settings.numFractionDigits ?? 2;
        this.maxElements = settings.maxElements ?? 64;
    }
}

export class MetadataSettings extends GenericSettings {
    mode: "tree" | "text" | "table";

    constructor(settings: Partial<MetadataSettings> = { mode: 'tree' }) {
        super();
        this.mode = settings.mode ?? 'tree';
    }
}

export class PlotSettings extends GenericSettings {
    fillParent: boolean;
    debounce: number;

    constructor(settings: Partial<PlotSettings> = { fillParent: true, debounce: 10 }) {
        super();
        this.fillParent = settings.fillParent ?? true;
        this.debounce = settings.debounce ?? 10;
    }
}

export class PointCloudSettings extends GenericSettings {
    background: string;
    gridColor: string;
    gridTile: number;
    gridSize: number;
    pointSize: number;
    distance: number;

    constructor(settings: Partial<PointCloudSettings> = {
        background: '#222',
        gridColor: '#888',
        gridTile: 0.1,
        gridSize: 1,
        pointSize: 0.01,
        distance: 1.0
    }) {
        super();
        this.background = settings.background ?? '#222';
        this.gridColor = settings.gridColor ?? '#888';
        this.gridTile = settings.gridTile ?? 0.1;
        this.gridSize = settings.gridSize ?? 1;
        this.pointSize = settings.pointSize ?? 0.01;
        this.distance = settings.distance ?? 1.0;
    }
}

// Define the EyegwayStyle schema with defaults
export const EyegwayStyleSchema = z.object({
    logo: z.string().default('images/eyegway-logo.svg'),
    header: z.object({
        "background-color": z.object({
            r: z.number().default(255),
            g: z.number().default(255),
            b: z.number().default(255),
            a: z.number().default(1),
        }),
    }),
    panel: z.object({
        "background-color": z.object({
            r: z.number().default(255),
            g: z.number().default(255),
            b: z.number().default(255),
            a: z.number().default(1),
        }),
    }),
    content: z.object({
        "background-color": z.object({
            r: z.number().default(255),
            g: z.number().default(255),
            b: z.number().default(255),
            a: z.number().default(1),
        }),
    }),
    background: z.object({
        "first-color": z.object({
            r: z.number().default(255),
            g: z.number().default(255),
            b: z.number().default(255),
            a: z.number().default(1),
        }),
        "second-color": z.object({
            r: z.number().default(255),
            g: z.number().default(255),
            b: z.number().default(255),
            a: z.number().default(1),
        }),
    }),
});

// Define the BulmaStyle schema with defaults
const BulmaStyleSchema = z.object({
    scheme: z.object({
        h: z.string().default("221deg"),
        s: z.string().default("14%"),
        main_l: z.string().default("100%"),
    }),
    primary: z.object({
        h: z.string().default("171deg"),
        s: z.string().default("100%"),
        l: z.string().default("41%"),
    }),
    info: z.object({
        h: z.string().default("198deg"),
        s: z.string().default("100%"),
        l: z.string().default("41%"),
    }),
    link: z.object({
        h: z.string().default("233deg"),
        s: z.string().default("100%"),
        l: z.string().default("41%"),
    }),
    success: z.object({
        h: z.string().default("153deg"),
        s: z.string().default("100%"),
        l: z.string().default("41%"),
    }),
    warning: z.object({
        h: z.string().default("42deg"),
        s: z.string().default("100%"),
        l: z.string().default("41%"),
    }),
    danger: z.object({
        h: z.string().default("348deg"),
        s: z.string().default("100%"),
        l: z.string().default("41%"),
    }),
    border_l: z.string().default("86%"),
    text_l: z.string().default("29%"),
    text_strong_l: z.string().default("48%"),
    text_weak_l: z.string().default("21%"),
    shadow_l: z.string().default("4%"),
});

// Define the StyleSettings schema
export const StyleSettingsSchema: z.ZodSchema = z.object({
    id: z.number().default(() => Date.now()),
    eyegway: EyegwayStyleSchema,
    bulma: BulmaStyleSchema,
});

export type EyegwayStyle = z.infer<typeof EyegwayStyleSchema>;
export type BulmaStyle = z.infer<typeof BulmaStyleSchema>;

export type StyleSettings = z.infer<typeof StyleSettingsSchema>;