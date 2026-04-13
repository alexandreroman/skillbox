# Code Quality

ESLint v9 flat config, Prettier preferences, and
lint-staged globs.

## ESLint v9 — eslint.config.mjs

Use `typescript-eslint` with type-checked rules
and `eslint-config-prettier`:

```js
import eslint from '@eslint/js';
import { defineConfig } from 'eslint/config';
import tseslint from 'typescript-eslint';
import prettierConfig from 'eslint-config-prettier';

export default defineConfig(
  eslint.configs.recommended,
  tseslint.configs.recommendedTypeChecked,
  prettierConfig,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      '@typescript-eslint/no-unused-vars': [
        'warn',
        { argsIgnorePattern: '^_' },
      ],
    },
  },
  {
    ignores: ['dist/', 'node_modules/', 'coverage/'],
  },
);
```

## Prettier — .prettierrc

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

## lint-staged

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix --cache",
      "prettier --write"
    ],
    "*.{js,json,md,css}": [
      "prettier --write"
    ]
  }
}
```
