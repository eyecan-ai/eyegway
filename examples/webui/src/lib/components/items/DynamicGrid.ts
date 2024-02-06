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