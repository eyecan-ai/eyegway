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

export interface ColorStyle {
    logo: string;
    panel: string;
    header: string;
    container: string;
    background: string;
    internal_gradient: string;
    external_gradient: string;
    header_buttons: string;
}

export class StyleSettings {
    // Global
    color: ColorStyle = {
        logo: 'images/logo.png',
        panel: '#fff',
        header: '#ffffff',
        container: '#ffffff',
        background: '#ffffff',
        internal_gradient: '#ffffff',
        external_gradient: '#ebebeb',
        header_buttons: '#444444'
    };
}