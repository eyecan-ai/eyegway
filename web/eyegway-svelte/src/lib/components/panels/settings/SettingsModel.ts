export class GenericSettings { }


export class ImageSettings extends GenericSettings {
    fit: string;

    constructor(settings: Partial<ImageSettings> = { fit: 'contain' }) {
        super();
        this.fit = settings.fit ?? 'contain';
    }
}

export class MatrixSettings extends GenericSettings {
    decimals: number;
    colormap: string;

    constructor(settings: Partial<MatrixSettings> = { decimals: 2, colormap: 'viridis' }) {
        super();
        this.decimals = settings.decimals ?? 2;
        this.colormap = settings.colormap ?? 'viridis';
    }
}

export class MetadataSettings extends GenericSettings {
    expanded: boolean;

    constructor(settings: Partial<MetadataSettings> = { expanded: false }) {
        super();
        this.expanded = settings.expanded ?? false;
    }
}

export class PlotSettings extends GenericSettings {
    interactive: boolean;
    showLegend: boolean;

    constructor(settings: Partial<PlotSettings> = { interactive: true, showLegend: true }) {
        super();
        this.interactive = settings.interactive ?? true;
        this.showLegend = settings.showLegend ?? true;
    }
}

export class PointCloudSettings extends GenericSettings {
    background: string;
    grid_color: string;
    grid_tile: number;
    grid_size: number;
    point_size: number;
    distance: number;

    constructor(settings: Partial<PointCloudSettings> = {
        background: '#222',
        grid_color: '#888',
        grid_tile: 0.1,
        grid_size: 1,
        point_size: 0.01,
        distance: 1.0
    }) {
        super();
        this.background = settings.background ?? '#222';
        this.grid_color = settings.grid_color ?? '#888';
        this.grid_tile = settings.grid_tile ?? 0.1;
        this.grid_size = settings.grid_size ?? 1;
        this.point_size = settings.point_size ?? 0.01;
        this.distance = settings.distance ?? 1.0;
    }
}

export type SettingsType = ImageSettings | MatrixSettings | MetadataSettings | PlotSettings | PointCloudSettings;