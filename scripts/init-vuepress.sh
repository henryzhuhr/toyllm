if ! command -v pnpm &> /dev/null
then
    echo "pnpm could not be found"
    exit
fi

if [ ! -f "package.json" ]; then
  pnpm init
fi


pnpm add -D \
    vuepress@next \
    vue \
    @vuepress/bundler-vite@next \
    @vuepress/theme-default@next \
    @vuepress/plugin-copy-code@next \
    @vuepress/plugin-back-to-top@next \
    @vuepress/plugin-docsearch@next \
    @vuepress/plugin-external-link-icon@next \
    @vuepress/plugin-git@next


if [ ! -d "docs/.vuepress" ]; then
  mkdir -p docs/.vuepress
fi

project_name=$(basename `pwd`)

# docs/.vuepress/config.js
file_content="import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { defineUserConfig } from 'vuepress'
import { copyCodePlugin } from '@vuepress/plugin-copy-code'
import { backToTopPlugin } from '@vuepress/plugin-back-to-top'
import { docsearchPlugin } from '@vuepress/plugin-docsearch'
import { externalLinkIconPlugin } from '@vuepress/plugin-external-link-icon'
import { gitPlugin } from '@vuepress/plugin-git'


export default defineUserConfig({
    base: '/$project_name/',
    title: '$project_name',
    description: '',
    bundler: viteBundler(),
    theme: defaultTheme(),
    plugins: [
        // https://ecosystem.vuejs.press/zh/plugins/copy-code.html
        copyCodePlugin({
            showInMobile: true,
        }),
        // https://ecosystem.vuejs.press/zh/plugins/back-to-top.html
        backToTopPlugin(),
        // https://ecosystem.vuejs.press/zh/plugins/docsearch.html
        docsearchPlugin({
            locales: {
                '/': {
                    placeholder: '搜索文档',
                    translations: {
                        button: {
                            buttonText: '搜索文档',
                        },
                    },
                },
            }
        }),
        externalLinkIconPlugin({}),
        gitPlugin({}),
    ],
})"
config_file="docs/.vuepress/config.ts"
if [ ! -f "$config_file" ]; then
  echo "$file_content" > docs/.vuepress/config.ts
  echo "# Vuepress" >> .gitignore
  echo "node_modules" >> .gitignore
  echo ".vuepress/.temp" >> .gitignore
  echo ".vuepress/.cache" >> .gitignore
  echo ".vuepress/dist" >> .gitignore
fi

if [ ! -f "docs/README.md" ]; then
  echo "# Document for ${project_name}" > docs/README.md
fi

workflow_content='name: docs

on:
  # 每当 push 到 dev 分支时触发部署
  push:
    branches: [main]
  # 手动触发部署
  workflow_dispatch:

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout this
        # @see https://github.com/actions/checkout
        uses: actions/checkout@v3
            
      - name: Install Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20

      - name: Run install
        # @see https://github.com/marketplace/actions/setup-pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 9
          run_install: |
            - recursive: true
              args: [--frozen-lockfile, --strict-peer-dependencies]
            - args: [--global, gulp, prettier, typescript]
      
      - name: Build VuePress site
        run: pnpm docs:build

      - name: Deploy to GitHub Pages
        # @see https://github.com/crazy-max/ghaction-github-pages
        uses: crazy-max/ghaction-github-pages@v2
        with:
          # 部署到 gh-pages 分支
          target_branch: gh-pages
          # 部署目录为 VuePress 的默认输出目录
          build_dir: docs/.vuepress/dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'
if [ ! -d ".github/workflows" ]; then
  mkdir -p .github/workflows
fi

workflow_file=".github/workflows/docs-pnpm.yml"
if [ ! -f "$workflow_file" ]; then
  echo "$workflow_content" > $workflow_file
fi

echo "\033[00;32m"
echo "Please add the following scripts to your package.json file in the \"scripts\" section:"
echo ""
echo '  "docs:dev": "vuepress dev docs",'
echo '  "docs:build": "vuepress build docs",'
echo "\033[0m"