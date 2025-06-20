import { z } from "zod";

export const EyegwayStyleSchema = z.object({
    logo: z.string().default('images/eyegway-logo.svg'),
    header: z.object({
        "background-color": z.object({
            r: z.number(),
            g: z.number(),
            b: z.number(),
            a: z.number(),
        }),
    }),
    panel: z.object({
        "background-color": z.object({
            r: z.number(),
            g: z.number(),
            b: z.number(),
            a: z.number(),
        }),
    }),
    content: z.object({
        "background-color": z.object({
            r: z.number(),
            g: z.number(),
            b: z.number(),
            a: z.number(),
        }),
    }),
    background: z.object({
        "first-color": z.object({
            r: z.number(),
            g: z.number(),
            b: z.number(),
            a: z.number(),
        }),
        "second-color": z.object({
            r: z.number(),
            g: z.number(),
            b: z.number(),
            a: z.number(),
        }),
    }),
}).default({
    logo: 'images/eyegway-logo.svg',
    header: { "background-color": { r: 255, g: 255, b: 255, a: 1 } },
    panel: { "background-color": { r: 255, g: 255, b: 255, a: 1 } },
    content: { "background-color": { r: 255, g: 255, b: 255, a: 1 } },
    background: {
        "first-color": { r: 255, g: 255, b: 255, a: 1 },
        "second-color": { r: 255, g: 255, b: 255, a: 1 },
    },
});

// Define the BulmaStyle schema with defaults
const BulmaStyleSchema = z.object({
    scheme: z.object({
        h: z.string(),
        s: z.string(),
        main_l: z.string(),
    }),
    primary: z.object({
        h: z.string(),
        s: z.string(),
        l: z.string(),
    }),
    info: z.object({
        h: z.string(),
        s: z.string(),
        l: z.string(),
    }),
    link: z.object({
        h: z.string(),
        s: z.string(),
        l: z.string(),
    }),
    success: z.object({
        h: z.string(),
        s: z.string(),
        l: z.string(),
    }),
    warning: z.object({
        h: z.string(),
        s: z.string(),
        l: z.string(),
    }),
    danger: z.object({
        h: z.string(),
        s: z.string(),
        l: z.string(),
    }),
    border_l: z.string(),
    text_l: z.string(),
    text_strong_l: z.string(),
    text_weak_l: z.string(),
    shadow_l: z.string(),
}).default({
    scheme: { h: "221deg", s: "14%", main_l: "100%" },
    primary: { h: "171deg", s: "100%", l: "41%" },
    info: { h: "198deg", s: "100%", l: "41%" },
    link: { h: "233deg", s: "100%", l: "41%" },
    success: { h: "153deg", s: "100%", l: "41%" },
    warning: { h: "42deg", s: "100%", l: "41%" },
    danger: { h: "348deg", s: "100%", l: "41%" },
    border_l: "86%",
    text_l: "29%",
    text_strong_l: "48%",
    text_weak_l: "21%",
    shadow_l: "4%",
});

// Define the StyleSettings schema
export const StyleSettingsSchema: z.ZodSchema = z.object({
    id: z.number().default(() => Date.now()),
    eyegway: EyegwayStyleSchema,
    bulma: BulmaStyleSchema,
}).default(
    {
        id: Date.now(),
        eyegway: EyegwayStyleSchema.parse(undefined),
        bulma: BulmaStyleSchema.parse(undefined),
    }
)

export type EyegwayStyle = z.infer<typeof EyegwayStyleSchema>;
export type BulmaStyle = z.infer<typeof BulmaStyleSchema>;

export type StyleConfiguration = z.infer<typeof StyleSettingsSchema>;