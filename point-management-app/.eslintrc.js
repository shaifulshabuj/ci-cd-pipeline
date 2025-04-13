module.exports = {
  env: {
    node: true,
    jest: true,
    es2021: true
  },
  extends: 'eslint:recommended',
  parserOptions: {
    ecmaVersion: 2021
  },
  rules: {
    'no-console': 'off',
    'no-unused-vars': 'warn',
    'semi': ['error', 'always'],
    'quotes': ['warn', 'single']
  }
};