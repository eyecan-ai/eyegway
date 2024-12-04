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

export interface EyegwayStyle {
    logo: string;
    header: { "background-color": { r: number, g: number, b: number, a: number } };
    panel: { "background-color": { r: number, g: number, b: number, a: number } };
    content: { "background-color": { r: number, g: number, b: number, a: number } };
    background: {
        "first-color": { r: number, g: number, b: number, a: number },
        "second-color": { r: number, g: number, b: number, a: number }
    };
}

export interface BulmaStyle {
    scheme: { h: string, s: string, main_l: string };
    primary: { h: string, s: string, l: string };
    info: { h: string, s: string, l: string };
    link: { h: string, s: string, l: string };
    success: { h: string, s: string, l: string };
    warning: { h: string, s: string, l: string };
    danger: { h: string, s: string, l: string };
    //
    border_l: string;
    text_l: string;
    text_strong_l: string,
    text_weak_l: string,
    shadow_l: string;
}

export class StyleSettings {
    id: number = Date.now();
    eyegway: EyegwayStyle = {
        logo: 'images/logo.png',
        header: { "background-color": { r: 255, g: 255, b: 255, a: 1 } },
        panel: { "background-color": { r: 255, g: 255, b: 255, a: 1 } },
        content: { "background-color": { r: 255, g: 255, b: 255, a: 1 } },
        background: {
            "first-color": { r: 255, g: 255, b: 255, a: 1 },
            "second-color": { r: 255, g: 255, b: 255, a: 1 }
        },
    };

    bulma: BulmaStyle = {
        scheme: {
            h: "221deg",
            s: "14%",
            main_l: "100%",
        },
        primary: {
            h: "171deg",
            s: "100%",
            l: "41%"
        },
        info: {
            h: "198deg",
            s: "100%",
            l: "41%"
        },
        link: {
            h: "233deg",
            s: "100%",
            l: "41%"
        },
        success: {
            h: "153deg",
            s: "100%",
            l: "41%"
        },
        warning: {
            h: "42deg",
            s: "100%",
            l: "41%"
        },
        danger: {
            h: "348deg",
            s: "100%",
            l: "41%"
        },

        border_l: "86%",
        text_l: "29%",
        text_strong_l: "48%",
        text_weak_l: "21%",
        shadow_l: "4%",
    };
}