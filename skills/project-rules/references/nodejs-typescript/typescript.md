# TypeScript

Preferred `tsconfig.json` — strict, ESM-first:

```json
{
  "compilerOptions": {
    "esModuleInterop": true,
    "skipLibCheck": true,
    "target": "es2022",
    "allowJs": true,
    "resolveJsonModule": true,
    "moduleDetection": "force",
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "sourceMap": true,
    "declaration": true,
    "lib": ["es2022"]
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

For bundler projects (Vite, Nuxt, Next.js), use
`"module": "preserve"` and `"noEmit": true` instead.
Nuxt and Next.js generate their own tsconfig —
extend it rather than replacing it.
