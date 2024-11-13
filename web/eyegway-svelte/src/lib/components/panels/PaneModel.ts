export class PaneConfiguration {
    id: number;
    split: string;
    children: PaneConfiguration[];
    item: { name: string };

    constructor(id: number, split: string, children: PaneConfiguration[], item: { name: string }) {
        this.id = id;
        this.split = split;
        this.children = children;
        this.item = item;
    }

    static fromJson(json: any): PaneConfiguration {
        return new PaneConfiguration(
            json.id,
            json.split,
            json.children.map((child: any) => PaneConfiguration.fromJson(child)),
            json.item
        );
    }
}

export class TileItem {
    name: string = '';

    constructor(name: string = '') {
        this.name = name;
    }
}
